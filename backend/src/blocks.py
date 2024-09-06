from __future__ import annotations

from typing import Literal, Union

from .elements import Element, PlainText
from .utils import NoExtra


class BlockBase(NoExtra):
    pass


class RichText(BlockBase):
    type: Literal['rich_text'] = 'rich_text'
    elements: list[Element]


# TODO
class Call(BlockBase, extra='ignore'):
    type: Literal['call'] = 'call'
    call_id: str
    api_decoration_available: bool
    call: dict


class Section(BlockBase):
    type: Literal['section'] = 'section'
    elements: list[Element]
    # TODO
    accessory: dict | None = None


class Header(BlockBase):
    type: Literal['header'] = 'header'
    text: PlainText


class Context(BlockBase):
    type: Literal['context'] = 'context'
    elements: list[Element]


class Divider(BlockBase):
    type: Literal['divider'] = 'divider'


class Actions(BlockBase):
    type: Literal['actions'] = 'actions'
    # TODO
    elements: list


# media


class Video(BlockBase):
    type: Literal['video'] = 'video'
    url: str | None
    thumbnail: str | None


class Audio(BlockBase):
    type: Literal['audio'] = 'audio'
    url: str | None


# TODO: same as attachments?
class File(BlockBase):
    type: Literal['file'] = 'file'
    url: str | None
    name: str | None
    mimetype: str | None


class Tombstone(BlockBase):
    type: Literal['tombstone'] = 'tombstone'


type Block = Union[*BlockBase.__subclasses__()]
