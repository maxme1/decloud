from __future__ import annotations

from typing import Literal, Union

from .utils import NoExtra


class ElementBase(NoExtra):
    pass


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


class Preformat(ElementBase):
    type: Literal['pre'] = 'pre'
    element: Element
    language: str | None


# containers

class Sequence(ElementBase):
    type: Literal['sequence'] = 'sequence'
    elements: list[Element]


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


class Channel(ElementBase):
    type: Literal['channel'] = 'channel'
    channel_id: str
    text: str | None = None


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
    # FIXME
    text: Element | None = None

    unsafe: bool | None = None


class Color(ElementBase):
    type: Literal['color'] = 'color'
    value: str


class Broadcast(ElementBase):
    type: Literal['broadcast'] = 'broadcast'
    range: Literal['channel', 'here', 'everyone']


class User(ElementBase):
    type: Literal['user'] = 'user'
    user_id: str
    text: str | None = None


class UserGroup(ElementBase):
    type: Literal['usergroup'] = 'usergroup'
    usergroup_id: str


class Button(ElementBase):
    type: Literal['button'] = 'button'
    text: Text
    value: str | None = None
    action_id: str
    # url: str | None = None
    style: Literal['ordered', 'bullet', 'primary'] | None = None
    # confirm: dict | None = None


class Image(ElementBase):
    type: Literal['image'] = 'image'
    url: str | None = None
    name: str | None = None


class Icon(ElementBase):
    type: Literal['icon'] = 'icon'
    url: str | None = None
    name: str | None = None


type Element = Union[*ElementBase.__subclasses__()]
