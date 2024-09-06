from typing import Union

from pydantic import model_validator

from ..utils import NoExtra


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
