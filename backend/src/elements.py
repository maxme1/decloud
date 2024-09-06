from __future__ import annotations

from typing import Literal, Union

from .utils import NoExtra


StyleStr = Literal['ordered', 'bullet', 'primary']
Style = dict


class ElementBase(NoExtra):
    style: Style | None = None


class Quote(ElementBase):
    type: Literal['quote'] = 'quote'
    element: Element


class Sequence(ElementBase):
    type: Literal['sequence'] = 'sequence'
    elements: list[Element]


class RichTextElement(ElementBase):
    type: Literal['rich_text_section', 'rich_text_preformatted', 'rich_text_quote']
    elements: list[Element]
    indent: int | None = None
    border: int | None = None
    offset: int | None = None


class RichTextList(ElementBase):
    type: Literal['rich_text_list'] = 'rich_text_list'
    elements: list[Element]
    indent: int | None = None
    border: int | None = None
    offset: int | None = None
    style: StyleStr


class Text(ElementBase):
    type: Literal['text'] = 'text'
    text: str


class PlainText(ElementBase):
    type: Literal['plain_text'] = 'plain_text'
    text: str
    emoji: bool


class Channel(ElementBase):
    type: Literal['channel'] = 'channel'
    channel_id: str
    text: str | None = None


class Markdown(ElementBase):
    type: Literal['mrkdwn'] = 'mrkdwn'
    text: str
    verbatim: bool


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
    text: str | None = None

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
    text: PlainText
    value: str | None = None
    action_id: str
    # url: str | None = None
    style: StyleStr | None = None
    # confirm: dict | None = None


class ImageElement(ElementBase):
    type: Literal['image'] = 'image'
    url: str | None = None


type Element = Union[*ElementBase.__subclasses__()]
