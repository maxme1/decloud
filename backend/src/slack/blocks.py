from __future__ import annotations

from typing import Literal, Union

from pydantic import Field, model_validator

from .. import blocks
from ..utils import NoExtra
from .elements import Element, PlainText
from .utils import file_url


class BlockBase(NoExtra):
    block_id: str | None = None

    def convert(self):
        dump = self.model_dump(exclude={'block_id'})
        if 'elements' in dump:
            dump['elements'] = [x.convert() for x in self.elements]
        return dump


class RichText(BlockBase):
    type: Literal['rich_text']
    elements: list[Element]

    def convert(self):
        return blocks.RichText(elements=[x.convert() for x in self.elements])


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
        assert bool(v.text) != bool(v.fields), (v.text, v.fields)
        return v

    def convert(self):
        return blocks.Section(
            elements=[x.convert() for x in self.fields] if self.fields else [self.text.convert()],
            accessory=self.accessory,
        )


class Header(BlockBase):
    type: Literal['header']
    text: PlainText


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
        return blocks.Image(url=file_url(self.image_url))


class Actions(BlockBase):
    type: Literal['actions']
    elements: list[Element]


type Block = Union[*BlockBase.__subclasses__()]
