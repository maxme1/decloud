from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, Field, TypeAdapter, model_validator

from ..utils import NoExtra
from .blocks import Block


TimeStr = str


class Reaction(NoExtra):
    name: str
    count: int
    users: list[str]


class Message(NoExtra):
    type: Literal['message']
    ts: TimeStr

    text: str
    reactions: list[Reaction] = Field(default_factory=list)


class AttachmentField(NoExtra):
    title: str | None = None
    value: str | None = None
    short: bool | None = None


class MessageBlock(BaseModel):
    class MBlocks(BaseModel):
        blocks: list[Block]

    message: MBlocks


# TODO: catch all the extras
class Attachment(BaseModel):
    author_icon: str | None = None
    author_link: str | None = None
    author_name: str | None = None
    author_subname: str | None = None
    author_id: str | None = None

    bot_id: str | None = None

    channel_id: str | None = None

    is_msg_unfurl: bool | None = None
    is_share: bool | None = None
    is_reply_unfurl: bool | None = None
    is_thread_root_unfurl: bool | None = None
    is_app_unfurl: bool | None = None
    is_animated: bool | None = None

    files: list[dict] = Field(default_factory=list)

    fallback: str | None = None
    fields: list[AttachmentField] = Field(default_factory=list)
    footer: str | None = None
    footer_icon: str | None = None

    image_url: str | None = None
    image_width: int | None = None
    image_height: int | None = None
    image_bytes: int | None = None

    video_html: str | None = None
    video_html_width: int | None = None
    video_html_height: int | None = None

    mrkdwn_in: list[str] = Field(default_factory=list)
    pretext: str | None = None
    text: str | None = None
    thumb_url: str | None = None
    thumb_width: int | None = None
    thumb_height: int | None = None
    title: str | None = None
    title_link: str | None = None
    ts: TimeStr | int | None = None
    id: int | None = None

    service_name: str | None = None
    service_icon: str | None = None
    service_url: str | None = None

    app_unfurl_url: str | None = None
    app_id: str | None = None

    from_url: str | None = None
    original_url: str | None = None

    blocks: list[dict] = Field(default_factory=list)
    message_blocks: list[MessageBlock] = Field(default_factory=list)
    color: str | None = None


class ThreadMixin(NoExtra):
    attachments: list[Attachment] = Field(default_factory=list)
    thread_ts: TimeStr | None = None
    replies: list[AnyMessageType] = Field(default_factory=list)
    reply_count: int | None = None
    reply_users_count: int | None = None
    latest_reply: TimeStr | None = None
    reply_users: list[str] | None = None
    is_locked: bool | None = None
    subscribed: bool | None = None
    last_read: TimeStr | None = None
    edited: dict | None = None
    blocks: list[Block] = Field(default_factory=list)
    saved: dict | None = None
    client_msg_id: str | None = None
    parent_user_id: str | None = None

    bot_id: str | None = None
    app_id: str | None = None

    pinned_to: list[str] | None = None
    pinned_info: dict | None = None

    # slackbot?
    channel: str | None = None
    no_notifications: bool | None = None
    permalink: str | None = None
    room: dict | None = None


class Agent(NoExtra):
    user: str | None = None
    team: str | None = None


class FileTombstone(NoExtra):
    mode: Literal['tombstone']
    id: str


class CommonFields(BaseModel):
    id: str
    file_access: Literal['access_denied', 'visible']
    timestamp: int
    created: int
    user: str


class FileExternal(CommonFields, BaseModel):
    mode: Literal['external']

    name: str
    title: str
    mimetype: str
    filetype: str
    pretty_type: str
    editable: bool
    size: int
    is_external: bool
    external_type: str
    is_public: bool
    public_url_shared: bool
    display_as_bot: bool
    username: str
    url_private: str
    permalink: str
    is_starred: bool
    user_team: str
    has_rich_preview: bool


class FileInternal(CommonFields, BaseModel):
    mode: Literal['snippet', 'hosted', 'quip', 'email']

    name: str
    title: str
    mimetype: str
    filetype: str
    pretty_type: str
    editable: bool
    size: int
    is_external: bool
    external_type: str
    is_public: bool
    public_url_shared: bool
    display_as_bot: bool
    username: str
    url_private: str
    url_private_download: str
    permalink: str
    permalink_public: str
    is_starred: bool
    user_team: str
    has_rich_preview: bool


