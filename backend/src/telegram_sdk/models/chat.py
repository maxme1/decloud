from __future__ import annotations

from typing import Literal, Union

from ..utils import TypeDispatch


class Chat(TypeDispatch, extra='ignore'):
    class ChatTypeBase(TypeDispatch):
        pass

    class ChatTypePrivate(ChatTypeBase):
        type_: Literal['chatTypePrivate']
        user_id: int

    class ChatTypeSupergroup(ChatTypeBase):
        type_: Literal['chatTypeSupergroup']
        supergroup_id: int
        is_channel: bool

    class ChatTypeBasicGroup(ChatTypeBase, extra='ignore'):
        type_: Literal['chatTypeBasicGroup']

    type_: Literal['chat']
    id: int
    type: Union[*ChatTypeBase.__subclasses__()]
    title: str
    last_message: dict | None = None
