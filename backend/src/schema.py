from __future__ import annotations

import datetime
from typing import Literal, Union

from .elements import EmojiBase, Element
from .utils import NoExtra


class AttachmentBase(NoExtra):
    pass


class RemovedAttachment(AttachmentBase):
    type: Literal['removed'] = 'removed'


class URLAttachment(AttachmentBase):
    type: Literal['image', 'other']
    url: str | None


type Attachment = Union[*AttachmentBase.__subclasses__()]


class Reaction(NoExtra):
    emoji: EmojiBase
    users: list[str]


class Base(NoExtra):
    type: str
    id: str
    timestamp: datetime.datetime
    thread: list[AnyMessage]
    elements: list[Element]
    reactions: list[Reaction]


class Agent(NoExtra):
    id: str
    name: str
    avatar: str | None
    is_bot: bool


class BaseSystemMessage(Base):
    type: Literal['system'] = 'system'
    event: Literal['join', 'leave', 'purpose', 'archive'] | str
    agents: list[str]


class Call(BaseSystemMessage):
    event: Literal['call'] = 'call'
    duration: float | None


class Shared(NoExtra):
    id: str | None
    agent_id: str | None
    channel_id: str | None

    timestamp: datetime.datetime | None
    elements: list[Element]


class AgentMessage(Base):
    type: Literal['agent'] = 'agent'

    agent_id: str | None
    edited: datetime.datetime | None

    shared: list[Shared]
    reply_to: list[str]


type SystemMessage = Union[BaseSystemMessage, *BaseSystemMessage.__subclasses__()]
type AnyMessage = AgentMessage | SystemMessage
