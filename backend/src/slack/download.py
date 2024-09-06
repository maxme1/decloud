import datetime
import shutil
import time
from pathlib import Path

import deli
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from tqdm.auto import tqdm


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

        if unpack is not None:
            for x in response[unpack]:
                yield x
        else:
            yield response

        if mode == 'cursor':
            pagination['cursor'] = response.get('response_metadata', {}).get('next_cursor')
            if pagination['cursor'] is None:
                break

        else:
            print(response['paging'])
            pagination['page'] += 1
            if response['paging']['pages'] < pagination['page']:
                break


def get_files(client: WebClient, root: Path):
    root = Path(root)
    errors, no_url = [], []
    min_free_size = 20 * 1024 ** 3  # 20Gb
    for file in tqdm(paginated(client.files_list, unpack='files', show_files_hidden_by_limit=True, limit=200)):
        if shutil.disk_usage(root).free < min_free_size:
            break

        # if file.size > max_file_size:
        #     too_big.append(file)
        #     continue

        file_id = file['id']
        meta = root / f'{file_id}.meta.json'
        content = root / file_id

        if not meta.exists():
            deli.save(file, meta)

        if not content.exists():
            if 'url_private_download' not in file:
                no_url.append(file)

            else:
                try:
                    download(client, file['url_private_download'], content)

                except (ConnectionError, requests.ConnectionError):
                    errors.append(file)

    return errors, no_url


def download(client: WebClient, url, to):
    headers = {"Authorization": "Bearer " + client.token}
    with open(to, 'wb') as out:
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            out.write(chunk)


def get_conversations(client: WebClient, root):
    root = Path(root)
    for c in client.conversations_list(limit=500):
        channel = c['id']
        path = root / f'{channel}.json'
        if path.exists():
            continue

        print(c['name'])

        try:
            msgs = deli.load(path)
        except FileNotFoundError:
            msgs = []

        if not msgs:
            oldest = None

        else:
            oldest = msgs[-1]['ts']

        print(datetime.datetime.fromtimestamp(float(oldest or 0)))  # , datetime.datetime.fromtimestamp(float(latest)))

        for m in tqdm(paginated(
                client.conversations_history, unpack='messages',
                channel=channel, oldest=oldest, limit=200, include_all_metadata=True,
        )):
            msgs.append(m)
            if m.get('reply_count', 0) > 0:
                assert 'replies' not in m
                m['replies'] = sorted(list(paginated(
                    client.conversations_replies, unpack="messages", channel=channel, ts=m['ts'], limit=200
                )), key=lambda x: float(x['ts']))

        assert len(msgs) - len({x['ts'] for x in msgs}) == 0
        msgs = sorted(msgs, key=lambda x: float(x['ts']))
        deli.save(msgs, channel + '.json')

        time.sleep(1)
