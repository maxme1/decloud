from __future__ import annotations

from functools import cache
from typing import Literal, Union

import deli

from .. import elements
from ..settings import settings
from ..utils import NoExtra
from .mrkdwn import parse
from .utils import standard_emojis


# TODO: customize by chat
@cache
def custom_emojis():
    return deli.load(settings.slack_root / 'emojis.json')


StyleStr = Literal['ordered', 'bullet', 'primary']
Style = dict


class ElementBase(NoExtra):
    style: Style | None = None

    def convert(self):
        dump = self.model_dump()
        if 'elements' in dump:
            dump['elements'] = [x.convert() for x in self.elements]
        return dump


class RichTextElement(ElementBase):
    type: Literal['rich_text_section', 'rich_text_preformatted', 'rich_text_quote']
    elements: list[Element]
    indent: int | None = None
    border: int | None = None
    offset: int | None = None


class RichTextList(ElementBase):
    type: Literal['rich_text_list']
    elements: list[Element]
    indent: int | None = None
    border: int | None = None
    offset: int | None = None
    style: StyleStr


class Text(ElementBase):
    type: Literal['text']
    text: str


class PlainText(ElementBase):
    type: Literal['plain_text']
    text: str
    emoji: bool


class Channel(ElementBase):
    type: Literal['channel']
    channel_id: str


class Mrkdwn(ElementBase):
    type: Literal['mrkdwn']
    text: str
    verbatim: bool

    def convert(self):
        return elements.RichTextElement(elements=list(parse(self.text)), type='rich_text_section')


class Emoji(ElementBase):
    type: Literal['emoji']
    name: str | None
    unicode: str | None = None
    skin_tone: int | None = None

    def convert(self):
        name = self.name
        return elements.Emoji(
            url=custom_emojis().get(name), unicode=self.unicode or standard_emojis().get(name), name=name,
            skin_tone=self.skin_tone,
        )


class Link(ElementBase):
    type: Literal['link']
    url: str
    text: str | None = None

    unsafe: bool | None = None


class Color(ElementBase):
    type: Literal['color']
    value: str


class Broadcast(ElementBase):
    type: Literal['broadcast']
    range: Literal['channel', 'here', 'everyone']


class User(ElementBase):
    type: Literal['user']
    user_id: str


class UserGroup(ElementBase):
    type: Literal['usergroup']
    usergroup_id: str


class Button(ElementBase):
    type: Literal['button']
    text: PlainText
    value: str | None = None
    action_id: str
    # url: str | None = None
    style: StyleStr | None = None
    # confirm: dict | None = None


type Element = Union[*ElementBase.__subclasses__()]
