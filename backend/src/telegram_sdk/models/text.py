from __future__ import annotations

from functools import partial
from typing import Literal, Union

from ... import elements
from ..utils import TypeDispatch


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
                    'textEntityTypePre': partial(elements.Code, language=None),
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
            case TextEntityTypeMediaTimestamp(media_timestamp=media_timestamp):
                # TODO
                return element
            case _:
                raise NotImplementedError(entity, self.text)

    def convert(self):
        # group nested entities
        groups = []
        for entity in sorted(self.entities, key=lambda x: -x.length):
            entity_start, entity_stop = entity.offset, entity.offset + entity.length
            for group in groups:
                start, stop = group[:2]
                if start <= entity_start < stop or start < entity_stop <= stop:
                    if start <= entity_start and entity_stop <= stop:
                        group[0] = entity_start
                        group[1] = entity_stop
                        group[2].append(entity)
                        break
                    else:
                        raise ValueError('overlapping entities', entity, group)

            else:
                groups.append([entity_start, entity_stop, [entity]])

        # merge the groups
        merged = []
        for _, _, group in sorted(groups, key=lambda x: x[0]):
            group = group[::-1]
            entity = group[0]
            start, stop = entity.offset, entity.offset + entity.length

            wrapped = self._dispatch(entity.type, elements.Text(text=self.text[start:stop]), start, stop)
            for entity in group[1:]:
                begin, end = entity.offset, entity.offset + entity.length
                pieces = []
                if begin != start:
                    pieces.append(elements.Text(text=self.text[start:begin]))
                pieces.append(wrapped)
                if end != stop:
                    pieces.append(elements.Text(text=self.text[end:stop]))

                wrapped = elements.Sequence.wrap(pieces)
                wrapped = self._dispatch(entity.type, wrapped, begin, end)
                start, stop = begin, end

            merged.append((start, stop, wrapped))

        # deal with text in between
        start, parts = 0, []
        for begin, end, entity in merged:
            prefix = self.text[start:begin]
            if prefix:
                parts.append(elements.Text(text=prefix))

            parts.append(entity)
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
