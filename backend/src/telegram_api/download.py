import hashlib
import secrets
import shutil
import string
import time
from collections import defaultdict
from pathlib import Path

import deli
import rich
import typer
from pydantic_settings import BaseSettings
from rich.progress import track
from tqdm.auto import tqdm

from .models.chat import Chat
from .models.media import File
from .models.message import Message, SenderUser
from .models.user import User
from ..backup import app


class TgSettings(BaseSettings):
    api_id: int
    api_hash: str
    phone: str
    library_path: Path | None = None
    files_directory: Path | None = None
    encryption_key: str | None = None


@app.command()
def telegram_api(storage: Path, env_file: Path):
    from telegram.client import Telegram

    settings = TgSettings(_env_file=env_file)
    encryption_key = settings.encryption_key
    if encryption_key is None:
        encryption_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        rich.print(f"You db encryption key is: [bold red]{encryption_key}[/bold red] Save it to your env file!")

    client = Telegram(
        settings.api_id,
        settings.api_hash,
        database_encryption_key=encryption_key,
        phone=settings.phone,
        library_path=settings.library_path,
        files_directory=settings.files_directory,
        use_message_database=False,
        tdlib_verbosity=0,
        # device_model: str = 'python-telegram',
        # application_version: str = '0.19.0',
        # system_version: str = 'unknown',
    )
    client.login()
    download(client, storage)


def download(client, storage):
    storage = Path(storage)
    # fixme
    chats_ids = wait(client.get_chats(limit=1000))['chat_ids']
    assert len(chats_ids) < 1000

    # update the chats list
    chats_path = storage / 'chats.json'
    chats = load(chats_path)

    for chat in set(chats_ids) - {x['id'] for x in chats}:
        chat = wait(client.get_chat(chat))
        chat.pop('@extra', None)
        chats.append(chat)

    save(chats, chats_path)

    # update the messages and gather files and users
    chat_files, user_ids = defaultdict(set), set()
    for chat in tqdm(chats, desc='Downloading messages'):
        continue
        chat = Chat.model_validate(chat)
        messages_path = storage / f'messages/{chat.id}.json'
        messages = load(messages_path)

        with tqdm(
                get_all_messages(client, chat.id, to_message_id=max((x['id'] for x in messages), default=None)),
                desc=f'{chat.title} (id: {chat.id})', leave=False,
        ) as bar:
            for message in bar:
                messages.append(message)
                message = Message.model_validate(message)

                if isinstance(message.sender_id, SenderUser):
                    user_ids.add(message.sender_id.user_id)

                # drop bots and channels for now
                if isinstance(chat.type, Chat.ChatTypePrivate):
                    chat_files[chat.id].update(x.id for x in message.content.get_files())

            # drop duplicates
            messages = list({x['id']: x for x in messages}.values())
            save(messages, messages_path)
            time.sleep(1)

    # update the users
    users_path = storage / 'users.json'
    users = load(users_path)
    for user in user_ids - {x['id'] for x in users}:
        user = wait(client.get_user(user))
        user.pop('@extra', None)
        users.append(user)

    save(users, users_path)

    # gather more files
    files = set()
    for user in users:
        user = User.model_validate(user)
        # drop bots and channels for now
        if not isinstance(user.type, (User.RegularUser, User.DeletedUser)):
            chat_files.pop(user.id, None)

        if user.profile_photo:
            files.add(user.profile_photo.big.id)
            files.add(user.profile_photo.small.id)

    for file_ids in chat_files.values():
        files.update(file_ids)

    # download the files
    files_root = storage / 'files'
    files_db_path = files_root / 'files.json'
    db = load(files_db_path)
    for file_id in tqdm(files - {x['id'] for x in db}, desc='Downloading files'):
        _update_files_db(client, file_id, files_root, db)
        time.sleep(0.3)
    save(db, files_db_path)


def load(path):
    if path.exists():
        try:
            return deli.load(path)
        except Exception as e:
            rich.print(f'Error loading {path}: {e}')
            raise typer.Exit(1) from e

    return []


def save(data, path):
    tmp = path.with_stem('tmp-' + path.stem)
    deli.save(data, tmp)
    tmp.rename(path)


# https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html
def wait(response):
    response.wait()
    if response.error:
        raise RuntimeError(response.error_info)
    update = response.update
    update.pop('@extra', None)
    return update


def get_all_messages(client, chat_id, to_message_id: int | None = None):
    from_message_id = 0
    while True:
        response = wait(client.get_chat_history(chat_id=chat_id, limit=1000, from_message_id=from_message_id))
        for message in response['messages']:
            if to_message_id is not None and message['id'] == to_message_id:
                return

            yield message
            from_message_id = message['id']

        if not response['total_count']:
            return

        time.sleep(1)


def download_file(client, file_id, storage):
    db_path = storage / 'files.json'
    db = load(db_path)
    _update_files_db(client, file_id, storage, db)
    save(db, db_path)


def _update_files_db(client, file_id, storage, db):
    def done(file):
        return file.local.is_downloading_completed and file.local.path

    def handler(update):
        nonlocal path
        file = update['file']
        file.pop('@extra', None)
        file = File.model_validate(file)
        if file.id == file_id:
            if done(file):
                path = file.local.path
            elif not file.local.is_downloading_active:
                path = False

    storage = Path(storage)
    if any(x['id'] == file_id for x in db):
        return True

    path = None
    client.add_update_handler('updateFile', handler)
    try:
        result = client.call_method('downloadFile', params=dict(file_id=file_id, priority=1, synchronous=False))
        result = wait(result)
        # result.wait()
        # if result.error and result.error_info['message'] == 'Invalid file identifier':
        #     rich.print(f'[red]Skipping file: {file_id}[/red]')
        #     return False
        # result = result.update
        # result.pop('@extra', None)
        result = File.model_validate(result)
        if done(result):
            path = result.local.path

        while path is None:
            time.sleep(0.1)

        if not path:
            rich.print(f'[red]Skipping file: {file_id}[/red]')
            return False

        if not isinstance(path, str):
            raise RuntimeError(path)

        path = Path(path)
        hasher = hashlib.sha256()
        with open(path, 'rb') as fd:
            while content := fd.read(1024 ** 2):
                hasher.update(content)

        if '.' not in path.name:
            ext = ''
        else:
            ext = '.' + path.name.split('.')[-1]

        filename = hasher.hexdigest()
        if not (storage / filename).exists():
            shutil.copyfile(path, storage / filename)
        db.append(dict(
            id=file_id, filename=filename, ext=ext, remote_id=result.remote.id, remote_uid=result.remote.unique_id,
        ))

    finally:
        client.remove_update_handler('updateFile', handler)

    return True
