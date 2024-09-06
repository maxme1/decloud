import sys

import deli

present = [
    'video/mp4', 'text/plain', 'image/png', 'audio/mpeg', 'image/gif', 'image/jpeg',
    'audio/ogg', 'text/x-python', 'image/vnd.djvu', 'image/webp',

    'text/x-tex', 'text/csv', 'text/html', 'text/x-python-script', 'text/x-csrc', 'video/mp2ts',
    'text/x-script.phyton', 'text/x-c', 'text/x-h', 'text/x-c++src', 'image/heic', 'audio/aac',

    'application/octet-stream', 'application/vnd.ms-publisher', 'application/vnd.sqlite3',
    'application/x-java-archive', 'application/x-bittorrent', 'application/pdf', 'application/x-compressed-tar',
    'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/x-7z-compressed', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/xml', 'application/x-zip-compressed', 'application/zip', 'text/vnd.trolltech.linguist',
    'application/x-ms-dos-executable', 'application/x-ipynb+json', 'multipart/x-zip', 'application/javascript',
    'application/json', 'application/x-msexcel',
]
k = 'mime_type'

file, = sys.argv[1:]
for m in deli.load(file)['messages']:
    if k in m and m[k] not in present:
        if not m[k].startswith(('application/', 'text/')):
            print(k, m[k])