class UnknownFile(CommonFields, BaseModel):
    pass

    # @model_validator(mode='before')
    # def _p(cls, values):
    #     print(values)
    #     return values


type File = FileTombstone | FileExternal | FileInternal | UnknownFile


class UserMessage(Message, ThreadMixin, Agent):
    user_team: str | None = None
    source_team: str | None = None
    user_profile: dict | None = None

    #
    files: list[File] = Field(default_factory=list)
    upload: bool | None = None
    upload_reply_to: str | None = None
    display_as_bot: bool | None = None

    x_files: list[str] = Field(default_factory=list)

    # ???
    bot_profile: dict | None = None


class BotMessage(Message, ThreadMixin, Agent):
    subtype: Literal['bot_message']
    username: str | None = None
    icons: dict = Field(default_factory=dict)


class EventMessage(Message):
    user: str
    subtype: str
    team: str | None = None


class ChannelJoin(EventMessage):
    subtype: Literal['channel_join']
    team: str | None = None
    inviter: str | None = None


class ChannelLeave(EventMessage):
    subtype: Literal['channel_leave']


class ChannelName(EventMessage):
    subtype: Literal['channel_name']
    old_name: str
    name: str


class ChannelTopic(EventMessage):
    subtype: Literal['channel_topic']
    topic: str


class ChannelPurpose(EventMessage):
    subtype: Literal['channel_purpose']
    purpose: str


class GroupPurpose(EventMessage):
    subtype: Literal['group_purpose']
    purpose: str


class GroupJoin(EventMessage):
    subtype: Literal['group_join']


class ChannelArchive(EventMessage):
    subtype: Literal['channel_archive']


class ChannelUnarchive(EventMessage):
    subtype: Literal['channel_unarchive']


class ReminderAdd(EventMessage):
    subtype: Literal['reminder_add']


class FileMixin(NoExtra):
    is_intro: bool | None = None
    file: dict | None = None
    files: list[File] = Field(default_factory=list)
    team: str | None = None

    attachments: list[dict] = Field(default_factory=list)
    blocks: list[Block] = Field(default_factory=list)


class PinnedItem(EventMessage, FileMixin):
    subtype: Literal['pinned_item']
    item_type: Literal['C', 'F']
    item: dict | None = None
    comment: str | None = None


class BotEvent(EventMessage):
    subtype: Literal['bot_add', 'bot_disable', 'bot_remove', 'bot_enable']
    bot_id: str
    bot_link: str | None = None


class FileComment(EventMessage, FileMixin):
    subtype: Literal['file_comment']
    comment: dict
    user: str | None = None
    edited: dict | None = None


class AppConversationJoin(EventMessage):
    subtype: Literal['app_conversation_join']
    inviter: str


class ThreadBroadcast(EventMessage, ThreadMixin):
    subtype: Literal['thread_broadcast']
    root: dict | None = None
    thread_ts: TimeStr | None = None
    user: str | None = None

    files: list[File] = Field(default_factory=list)
    x_files: list[str] = Field(default_factory=list)
    upload: bool | None = None
    display_as_bot: bool | None = None


class ReplyBroadcast(EventMessage):
    # deprecated
    subtype: Literal['reply_broadcast']
    attachments: list[dict]


class HuddleThread(EventMessage, ThreadMixin):
    subtype: Literal['huddle_thread']


# TODO
class Tombstone(EventMessage, Message, ThreadMixin, extra='ignore'):
    subtype: Literal['tombstone']
    hidden: bool


class ShRoomCreated(EventMessage):
    subtype: Literal['sh_room_created']

    channel: str
    no_notifications: bool
    permalink: str
    room: dict
    team: str | None = None


class ChannelCanvasUpdated(EventMessage, extra='ignore'):
    subtype: Literal['channel_canvas_updated']


MessageTypes = {*Message.__subclasses__(), *ThreadMixin.__subclasses__(), *EventMessage.__subclasses__()} - {
    ThreadMixin, EventMessage}

type AnyMessageType = Union[*MessageTypes]

AnyMessage = TypeAdapter(Union[*MessageTypes])
