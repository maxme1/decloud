import hashlib
import json
import shutil
import sys
from pathlib import Path

import deli
from tqdm.auto import tqdm


MISSING_FILE = '(File not included. Change data exporting settings to download.)'


def transfer(path, storage):
    hasher = hashlib.sha256()
    with open(path, 'rb') as file:
        while content := file.read(1024 ** 2):
            hasher.update(content)

        if '.' not in path.name:
            ext = ''
        else:
            ext = '.' + path.name.split('.')[-1]

    relative = f'storage/{hasher.hexdigest()}{ext}'
    (storage / 'storage').mkdir(exist_ok=True)
    target = storage / relative
    if not target.exists():
        shutil.copyfile(path, target)

    return relative


def normalize(storage, root):
    def replace(d, k):
        if k not in d:
            return
        if d[k] == MISSING_FILE:
            return

        local = root / d[k]
        if local not in mapping:
            mapping[local] = transfer(local, storage)
        d[k] = mapping[local]

    root, storage = Path(root), Path(storage)

    content = deli.load(root / 'result.json')
    mapping = {}
    for message in tqdm(content['messages']):
        for key in 'file', 'thumbnail', 'photo', 'contact_vcard':
            replace(message, key)

        for entity in message['text_entities']:
            replace(entity, 'document_id')
        if isinstance(message['text'], list):
            for text in message['text']:
                if isinstance(text, dict):
                    replace(text, 'document_id')

    # make sure we copied all the files
    missing = {x for x in root.rglob('*') if not x.is_dir()} - set(mapping) - {root / 'result.json'}
    assert not missing, missing

    chat_id = content['id']
    current_path = storage / f'{chat_id}.json'
    if not current_path.exists():
        current = content

    else:
        current = deli.load(current_path)
        mapping = {x['id']: x for x in current['messages']}
        assert len(mapping) == len(current['messages'])

        for message in content['messages']:
            if message['id'] in mapping:
                old = mapping[message['id']]
                assert json.dumps(message, sort_keys=True) == json.dumps(old, sort_keys=True), (old, message)

            else:
                current['messages'].append(message)

        current['name'] = content['name']

    deli.save(current, current_path)

    # update the chats list
    chats_path = storage / 'chats.json'
    if not chats_path.exists():
        chats = {}
    else:
        chats = deli.load(chats_path)
    chats[chat_id] = current['name']
    deli.save(chats, chats_path)


if __name__ == '__main__':
    normalize(*sys.argv[1:])
