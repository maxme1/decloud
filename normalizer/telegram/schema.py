import json
from typing import Literal, Union

from pydantic import BaseModel, Field, TypeAdapter


MISSING_FILE = '(File not included. Change data exporting settings to download.)'
StoredFile = str


class NoExtra(BaseModel, extra='forbid'):
    pass


class PlainLike(NoExtra):
    type: Literal[
        'italic', 'phone', 'mention', 'cashtag', 'bank_card', 'underline', 'blockquote',
        'plain', 'link', 'code', 'email', 'bold', 'hashtag',
    ]
    text: str


class Pre(PlainLike):
    type: Literal['pre']
    language: str


class TextLink(PlainLike):
    type: Literal['text_link']
    href: str


class MentionName(PlainLike):
    type: Literal['mention_name']
    user_id: int


class CustomEmoji(PlainLike):
    type: Literal['custom_emoji']
    document_id: StoredFile


TextEntity = PlainLike | Pre | TextLink | MentionName | CustomEmoji


class Location(NoExtra):
    latitude: float
    longitude: float


class Contact(NoExtra):
    phone_number: str
    first_name: str
    last_name: str


class MessageBase(NoExtra):
    id: int

    text: str | list[str | TextEntity]
    text_entities: list[TextEntity]


class BotButton(NoExtra):
    type: Literal['url']
    text: str
    data: str


class Message(MessageBase):
    type: Literal['message']

    from_id: str
    from_: str = Field(alias='from')

    date: str
    date_unixtime: int

    edited: str | None = None
    edited_unixtime: int | None = None

    forwarded_from: str | None = None
    reply_to_message_id: int | None = None
    via_bot: str | None = None

    file: StoredFile | None = None
    file_name: str | None = None
    mime_type: str | None = None

    photo: StoredFile | None = None
    width: int | None = None
    height: int | None = None

    sticker_emoji: str | None = None
    thumbnail: StoredFile | None = None

    media_type: None | Literal[
        'sticker', 'animation', 'video_file', 'audio_file', 'video_message', 'voice_message'
    ] = None

    # animation
    duration_seconds: int | None = None

    contact_information: Contact | None = None
    contact_vcard: StoredFile = None

    location_information: Location | None = None
    live_location_period_seconds: int | None = None

    inline_bot_buttons: list[list[BotButton]] | None = None


class Service(MessageBase):
    type: Literal['service']

    actor: str
    actor_id: str

    date: str
    date_unixtime: int


class PhoneCall(Service):
    action: Literal['phone_call']
    duration_seconds: int | None = None
    discard_reason: Literal['hangup', 'missed', 'busy', 'disconnect'] | None = None


class EditChatTheme(Service):
    action: Literal['edit_chat_theme']
    emoticon: str


class CreateGroup(Service):
    action: Literal['create_group']
    title: str
    members: list[str]


class MigrateToSupergroup(Service):
    action: Literal['migrate_to_supergroup']


class MigrateFromGroup(Service):
    action: Literal['migrate_from_group']
    title: str


class InviteMembers(Service):
    action: Literal['invite_members']
    members: list[str]


class EditGroupPhoto(Service):
    action: Literal['edit_group_photo']
    photo: StoredFile
    width: int
    height: int


AnyMessage = TypeAdapter(Message | Union[*Service.__subclasses__()])

if __name__ == '__main__':
    print(json.dumps(AnyMessage.json_schema()))
