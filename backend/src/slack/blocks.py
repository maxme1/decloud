from __future__ import annotations

from typing import Literal, Union

from pydantic import Field, model_validator

from .. import elements
from ..utils import NoExtra
from .elements import Element, PlainText, convert_elements
from .utils import file_url


class BlockBase(NoExtra):
    block_id: str | None = None

    def convert(self):
        dump = self.model_dump(exclude={'block_id'})
        if 'elements' in dump:
            dump['elements'] = convert_elements(self.elements)
        return dump


class RichText(BlockBase):
    type: Literal['rich_text']
    elements: list[Element]

    def convert(self):
        return elements.Sequence(elements=convert_elements(self.elements))


# TODO
class Call(BlockBase, extra='ignore'):
    type: Literal['call']
    call_id: str
    api_decoration_available: bool
    call: dict


class Section(BlockBase):
    type: Literal['section']
    # TODO
    text: Element | None = None
    fields: list[Element] = Field(default_factory=list)
    # TODO
    accessory: dict | None = None

    @model_validator(mode='after')
    def _mutex(cls, v):
        assert bool(v.element) != bool(v.fields), (v.element, v.fields)
        return v

    def convert(self):
        # TODO: accessory
        # assert not self.accessory, self.accessory
        return elements.Section(element=elements.Sequence(
            elements=convert_elements(self.fields) if self.fields else [self.text.convert()]
        ))


class Header(BlockBase):
    type: Literal['header']
    text: PlainText

    def convert(self):
        return elements.Header(text=self.text.convert())


class Context(BlockBase):
    type: Literal['context']
    elements: list[Element]


class Divider(BlockBase):
    type: Literal['divider']


class Image(BlockBase):
    type: Literal['image']
    image_url: str
    alt_text: str
    fallback: str
    image_width: int
    image_height: int
    image_bytes: int
    is_animated: bool = False
    rotation: int = 0

    def convert(self):
        return elements.Image(url=file_url(self.image_url))


class Actions(BlockBase):
    type: Literal['actions']
    elements: list[Element]


type Block = Union[*BlockBase.__subclasses__()]
