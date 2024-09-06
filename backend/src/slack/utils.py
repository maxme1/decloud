from functools import cache
from pathlib import Path

import deli

from ..settings import settings


def to_unicode(x: str | None):
    if x is None:
        return
    return int(x, 16).to_bytes(4, 'big').decode('utf-32-be')


def file_url(x):
    if x and (settings.slack_root / 'files' / x).exists():
        return f'{settings.base_url}/files/slack/{x}'


@cache
def standard_emojis():
    # TODO: modifiers, e.g. skin tone
    standard = {
        x['shortname'][1:-1]: x['unicode'] for x in
        deli.load(Path(__file__).parent.parent.parent / 'emojis.json')['emojis']
    }
    slack = deli.load(Path(__file__).parent.parent.parent / 'slack_emojis.json')
    for name, code in slack.items():
        if code not in standard and name not in standard:
            try:
                int(code, 16)
            except ValueError:
                continue

            standard[name] = code

    return standard
