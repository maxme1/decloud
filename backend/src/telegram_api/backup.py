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
from tqdm.auto import tqdm

from ..backup import app
from .models.chat import Chat
from .models.media import File
from .models.message import Message
from .models.sender import SenderUser
from .models.user import User
from ..utils import load_backup, save_backup


# https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html


class TgSettings(BaseSettings):
    api_id: int
    api_hash: str
    phone: str
    library_path: Path | None = None
    files_directory: Path | None = None
    encryption_key: str | None = None


@app.command()
def telegram_sdk(storage: Path):
    from telegram.client import Telegram

    settings = TgSettings(_env_file=storage / '.env')
    encryption_key = settings.encryption_key
    if encryption_key is None:
        encryption_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        rich.print(f"You db encryption key is: [bold red]{encryption_key}[/bold red] Save it to your env file!")

    files_dir = settings.files_directory or (storage / 'session')
    files_dir.mkdir(exist_ok=True)

    client = Telegram(
        settings.api_id,
        settings.api_hash,
        database_encryption_key=encryption_key,
        phone=settings.phone,
        library_path=settings.library_path,
        files_directory=files_dir,
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

    # TODO: move to args
    update_chats = update_messages = update_users = update_files = True

    # update the chats list
    chats_path = storage / 'chats.json'
    chats = load_backup(chats_path)

    if update_chats:
        for chat in set(chats_ids) - {x['id'] for x in chats}:
            chat = wait(client.get_chat(chat))
            chats.append(chat)

        save_backup(chats, chats_path)

    # update the messages and gather files and users
    chat_files, user_ids = defaultdict(list), set()
    if update_messages or update_files or update_users:
        for chat in tqdm(chats, desc='Downloading messages'):
            chat = Chat.model_validate(chat)
            messages_path = storage / f'messages/{chat.id}.json'
            messages = load_backup(messages_path)

            if update_messages:
                with tqdm(
                        get_all_messages(client, chat.id, to_message_id=max((x['id'] for x in messages), default=None)),
                        desc=f'{chat.title} (id: {chat.id})', leave=False,
                ) as bar:
                    for message in bar:
                        messages.append(message)

                    # drop duplicates
                    messages = list({x['id']: x for x in messages}.values())
                    save_backup(messages, messages_path)
                    time.sleep(1)

            if update_files or update_users:
                for message in messages:
                    message = Message.model_validate(message)

                    if isinstance(message.sender_id, SenderUser):
                        user_ids.add(message.sender_id.user_id)

                    # drop bots and channels for now
                    if isinstance(chat.type, Chat.ChatTypePrivate):
                        chat_files[chat.id].extend(message.content.get_files())

    # update the users
    users_path = storage / 'users.json'
    users = load_backup(users_path)

    if update_users:
        for user in user_ids - {x['id'] for x in users}:
            try:
                user = wait(client.get_user(user))
            except RuntimeError as e:
                rich.print(f'[red]Error getting user {user}: {e}[/red]')
                continue

            users.append(user)

        save_backup(users, users_path)

    # gather more files
    files = []
    for user in users:
        user = User.model_validate(user)
        # drop bots and channels for now
        if not isinstance(user.type, (User.RegularUser, User.DeletedUser)):
            chat_files.pop(user.id, None)

        if user.profile_photo:
            files.append(user.profile_photo.big)
            files.append(user.profile_photo.small)

    for file_ids in chat_files.values():
        files.extend(file_ids)

    # download the files
    if update_files:
        files_root = storage / 'files'
        files_db_path = files_root / 'files.json'
        skipped_db_path = files_root / 'skipped.json'
        db = load_backup(files_db_path)
        skipped = set(load_backup(skipped_db_path))
        n_skipped = 0
        with tqdm(
                {x.remote.id for x in files} - {x['remote_id'] for x in db} - skipped, desc='Downloading files'
        ) as bar:
            try:
                for file_id in bar:
                    # file ids are generated each time the client is created
                    file = File.model_validate(wait(client.call_method(
                        'getRemoteFile', params=dict(remote_file_id=file_id)
                    )))
                    if file.remote.id == file_id:
                        success = _update_files_db(client, file.id, files_root, db)
                    else:
                        # TODO???
                        success = False

                    n_skipped += not success
                    if not success:
                        bar.set_postfix_str(f'Skipped: {n_skipped}')
                        skipped.add(file_id)

                    time.sleep(0.1)

            except KeyboardInterrupt as e:
                save_backup(db, files_db_path)
                save_backup(list(skipped), skipped_db_path)
                raise typer.Exit(1) from e

            save_backup(db, files_db_path)
            save_backup(list(skipped), skipped_db_path)


def wait(response):
    response.wait()
    if response.error:
        raise RuntimeError(response.error_info)
    update = response.update
    update.pop('@extra', None)
    time.sleep(0.1)
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
    db = load_backup(db_path)
    _update_files_db(client, file_id, storage, db)
    save_backup(db, db_path)


def _update_files_db(client, file_id, storage, db) -> bool:
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
            elif not (file.local.is_downloading_active or file.local.is_downloading_completed):
                path = False

    if any(x['remote_id'] == file_id for x in db):
        return True

    path = None
    storage = Path(storage)
    client.add_update_handler('updateFile', handler)
    try:
        result = wait(client.call_method('downloadFile', params=dict(file_id=file_id, priority=1, synchronous=False)))
        result = File.model_validate(result)
        if done(result):
            path = result.local.path

        while path is None:
            time.sleep(0.01)

        if not path:
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
