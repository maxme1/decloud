from __future__ import annotations

import datetime
from typing import Literal, Union

from .elements import Element, EmojiBase
from .utils import NoExtra


AgentID = str


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
    id: AgentID
    name: str
    avatar: str | None
    is_bot: bool


SystemEventType = Literal['topic', 'create', 'archive'] | str


class BaseSystemMessage(Base):
    type: Literal['system'] = 'system'
    event: SystemEventType
    agents: list[str]


class Call(BaseSystemMessage):
    event: Literal['call'] = 'call'
    duration: float | None
    status: Literal['missed', 'declined', 'hung_up', 'disconnected'] | None


class Join(BaseSystemMessage):
    event: Literal['join'] = 'join'
    by: AgentID | None


class Leave(BaseSystemMessage):
    event: Literal['leave'] = 'leave'
    by: AgentID | None


class Rename(BaseSystemMessage):
    event: Literal['rename'] = 'rename'
    name: str


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


type SystemMessage = Union[BaseSystemMessage, *BaseSystemMessage.__subclasses__()]
type AnyMessage = AgentMessage | SystemMessage
