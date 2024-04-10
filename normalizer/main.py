import hashlib
import json
import shutil
import sys
from pathlib import Path

import deli
from tqdm.auto import tqdm
from functools import cache
import os


@cache
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
    target = storage / relative
    if not target.exists():
        shutil.move(path, target)
    else:
        os.remove(path)

    return relative


def normalize_(content, root, storage):
    paths = ['file', 'thumbnail', 'photo']
    for m in tqdm(content['messages']):
        for key in paths:
            if key in m:
                m[key] = transfer(root / m[key], storage)


def normalize(storage, root):
    root, storage = Path(root), Path(storage)

    content = deli.load(root / 'result.json')
    normalize_(content, root, storage)
    # TODO: don't remove anything and just keep a list of visited files
    assert [x for x in root.rglob('*') if not x.is_dir()] == [root / 'result.json']
    shutil.rmtree(root)

    chat_id = content['id']
    current_path = storage / f'{chat_id}.json'
    if not current_path.exists():
        current = content

    else:
        current = deli.load(current_path)
        mapping = {x['id']: x for x in current['messages']}
        assert len(mapping) == len(current['messages'])

        for m in content['messages']:
            if m['id'] in mapping:
                assert json.dumps(m, sort_keys=True) == json.dumps(mapping[m['id']], sort_keys=True)

            else:
                current['messages'].append(m)

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
