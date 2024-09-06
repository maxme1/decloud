from functools import cache
from typing import Union

import deli
from pydantic import model_validator

from ..settings import settings
from ..utils import NoExtra


@cache
def custom_emojis():
    return {x['id']: x['emoji'] for x in deli.load(settings.telegram_api_root / 'custom-emojis.json')}


class TypeDispatch(NoExtra):
    @model_validator(mode='before')
    def _adjust_type(cls, values):
        if isinstance(values, dict) and '@type' in values:
            assert 'type_' not in values, list(values)
            values['type_'] = values.pop('@type')

        return values


class Subclasses:
    def __class_getitem__(cls, item):
        return Union[*item.__subclasses__()]
