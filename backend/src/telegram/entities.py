from typing import Literal, Union

from .utils import file_url
from .. import elements
from ..utils import NoExtra


MISSING_FILE = '(File not included. Change data exporting settings to download.)'
StoredFile = str


class PlainLike(NoExtra):
    type: Literal[
        'italic', 'phone', 'mention', 'cashtag', 'bank_card', 'underline',
        'plain', 'link', 'code', 'email', 'bold', 'hashtag', 'strikethrough', 'bot_command', 'spoiler',
    ]
    text: str

    def convert(self):
        assert type(self) is PlainLike, self
        text = self.text
        wrapped = elements.Text(text=text)

        match self.type:
            case 'link':
                return elements.Link(url=text)
            case 'mention':
                return elements.User(user_id=text)
            case 'bold':
                return elements.Bold(element=wrapped)
            case 'italic':
                return elements.Italic(element=wrapped)
            case 'strikethrough':
                return elements.Strike(element=wrapped, position='through')
            case 'underline':
                return elements.Strike(element=wrapped, position='under')
            case 'code':
                return elements.Code(element=wrapped, language=None)

        return wrapped


class BlockQuote(PlainLike):
    type: Literal['blockquote']
    collapsed: bool | None = None

    def convert(self):
        # TODO: collapsed
        return elements.Quote(element=elements.Text(text=self.text))


class Pre(PlainLike):
    type: Literal['pre']
    language: str

    def convert(self):
        return elements.Code(element=elements.Text(text=self.text), language=self.language)


class TextLink(PlainLike):
    type: Literal['text_link']
    href: str

    def convert(self):
        return elements.Link(url=self.href, element=elements.Text(text=self.text))


class MentionName(PlainLike):
    type: Literal['mention_name']
    user_id: int

    def convert(self):
        return elements.User(user_id=str(self.user_id), element=self.text)


class CustomEmoji(PlainLike):
    type: Literal['custom_emoji']
    document_id: StoredFile

    def convert(self):
        return elements.Emoji(name=None, url=file_url(self.document_id), skin_tone=None, unicode=self.text)


type TextEntity = Union[PlainLike, *PlainLike.__subclasses__()]
