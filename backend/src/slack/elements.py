from __future__ import annotations

from functools import cache
from typing import Literal, Union

import deli

from .. import elements
from ..settings import settings
from ..utils import NoExtra, split_into_segments
from .mrkdwn import parse
from .utils import file_url, standard_emojis


# TODO: customize by chat
@cache
def custom_emojis():
    return deli.load(settings.slack_root / 'emojis.json')


StyleStr = Literal['ordered', 'bullet', 'primary']
Style = dict


def convert_elements(xs: list[Element]) -> list[elements.Element]:
    # it turns out that quotes are spread across multiple elements
    result = []
    for is_quote, group in split_into_segments(
            xs, lambda x: isinstance(x, (RichTextElement, RichTextList)) and (x.type == 'rich_text_quote' or x.border)
    ):
        if is_quote:
            converted = []
            for elt in group:
                # we don't want nested quotes
                if elt.type == 'rich_text_quote':
                    converted.extend(convert_elements(elt.elements))
                else:
                    converted.append(elt.convert())

            if len(converted) != 1:
                converted = elements.Sequence(elements=converted)
            else:
                converted = converted[0]
            result.append(elements.Quote(element=converted))
        else:
            result.extend(x.convert() for x in group)

    return result


class ElementBase(NoExtra):
    style: Style | None = None

    def convert(self):
        dump = self.model_dump()
        style = dump.pop('style', None) or {}

        if 'elements' in dump:
            dump['elements'] = convert_elements(self.elements)

        assert isinstance(style, dict), (style, type(self))

        if style.pop('code', None):
            dump = elements.Code(element=dump)
        if style.pop('bold', None):
            dump = elements.Bold(element=dump)
        if style.pop('strike', None):
            dump = elements.Strike(element=dump)
        if style.pop('italic', None):
            dump = elements.Italic(element=dump)
        # TODO: ???
        style.pop('unlink', None)

        assert not style, (style, type(self))
        return dump


class RichTextElement(ElementBase):
    type: Literal['rich_text_section', 'rich_text_preformatted', 'rich_text_quote']
    elements: list[Element]
    indent: int | None = None
    border: int | None = None
    offset: int | None = None

    def convert(self):
        assert not self.style, self.style

        sequence = elements.Sequence(elements=convert_elements(self.elements))
        if self.type == 'rich_text_quote':
            assert not self.indent and not self.offset, (self.indent, self.offset)
            return elements.Quote(element=sequence)

        if self.type == 'rich_text_preformatted':
            assert not self.indent and not self.offset, (self.indent, self.offset)
            return elements.Preformat(element=sequence, language=None)

        assert self.type == 'rich_text_section', self.type
        assert not self.border, self.border
        assert not self.offset, self.offset
        assert not self.indent, self.indent
        return elements.Section(element=sequence)


class RichTextList(ElementBase):
    type: Literal['rich_text_list']
    elements: list[Element]
    indent: int | None = None
    border: int | None = None
    offset: int | None = None
    style: StyleStr

    def convert(self):
        # assert not self.offset, (self.offset, self.elements)
        assert self.style in ('ordered', 'bullet'), self.style
        return elements.List(
            elements=convert_elements(self.elements),
            style='ordered' if self.style == 'ordered' else 'unordered',
        )


class Text(ElementBase):
    type: Literal['text']
    text: str

    # def convert(self):
    #     text = elements.Text(text=self.text)
    #
    #
    #     assert not style, style
    #     return text


class PlainText(ElementBase):
    type: Literal['plain_text']
    text: str
    emoji: bool

    def convert(self):
        # TODO: emoji?
        assert not self.style, self.style
        return elements.Text(text=self.text)


class Channel(ElementBase):
    type: Literal['channel']
    channel_id: str


class Mrkdwn(ElementBase):
    type: Literal['mrkdwn']
    text: str
    verbatim: bool

    def convert(self):
        assert not self.style, self.style
        return elements.Sequence(elements=list(parse(self.text)))


class Emoji(ElementBase):
    type: Literal['emoji']
    name: str | None
    unicode: str | None = None
    skin_tone: int | None = None
    # TODO: ???
    url: str | None = None
    display_url: str | None = None
    display_team_id: str | None = None

    def convert(self):
        # assert not self.style, self.style
        name = self.name
        return elements.Emoji(
            url=custom_emojis().get(name), unicode=self.unicode or standard_emojis().get(name),
            name=name, skin_tone=self.skin_tone,
        )


class Link(ElementBase):
    type: Literal['link']
    url: str
    text: str | None = None

    unsafe: bool | None = None


class Image(ElementBase):
    type: Literal['image']
    image_url: str
    alt_text: str | None = None

    def convert(self):
        assert not self.style, self.style
        return elements.Image(url=file_url(self.image_url))


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
    url: str | None = None
    style: StyleStr | None = None
    confirm: dict | None = None

    def convert(self):
        return self.model_dump()


type Element = Union[*ElementBase.__subclasses__()]
