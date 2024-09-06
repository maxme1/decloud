from __future__ import annotations

from typing import Literal, Union

from .utils import NoExtra


class ElementBase(NoExtra):
    pass


# legacy


class Header(ElementBase):
    type: Literal['header'] = 'header'
    element: Element


class Context(ElementBase):
    type: Literal['context'] = 'context'
    elements: list[Element]


class Divider(ElementBase):
    type: Literal['divider'] = 'divider'


class Actions(ElementBase):
    type: Literal['actions'] = 'actions'
    # TODO
    elements: list


class Button(ElementBase):
    type: Literal['button'] = 'button'
    text: Text
    value: str | None = None
    action_id: str
    # url: str | None = None
    style: Literal['ordered', 'bullet', 'primary'] | None = None
    # confirm: dict | None = None


# styles

class Quote(ElementBase):
    type: Literal['quote'] = 'quote'
    element: Element


class Bold(ElementBase):
    type: Literal['bold'] = 'bold'
    element: Element


class Italic(ElementBase):
    type: Literal['italic'] = 'italic'
    element: Element


class Strike(ElementBase):
    type: Literal['strike'] = 'strike'
    element: Element
    position: Literal['under', 'over', 'through']


class Code(ElementBase):
    type: Literal['code'] = 'code'
    element: Element
    language: str | None


class Preformat(ElementBase):
    type: Literal['pre'] = 'pre'
    element: Element


# containers

class Sequence(ElementBase):
    type: Literal['sequence'] = 'sequence'
    elements: list[Element]

    @classmethod
    def wrap(cls, elements):
        if len(elements) == 1:
            return elements[0]
        return cls(elements=elements)


class Section(ElementBase):
    type: Literal['section'] = 'section'
    element: Element


class List(ElementBase):
    type: Literal['list'] = 'list'
    elements: list[Element]
    style: Literal['ordered', 'unordered']


# primitives

class Text(ElementBase):
    type: Literal['text'] = 'text'
    text: str


class EmojiBase(NoExtra):
    name: str | None
    unicode: str | None
    skin_tone: int | None
    url: str | None


class Emoji(ElementBase, EmojiBase):
    type: Literal['emoji'] = 'emoji'


class Link(ElementBase):
    type: Literal['link'] = 'link'
    url: str
    element: Element | None


class Color(ElementBase):
    type: Literal['color'] = 'color'
    value: str


# mentions

class Channel(ElementBase):
    type: Literal['channel'] = 'channel'
    channel_id: str
    text: str | None


class Broadcast(ElementBase):
    type: Literal['broadcast'] = 'broadcast'
    range: Literal['channel', 'here', 'everyone']


class User(ElementBase):
    type: Literal['user'] = 'user'
    user_id: str
    element: Element | None


class UserGroup(ElementBase):
    type: Literal['usergroup'] = 'usergroup'
    usergroup_id: str


# misc

class Contact(ElementBase):
    type: Literal['contact'] = 'contact'
    name: str | None
    phone: str | None


class Location(ElementBase):
    type: Literal['location'] = 'location'
    name: str | None
    address: str | None
    latitude: float | None
    longitude: float | None


# media

class Image(ElementBase):
    type: Literal['image'] = 'image'
    url: str | None
    name: str | None


class Icon(ElementBase):
    type: Literal['icon'] = 'icon'
    url: str | None
    name: str | None


class Sticker(ElementBase):
    type: Literal['sticker'] = 'sticker'
    url: str | None
    emoji: Emoji | None
    mimetype: str | None


class Video(ElementBase):
    type: Literal['video'] = 'video'
    url: str | None
    thumbnail: str | None
    name: str | None
    size: int | None


class Audio(ElementBase):
    type: Literal['audio'] = 'audio'
    url: str | None
    thumbnail: str | None
    name: str | None


class File(ElementBase):
    type: Literal['file'] = 'file'
    url: str | None
    name: str | None
    mimetype: str | None
    thumbnail: str | None


type Element = Union[*ElementBase.__subclasses__()]
