from __future__ import annotations

import datetime
from typing import Literal

from ...schema import BaseSystemMessage, SystemEventType, Call
from ..utils import TypeDispatch
from .content import ContentBase
from .media import MiniThumbnail, PhotoSize


class SystemEvent:
    _event: str | None
    _event_class: type

    @property
    def event_class(self):
        return getattr(self, '_event_class', None) or BaseSystemMessage

    def convert(self, context):
        return

    def get_event(self) -> SystemEventType:
        return getattr(self, '_event', None) or self.type_

    def kwargs(self, message):
        return {}


class MessageCall(SystemEvent, ContentBase):
    class Reason(TypeDispatch):
        type_: Literal[
            'callDiscardReasonHungUp', 'callDiscardReasonMissed', 'callDiscardReasonDisconnected',
            'callDiscardReasonDeclined',
        ]

    type_: Literal['messageCall']
    is_video: bool
    duration: int
    discard_reason: Reason

    _event = 'call'
    _event_class = Call

    def kwargs(self, message):
        status = self.discard_reason.type_.removeprefix('callDiscardReason')
        if status == 'HungUp':
            status = 'hung_up'
        return dict(duration=self.duration, status=status.lower())


class ChatAddMembers(SystemEvent, ContentBase):
    type_: Literal['messageChatAddMembers']
    member_user_ids: list[int]

    _event = 'join'

    def kwargs(self, message):
        return dict(agents=self.member_user_ids)


class BasicGroupChatCreate(SystemEvent, ContentBase):
    type_: Literal['messageBasicGroupChatCreate']
    member_user_ids: list[int]
    title: str

    _event = 'create'

    def kwargs(self, message):
        return dict(agents=self.member_user_ids)


class SupergroupChatCreate(SystemEvent, ContentBase):
    type_: Literal['messageSupergroupChatCreate']
    title: str

    _event = 'create'


class ChatChangeTitle(SystemEvent, ContentBase):
    type_: Literal['messageChatChangeTitle']
    title: str


class ForumTopicCreated(SystemEvent, ContentBase):
    type_: Literal['messageForumTopicCreated']
    name: str
    icon: dict


class ForumTopicIsClosedToggled(SystemEvent, ContentBase):
    type_: Literal['messageForumTopicIsClosedToggled']
    is_closed: bool


class ChatChangePhoto(SystemEvent, ContentBase):
    class ChatPhoto(TypeDispatch):
        type_: Literal['chatPhoto']
        id: str
        sizes: list[PhotoSize]
        added_date: datetime.datetime
        minithumbnail: MiniThumbnail | None = None
        animation: dict | None = None
        small_animation: dict | None = None
        sticker: dict | None = None

    type_: Literal['messageChatChangePhoto']
    photo: ChatPhoto

    def get_files(self):
        return [size.photo for size in self.photo.sizes]


class ChatDeleteMember(SystemEvent, ContentBase):
    type_: Literal['messageChatDeleteMember']
    user_id: int

    _event = 'leave'

    def kwargs(self, message):
        return dict(agents=[self.user_id])


class ChatSetTheme(SystemEvent, ContentBase):
    type_: Literal['messageChatSetTheme']
    theme_name: str


class ChatUpgradeFrom(SystemEvent, ContentBase):
    type_: Literal['messageChatUpgradeFrom']
    basic_group_id: int
    title: str


class PinMessage(SystemEvent, ContentBase):
    type_: Literal['messagePinMessage']
    message_id: int


class VideoChatEnded(SystemEvent, ContentBase):
    type_: Literal['messageVideoChatEnded']
    duration: int


class InviteVideoChatParticipants(SystemEvent, ContentBase):
    type_: Literal['messageInviteVideoChatParticipants']
    group_call_id: int
    user_ids: list[int]


class JoinByLink(SystemEvent, ContentBase):
    type_: Literal['messageChatJoinByLink']

    _event = 'join'

    def kwargs(self, message):
        return dict(agents=[message.sender_id.user_id])


class SimpleEvent(SystemEvent, ContentBase):
    type_: Literal['messageContactRegistered', 'messageChatDeletePhoto']


class ChatBoost(SystemEvent, ContentBase):
    type_: Literal['messageChatBoost']
    boost_count: int
