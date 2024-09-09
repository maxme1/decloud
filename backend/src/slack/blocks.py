from __future__ import annotations

from typing import Literal, Union

from pydantic import Field, model_validator

from .. import elements
from ..utils import NoExtra
from .elements import Element, PlainText, convert_elements


class BlockBase(NoExtra):
    block_id: str | None = None

    def convert(self, context):
        dump = self.model_dump(exclude={'block_id'})
        if 'elements' in dump:
            dump['elements'] = convert_elements(self.elements, context)
        return dump


class RichText(BlockBase):
    type: Literal['rich_text']
    elements: list[Element]

    def convert(self, context):
        return elements.Sequence(elements=convert_elements(self.elements, context))


# TODO
class Call(BlockBase, extra='ignore'):
    class CallVersions(NoExtra, extra='ignore'):
        class CallData(NoExtra, extra='ignore'):
            name: str

        v1: CallData

    type: Literal['call']
    call_id: str
    api_decoration_available: bool
    call: CallVersions

    def convert(self, context):
        return elements.Header(element=elements.Text(text=self.call.v1.name))


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

    def convert(self, context):
        # TODO: accessory
        # assert not self.accessory, self.accessory
        return elements.Section(element=elements.Sequence(
            elements=convert_elements(self.fields, context) if self.fields else [self.text.convert(context)]
        ))


class Header(BlockBase):
    type: Literal['header']
    text: PlainText

    def convert(self, context):
        return elements.Header(element=self.text.convert(context))


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

    def convert(self, context):
        return elements.Image(url=context.get_file_url(self.image_url), name=self.alt_text)


class Actions(BlockBase):
    type: Literal['actions']
    elements: list[Element]


type Block = Union[*BlockBase.__subclasses__()]
