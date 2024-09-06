from __future__ import annotations

import datetime
from typing import Literal, Union

from .blocks import Block
from .elements import EmojiBase
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
    blocks: list[Block]
    reactions: list[Reaction]


class Agent(NoExtra):
    id: str
    name: str
    avatar: str | None
    is_bot: bool


class SystemMessage(Base):
    type: Literal['system'] = 'system'
    event: Literal['call', 'join', 'leave'] | str
    agents: list[str]


class Shared(NoExtra):
    message: AnyMessage
    channel_id: str


class AgentMessage(Base):
    type: Literal['agent'] = 'agent'

    agent_id: str | None

    shared: list[Shared]
    reply_to: list[str]


type AnyMessage = AgentMessage | SystemMessage
