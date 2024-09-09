import hashlib
import secrets
import shutil
import string
import time
from collections import defaultdict
from enum import Enum
from pathlib import Path

import rich
import typer
from pydantic_settings import BaseSettings
from tqdm.rich import tqdm

from ..backup import app
from ..utils import load_backup, nested_rich, save_backup
from .models.chat import Chat
from .models.media import File
from .models.message import CustomEmojiReaction, Message
from .models.text import TextEntityCustomEmoji
from .models.user import User


# https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html


class TgSettings(BaseSettings):
    api_id: int
    api_hash: str
    phone: str
    encryption_key: str
    library_path: Path | None = None
    files_directory: Path | None = None


@app.command()
def telegram_sdk(storage: Path):
    from telegram.client import Telegram  # noqa

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


class ChatType(Enum):
    bot, personal, group, supergroup, channel = range(5)

    @classmethod
    def detect(cls, chat: Chat, users: dict):
        match chat.type:
            case Chat.ChatTypePrivate(user_id=user_id):
                if user_id in users and isinstance(users[user_id].type, User.BotUser):
                    return cls.bot
                return cls.personal
            case Chat.ChatTypeBasicGroup():
                return cls.group
            case Chat.ChatTypeSupergroup(is_channel=is_channel):
                return cls.channel if is_channel else cls.supergroup
            case _:
                raise ValueError(f'Unknown chat type: {chat.type}')


def download(client, storage):
    storage = Path(storage)
    # fixme
    #  TODO: also update all chat lists
    chats_ids = wait(client.get_chats(limit=1000))['chat_ids']
    assert len(chats_ids) < 1000

    # TODO: move to args
    # filters
    #  content type
    update_chats = update_messages = update_users = update_files = True
    update_messages = False
    #  conversation type
    update_types = ChatType.personal, ChatType.group, ChatType.supergroup

    # update the chats list
    chats_path = storage / 'chats.json'
    chats = load_backup(chats_path)
    if update_chats:
        for chat in set(chats_ids) - {x['id'] for x in chats}:
            chat = wait(client.get_chat(chat))
            chats.append(chat)

        save_backup(chats, chats_path)

    # we need users beforehand to know the right chat types
    users_path = storage / 'users.json'
    users = load_backup(users_path)
    users_dict = {x['id']: User.model_validate(x) for x in users}
    for chat in chats:
        chat = Chat.model_validate(chat)
        if isinstance(chat.type, Chat.ChatTypePrivate):
            if isinstance(chat.type, Chat.ChatTypePrivate) and chat.type.user_id not in users_dict:
                user = get_user(client, chat.type.user_id)
                if user is not None:
                    users.append(user)
                    users_dict[user['id']] = User.model_validate(user)

    # update the messages and gather files and users
    chat_files, user_ids, emoji_ids = defaultdict(list), set(), set()
    if update_messages or update_files or update_users:
        with nested_rich() as progress:
            for chat in progress(chats, desc='Processing messages'):
                chat = Chat.model_validate(chat)
                chat_type = ChatType.detect(chat, users_dict)
                if chat_type not in update_types:
                    rich.print(
                        f'[yellow]Skipping chat {chat.title} '
                        f'because it is of type [italic]{chat_type.name}[/italic][/yellow]'
                    )
                    continue

                messages_path = storage / f'messages/{chat.id}.json'
                messages = load_backup(messages_path)

                if update_messages:
                    with progress(
                            get_all_messages(
                                client, chat.id, to_message_id=max((x['id'] for x in messages), default=None)
                            ),
                            desc=f'{chat.title} (id: {chat.id})', leave=False
                    ) as bar:
                        for message in bar:
                            messages.append(message)

                        # drop duplicates
                        messages = list({x['id']: x for x in messages}.values())
                        save_backup(messages, messages_path)
                        time.sleep(1)

                if update_files or update_users:
                    for message in progress(messages, desc=f'Processing messages for {chat.title}', leave=False):
                        message = Message.model_validate(message)

                        user_ids.update(message.get_user_ids())
                        chat_files[chat.id].extend(message.content.get_files())

                        if message.interaction_info and message.interaction_info.reactions:
                            for r in message.interaction_info.reactions.reactions:
                                if isinstance(r.type, CustomEmojiReaction):
                                    emoji_ids.add(r.type.custom_emoji_id)

                        if isinstance(message.content, TextEntityCustomEmoji):
                            emoji_ids.add(message.content.custom_emoji_id)

    # TODO: custom emojis

    # update the users
    if update_users:
        missing = 0
        for user in user_ids - {x['id'] for x in users}:
            user = get_user(client, user)
            if user is not None:
                users.append(user)
            else:
                missing += 1

        if missing:
            rich.print(f'[yellow]{missing} user(s) not found[/yellow]')
        save_backup(users, users_path)

    # gather more files
    files = []
    for user in users:
        user = User.model_validate(user)
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
        present = {x[FILE_UID_KEY] for x in db} | skipped
        with tqdm([file for file in files if get_file_uid(file) not in present], desc='Downloading files') as bar:
            try:
                for file in bar:
                    file_id = get_file_uid(file)
                    # file ids are generated each time the client is created
                    file = File.model_validate(wait(client.call_method(
                        'getRemoteFile', params=dict(remote_file_id=file.remote.id)
                    )))
                    assert file.remote.unique_id == file_id
                    success = _update_files_db(client, file.id, files_root, db)
                    n_skipped += not success
                    if not success:
                        # bar.set_postfix_str(f'Skipped: {n_skipped}')
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


def get_user(client, user):
    try:
        return wait(client.get_user(user))
    except RuntimeError as e:
        if e.args[0]['message'] != 'User not found':
            raise


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

    if any(x[FILE_UID_KEY] == file_id for x in db):
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


FILE_UID_KEY = 'remote_uid'


def get_file_uid(file: File):
    return file.remote.unique_id
