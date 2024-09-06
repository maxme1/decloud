from __future__ import annotations

from collections import defaultdict
from functools import partial
from typing import Literal, Union

from ... import elements
from ..utils import TypeDispatch, custom_emojis


class FormattedText(TypeDispatch):
    class Entity(TypeDispatch):
        type_: Literal['textEntity']
        offset: int
        length: int
        type: TextEntity

    type_: Literal['formattedText']
    text: str
    entities: list[Entity]

    def _dispatch(self, entity: TextEntity, element, start, stop):
        match entity:
            case TextEntitySimple(type_='textEntityTypeUrl'):
                return elements.Link(url=self.text[start:stop], element=element)
            case TextEntitySimple(type_=t):
                wrappers = {
                    'textEntityTypeBold': elements.Bold,
                    'textEntityTypeItalic': elements.Italic,
                    'textEntityTypeStrikethrough': partial(elements.Strike, position='through'),
                    'textEntityTypeUnderline': partial(elements.Strike, position='under'),
                    'textEntityTypeCode': elements.Preformat,
                    'textEntityTypeBlockQuote': elements.Quote,
                }
                if t in wrappers:
                    return wrappers[t](element=element)
                return element
            case TextEntityMentionName(user_id=user_id):
                return elements.User(user_id=str(user_id), element=element)
            case TextEntityCustomEmoji(custom_emoji_id=custom_emoji_id):
                # TODO
                # custom_emojis()[custom_emoji_id]
                return elements.Emoji(name=custom_emoji_id, url=None, skin_tone=None, unicode=None)
            case TextEntityTypeTextUrl(url=url):
                return elements.Link(url=url, element=element)
            case TextEntityTypePreCode(language=language):
                return elements.Code(element=element, language=language)
            case _:
                raise NotImplementedError(entity)

    def convert(self):
        # split into entities
        groups = defaultdict(list)
        for entity in self.entities:
            groups[entity.offset].append(entity)
        groups = sorted(groups.items())
        groups = [
            (offset, max(offset + x.length for x in entities), sorted(entities, key=lambda x: x.length))
            for offset, entities in groups
        ]
        # FIXME
        # validate
        for a, b in zip(groups, groups[1:]):
            assert a[1] <= b[0]

        start = 0
        parts = []
        for offset, end, entities in groups:
            prefix = self.text[start:offset]
            if prefix:
                parts.append(elements.Text(text=prefix))

            entity = entities[0]
            start = offset
            stop = offset + entity.length
            wrapped = self._dispatch(entity.type, elements.Text(text=self.text[start:stop]), start, stop)
            for entity in entities[1:]:
                if entity.offset != stop:
                    wrapped = elements.Sequence(elements=[
                        wrapped, elements.Text(text=self.text[stop:entity.offset]),
                    ])
                    stop = entity.offset
                wrapped = self._dispatch(entity.type, wrapped, start, stop)

            parts.append(wrapped)
            start = end

        if start < len(self.text):
            parts.append(elements.Text(text=self.text[start:]))

        return elements.Sequence.wrap(parts)


class TextEntityBase(TypeDispatch):
    pass


class TextEntitySimple(TextEntityBase):
    type_: Literal[
        'textEntityTypeBankCardNumber', 'textEntityTypeBold', 'textEntityTypeCashtag', 'textEntityTypeCode',
        'textEntityTypeEmailAddress', 'textEntityTypeHashtag', 'textEntityTypeItalic', 'textEntityTypeMention',
        'textEntityTypePhoneNumber', 'textEntityTypePre', 'textEntityTypeStrikethrough', 'textEntityTypeUnderline',
        'textEntityTypeUrl', 'textEntityTypeBlockQuote', 'textEntityTypeSpoiler', 'textEntityTypeExpandableBlockQuote',
        'textEntityTypeBotCommand',
    ]


class TextEntityMentionName(TextEntityBase):
    type_: Literal['textEntityTypeMentionName']
    user_id: int


class TextEntityCustomEmoji(TextEntityBase):
    type_: Literal['textEntityTypeCustomEmoji']
    custom_emoji_id: str


class TextEntityTypeTextUrl(TextEntityBase):
    type_: Literal['textEntityTypeTextUrl']
    url: str


class TextEntityTypePreCode(TextEntityBase):
    type_: Literal['textEntityTypePreCode']
    language: str


class TextEntityTypeMediaTimestamp(TextEntityBase):
    type_: Literal['textEntityTypeMediaTimestamp']
    media_timestamp: int


TextEntity = Union[*TextEntityBase.__subclasses__()]
