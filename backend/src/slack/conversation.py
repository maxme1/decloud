import datetime
from typing import Union

from pydantic import Field, TypeAdapter

from ..utils import NoExtra, Maybe


class ConversationBase(NoExtra):
    id: str


class Channel(ConversationBase):
    name: str
    name_normalized: str

    previous_names: list[str] = Field(default_factory=list)
    pending_shared: list[str] = Field(default_factory=list)
    shared_team_ids: list[str] = Field(default_factory=list)
    pending_connected_team_ids: list
    context_team_id: str
    frozen_reason: Maybe[str]
    conversation_host_id: Maybe[str]
    purpose: dict
    properties: Maybe[dict]
    topic: dict
    created: datetime.datetime
    updated: datetime.datetime
    last_read: Maybe[datetime.datetime]
    unlinked: int
    creator: str
    parent_conversation: None
    num_members: Maybe[int]
    priority: Maybe[float]

    is_channel: bool
    is_group: bool
    is_im: bool
    is_mpim: bool
    is_private: bool
    is_archived: bool
    is_general: bool
    is_member: bool
    is_shared: bool
    is_org_shared: bool
    is_ext_shared: bool
    is_open: Maybe[bool]
    is_pending_ext_shared: Maybe[bool]
    is_pending_shared: Maybe[bool]


class Private(ConversationBase):
    user: str

    is_im: bool
    is_archived: bool
    is_user_deleted: bool
    is_shared: Maybe[bool]
    is_org_shared: bool
    is_ext_shared: Maybe[bool]

    priority: float
    context_team_id: str
    created: datetime.datetime
    updated: datetime.datetime
    properties: Maybe[dict]


Conversation = TypeAdapter(Union[*ConversationBase.__subclasses__()])
