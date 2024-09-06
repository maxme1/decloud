from typing import Literal, Union

from pydantic import BaseModel, Field, TypeAdapter

MISSING_FILE = '(File not included. Change data exporting settings to download.)'
StoredFile = str


class NoExtra(BaseModel, extra='forbid'):
    pass


class PlainLike(NoExtra):
    type: Literal[
        'italic', 'phone', 'mention', 'cashtag', 'bank_card', 'underline',
        'plain', 'link', 'code', 'email', 'bold', 'hashtag', 'strikethrough', 'bot_command', 'spoiler',
    ]
    text: str


class BlockQuote(PlainLike):
    type: Literal['blockquote']
    collapsed: bool | None = None


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


TextEntity = Union[PlainLike, *PlainLike.__subclasses__()]


class Location(NoExtra):
    latitude: float
    longitude: float


class Contact(NoExtra):
    phone_number: str
    first_name: str
    last_name: str


class PollAnswer(NoExtra):
    text: str
    voters: int
    chosen: bool


class Poll(NoExtra):
    question: str
    closed: bool
    total_voters: int
    answers: list[PollAnswer]


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
    reply_to_peer_id: str | None = None
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
    # audio
    performer: str | None = None
    title: str | None = None

    contact_information: Contact | None = None
    contact_vcard: StoredFile = None

    location_information: Location | None = None
    live_location_period_seconds: int | None = None
    place_name: str | None = None
    address: str | None = None

    inline_bot_buttons: list[list[BotButton]] | None = None

    poll: Poll | None = None


class Service(MessageBase):
    type: Literal['service']

    actor: str | None
    actor_id: str

    date: str
    date_unixtime: int


class PhoneCall(Service):
    action: Literal['phone_call']
    duration_seconds: int | None = None
    discard_reason: Literal['hangup', 'missed', 'busy', 'disconnect'] | None = None


class GroupCall(Service):
    action: Literal['group_call']


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


class RemoveMembers(Service):
    action: Literal['remove_members']
    members: list[str]


class JoinGroupByLink(Service):
    action: Literal['join_group_by_link']
    inviter: str


class EditGroupPhoto(Service):
    action: Literal['edit_group_photo']
    photo: StoredFile
    width: int
    height: int


class EditGroupTitle(Service):
    action: Literal['edit_group_title']
    title: str


class TopicCreated(Service):
    action: Literal['topic_created']
    title: str


class TopicEdit(Service):
    action: Literal['topic_edit']
    new_icon_emoji_id: int


class PinMessage(Service):
    action: Literal['pin_message']
    message_id: int


AnyMessage = TypeAdapter(Message | Union[*Service.__subclasses__()])
