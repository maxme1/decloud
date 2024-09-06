from functools import cache

import deli
from pydantic import model_validator

from ..settings import settings
from ..utils import NoExtra


@cache
def id_to_file():
    return {x['id']: x['filename'] for x in deli.load(settings.telegram_api_root / 'files/files.json')}


@cache
def custom_emojis():
    return {x['id']: x['emoji'] for x in deli.load(settings.telegram_api_root / 'custom-emojis.json')}


def file_url(file_id: int | None) -> str | None:
    if file_id is None:
        return None

    if file_id not in id_to_file():
        print(f'File {file_id} not found')
        return

    return f'{settings.base_url}/files/telegramapi/{file_id}'


class TypeDispatch(NoExtra):
    @model_validator(mode='before')
    def _adjust_type(cls, values):
        if isinstance(values, dict) and '@type' in values:
            assert 'type_' not in values, list(values)
            values['type_'] = values.pop('@type')

        return values
