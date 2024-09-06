import hashlib
import shutil
import time
from pathlib import Path

import deli

from .models.media import File


# https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html
def wait(response):
    response.wait()
    if response.error:
        raise RuntimeError(response.error_info)
    return response.update


def get_all_messages(client, chat_id):
    from_message_id = 0
    while True:
        response = wait(client.get_chat_history(
            chat_id=chat_id,
            limit=1000,
            from_message_id=from_message_id,
        ))
        for message in response['messages']:
            yield message
            from_message_id = message['id']

        if not response.update['total_count']:
            break

        time.sleep(1)


def download_file(client, file_id, storage):
    db_path = storage / 'files.json'
    if not db_path.exists():
        storage.mkdir(exist_ok=True)
        db = []
    else:
        db = deli.load(db_path)

    _update_files_db(client, file_id, storage, db)
    deli.save(db, db_path)


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
        result = wait(client.call_method('downloadFile', params=dict(file_id=file_id, priority=1, synchronous=False)))
        result.pop('@extra', None)
        result = File.model_validate(result)
        if done(result):
            path = result.local.path

        while path is None:
            time.sleep(0.1)

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
