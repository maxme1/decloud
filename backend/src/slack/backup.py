import time
from enum import StrEnum
from pathlib import Path

import requests
import rich
from pydantic_settings import BaseSettings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from ..backup import app
from ..utils import load_backup, nested_rich, save_backup


class SlackSettings(BaseSettings):
    token: str


class ChatType(StrEnum):
    public_channel = 'public_channel'
    private_channel = 'private_channel'
    multi_personal = 'multi_personal'
    personal = 'personal'


class ChatContent(StrEnum):
    conversations = 'conversations'
    messages = 'messages'
    users = 'users'
    files = 'files'


TYPE_MAPPING = {'multi_personal': 'mpim', 'personal': 'im'}


@app.command()
def slack(storage: Path, types: list[ChatType] = tuple(ChatType), content: list[ChatContent] = tuple(ChatContent)):
    settings = SlackSettings(_env_file=storage / '.env')
    client = WebClient(token=settings.token)
    update(client, storage, types, content)


def update(client: WebClient, storage: Path, conv_types, content_types):
    update_conversations, update_messages, update_users, update_files = (x in content_types for x in ChatContent)

    conversations_path = storage / 'conversations.json'
    conversations = load_backup(conversations_path)
    if update_conversations:
        old = conversations
        conversations = list(paginated(
            client.conversations_list, unpack='channels', limit=500,
            types=','.join(TYPE_MAPPING.get(x.value, x.value) for x in conv_types)
        ))
        old = _update(conversations, old)
        save_backup(old, conversations_path)

    profiles = {}
    if update_messages or update_users:
        with nested_rich() as progress:
            for conversation in progress(conversations, desc='Processing messages'):
                channel = conversation['id']
                path = storage / f'messages/{channel}.json'
                messages = load_backup(path)

                if update_messages:
                    oldest = max((x['ts'] for x in messages), key=float, default=None)
                    added = False
                    for message in progress(paginated(
                            client.conversations_history, unpack='messages',
                            channel=channel, oldest=oldest, limit=200, include_all_metadata=True,
                    ), leave=False, desc=conversation.get('name') or conversation.get('user') or channel):
                        messages.append(message)
                        added = True
                        if message.get('reply_count', 0) > 0:
                            assert 'replies' not in message
                            message['replies'] = sorted(paginated(
                                client.conversations_replies, unpack='messages', channel=channel, ts=message['ts'],
                                limit=200
                            ), key=lambda x: float(x['ts']))

                    if added:
                        assert len(messages) == len({x['ts'] for x in messages})
                        messages = sorted(messages, key=lambda x: float(x['ts']))
                        save_backup(messages, path)
                        time.sleep(0.5)

                    time.sleep(0.5)

                gather_profiles_(messages, profiles)

    users_path = storage / 'users.json'
    users = load_backup(users_path)
    if update_users:
        new = list(paginated(client.users_list, unpack='members', limit=500))
        users = _update(new, users)
        users = {x['id']: x for x in users}
        # update user info using the profiles
        for user_id, profile in profiles.items():
            if set(profile) <= {'id', 'is_bot'}:
                continue

            profile['id'] = user_id
            if user_id in users:
                p = profile.setdefault('profile', {})
                p.update(users[user_id]['profile'])
                profile.update(users[user_id])
                profile['profile'] = p

            users[user_id] = profile
        users = list(users.values())
        # save
        save_backup(users, users_path)

    if update_files:
        visited = set()
        errors, no_url = [], []
        with nested_rich() as progress:
            for file in progress(paginated(
                    client.files_list, unpack='files', mode='page', show_files_hidden_by_limit=True, limit=200
            ), desc='Downloading files'):
                file_id = file['id']
                if file_id in visited:
                    continue
                visited.add(file_id)

                meta = storage / f'files/{file_id}.meta.json'
                content = storage / 'files' / file_id

                if not meta.exists():
                    save_backup(file, meta)

                if not content.exists():
                    url = file.get('url_private_download')
                    if not url:
                        no_url.append(file)

                    else:
                        try:
                            download(client, url, content)
                        except (ConnectionError, requests.ConnectionError):
                            errors.append(file)

        if errors or no_url:
            rich.print(f"[red]Couldn't download {len(errors) + len(no_url)} files[/red]")


def gather_profiles_(messages, profiles):
    """ Messages often contain useful information regarding profiles """
    for message in messages:
        if message.get('user'):
            profile = profiles.setdefault(message['user'], {})
            profile.setdefault('is_bot', False)

            if message.get('username'):
                profile['name'] = message['username']
            if message.get('user_profile'):
                profile.setdefault('profile', {}).update(message['user_profile'])

        if message.get('bot_id'):
            profile = profiles.setdefault(message['bot_id'], {})
            profile.setdefault('is_bot', True)

            if message.get('username'):
                profile['name'] = message['username']
            if message.get('bot_profile'):
                profile.setdefault('profile', {}).update(message['bot_profile'])

        for att in message.get('attachments', []):
            if att.get('author_id'):
                profile = profiles.setdefault(att['author_id'], {})

                if att.get('author_name'):
                    profile.setdefault('profile', {}).setdefault('real_name', att['author_name'])
                if att.get('author_icon'):
                    profile.setdefault('profile', {}).setdefault('image_48', att['author_icon'])
                if att.get('author_subname'):
                    profile.setdefault('profile', {}).setdefault('real_name', att['author_subname'])


def _update(new, old):
    updated = {x['id'] for x in old}
    return new + [x for x in old if x['id'] not in updated]


def paginated(method, /, unpack=None, mode='cursor', limit: int = None, **kwargs):
    assert mode in ('cursor', 'page')
    pagination = dict(cursor=None, limit=limit) if mode == 'cursor' else dict(page=1, count=limit)
    while True:
        try:
            response = method(**pagination, **kwargs)
        except SlackApiError as error:
            if error.response['error'] == 'ratelimited':
                delay = int(error.response.headers['Retry-After'])
                time.sleep(delay)
                continue

            else:
                raise

        data = response.data
        if unpack is not None:
            for x in data[unpack]:
                yield x
        else:
            yield data

        if mode == 'cursor':
            assert 'paging' not in data
            cursor = data.get('response_metadata', {}).get('next_cursor')
            # either None or ''
            if not cursor:
                break

            pagination['cursor'] = cursor

        else:
            assert 'response_metadata' not in data
            pagination['page'] += 1
            if response['paging']['pages'] < pagination['page']:
                break


def download(client: WebClient, url, to):
    with open(to, 'wb') as out:
        response = requests.get(url, headers={'Authorization': f'Bearer {client.token}'}, timeout=10, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            out.write(chunk)
