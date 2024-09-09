import datetime
from typing import Annotated, TypeVar, Union

from pydantic import BeforeValidator, model_validator

from ..utils import NoExtra


FlaggedTimestamp = Annotated[datetime.datetime | None, BeforeValidator(lambda x: x or None)]


class TypeDispatch(NoExtra):
    @model_validator(mode='before')
    def _adjust_type(cls, values):
        if isinstance(values, dict) and '@type' in values:
            assert 'type_' not in values, list(values)
            values['type_'] = values.pop('@type')

        return values


T = TypeVar('T')


class Subclasses:
    def __class_getitem__(cls, item: T) -> T:
        return Union[*item.__subclasses__()]
