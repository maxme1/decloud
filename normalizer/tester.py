import sys

import deli


interesting = {
    'media_type': [
        'sticker', 'animation', 'video_file', 'audio_file', 'video_message',
        'voice_message',
    ],
    'action': [
        'phone_call',

        'edit_chat_theme',
    ],
    'type': [
        'message', 'service'
    ],
    'mime_type': [
        'video/mp4', 'text/plain', 'image/png', 'audio/mpeg', 'image/gif', 'image/jpeg',
        'audio/ogg', 'text/x-python', 'image/vnd.djvu',

        'text/x-tex', 'text/csv', 'text/html', 'text/x-python-script', 'text/x-csrc', 'video/mp2ts',
        'text/x-script.phyton', 'text/x-c', 'text/x-h', 'text/x-c++src', 'image/heic', 'audio/aac',

        'application/octet-stream', 'application/vnd.ms-publisher', 'application/vnd.sqlite3',
        'application/x-java-archive', 'application/x-bittorrent', 'application/pdf', 'application/x-compressed-tar',
        'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/x-7z-compressed', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/xml', 'application/x-zip-compressed', 'application/zip', 'text/vnd.trolltech.linguist',
        'application/x-ms-dos-executable', 'application/x-ipynb+json', 'multipart/x-zip', 'application/javascript',
        'application/json', 'application/x-msexcel',
    ],
    #     'discard_reason': [

    #     ]
}

for m in deli.load(sys.argv[1])['messages'][::-1]:
    if 'action' in m:
        assert m['type'] == 'service'

    missing = set(m) - set(interesting) - {
        'text_entities', 'from', 'height', 'photo', 'width', 'edited', 'reply_to_message_id',
        'sticker_emoji', 'forwarded_from', 'mime_type', 'via_bot', 'file',
        'location_information', 'contact_information', 'actor', 'discard_reason',
        'live_location_period_seconds',
    } - {
                  'from_id', 'text', 'date', 'id', 'date_unixtime', 'edited_unixtime', 'thumbnail',
                  'duration_seconds', 'actor_id',
              }
    if missing:
        print('!!', {k: m[k] for k in missing})

    for k, present in interesting.items():
        if k in m and m[k] not in present:
            if not (k == 'mime_type' and m[k].startswith('application/')):
                print(k, m[k])

        # if 'media_type' not in m and 'file' in m:
        #     print('file', m['file'].split('.')[-1])

    for x in m['text_entities']:
        if x['type'] not in [
            'plain', 'link', 'pre', 'code', 'text_link', 'email', 'bold', 'hashtag',
            'italic', 'phone', 'mention',

            #
            'cashtag', 'bank_card', 'underline', 'mention_name', 'custom_emoji', 'blockquote',
        ]:
            print(x)
