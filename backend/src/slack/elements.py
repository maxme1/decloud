from __future__ import annotations

from typing import Literal, Union

from .. import elements
from ..utils import NoExtra, Maybe, split_into_segments
from .mrkdwn import convert_mrkdwn
from .utils import standard_emojis, to_unicode


StyleStr = Literal['ordered', 'bullet', 'primary']
Style = dict


def convert_elements(xs: list[Element], context) -> list[elements.Element]:
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
                    converted.extend(convert_elements(elt.elements, context))
                else:
                    converted.append(elt.convert(context))

            if len(converted) != 1:
                converted = elements.Sequence(elements=converted)
            else:
                converted = converted[0]
            result.append(elements.Quote(element=converted))
        else:
            result.extend(x.convert(context) for x in group)

    return result


class ElementBase(NoExtra):
    style: Maybe[Style]

    def convert(self, context):
        dump = self.model_dump()
        style = dump.pop('style', None) or {}
        assert isinstance(style, dict), (style, type(self))

        if 'elements' in dump:
            dump['elements'] = convert_elements(self.elements, context)

        dump = _apply_style(dump, style)
        return dump


def _apply_style(x, style):
    style = (style or {}).copy()
    if style.pop('code', None):
        x = elements.Code(element=x, language=None)
    if style.pop('bold', None):
        x = elements.Bold(element=x)
    if style.pop('strike', None):
        x = elements.Strike(element=x, position='through')
    if style.pop('italic', None):
        x = elements.Italic(element=x)
    # TODO: ???
    style.pop('unlink', None)
    assert not style, style
    return x


class RichTextElement(ElementBase):
    type: Literal['rich_text_section', 'rich_text_preformatted', 'rich_text_quote']
    elements: list[Element]
    indent: Maybe[int]
    border: Maybe[int]
    offset: Maybe[int]

    def convert(self, context):
        assert not self.style, self.style

        sequence = elements.Sequence(elements=convert_elements(self.elements, context))
        if self.type == 'rich_text_quote':
            assert not self.indent and not self.offset, (self.indent, self.offset)
            return elements.Quote(element=sequence)

        if self.type == 'rich_text_preformatted':
            assert not self.indent and not self.offset, (self.indent, self.offset)
            return elements.Code(element=sequence, language=None)

        assert self.type == 'rich_text_section', self.type
        assert not self.border, self.border
        assert not self.offset, self.offset
        assert not self.indent, self.indent
        return sequence


class RichTextList(ElementBase):
    type: Literal['rich_text_list']
    elements: list[Element]
    indent: Maybe[int]
    border: Maybe[int]
    offset: Maybe[int]
    style: StyleStr

    def convert(self, context):
        # assert not self.offset, (self.offset, self.elements)
        assert self.style in ('ordered', 'bullet'), self.style
        return elements.List(
            elements=[x.convert(context) for x in self.elements],
            style='ordered' if self.style == 'ordered' else 'unordered',
        )


class Text(ElementBase):
    type: Literal['text']
    text: str


class PlainText(ElementBase):
    type: Literal['plain_text']
    text: str
    emoji: bool

    def convert(self, context):
        # TODO: emoji?
        assert not self.style, self.style
        return elements.Text(text=self.text)


class Channel(ElementBase):
    type: Literal['channel']
    channel_id: str

    def convert(self, context):
        return _apply_style(elements.Channel(channel_id=self.channel_id, text=None), self.style)


class Mrkdwn(ElementBase):
    type: Literal['mrkdwn']
    text: str
    verbatim: bool

    def convert(self, context):
        assert not self.style, self.style
        return elements.Sequence(elements=convert_mrkdwn(self.text))


class Emoji(ElementBase):
    type: Literal['emoji']
    name: str | None
    unicode: Maybe[str]
    skin_tone: Maybe[int]
    # TODO: ???
    url: Maybe[str]
    display_url: Maybe[str]
    display_team_id: Maybe[str]

    def convert(self, context):
        # assert not self.style, self.style
        name = self.name
        return elements.Emoji(
            url=context.custom_emojis.get(name), unicode=to_unicode(self.unicode) or standard_emojis().get(name),
            name=name, skin_tone=self.skin_tone,
        )


class Link(ElementBase):
    type: Literal['link']
    url: str
    text: Maybe[str]

    unsafe: Maybe[bool]

    def convert(self, context):
        text = self.text
        if text is not None:
            text = elements.Text(text=text)
        return _apply_style(elements.Link(url=self.url, element=text), self.style)


class Image(ElementBase):
    type: Literal['image']
    image_url: str
    alt_text: Maybe[str]

    def convert(self, context):
        assert not self.style, self.style
        return elements.Image(url=context.get_file_url(self.image_url), name=self.alt_text)


class Color(ElementBase):
    type: Literal['color']
    value: str


class Broadcast(ElementBase):
    type: Literal['broadcast']
    range: Literal['channel', 'here', 'everyone']


class User(ElementBase):
    type: Literal['user']
    user_id: str

    def convert(self, context):
        return _apply_style(elements.User(user_id=self.user_id, element=None), self.style)


class UserGroup(ElementBase):
    type: Literal['usergroup']
    usergroup_id: str


class Button(ElementBase):
    type: Literal['button']
    text: PlainText
    value: Maybe[str]
    action_id: str
    url: Maybe[str]
    style: Maybe[StyleStr]
    confirm: Maybe[dict]

    def convert(self, context):
        dump = self.model_dump()
        dump['text'] = self.text.convert(context)
        return dump


type Element = Union[*ElementBase.__subclasses__()]
