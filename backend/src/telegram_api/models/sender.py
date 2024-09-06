from __future__ import annotations

from typing import Literal

from ..utils import TypeDispatch


class SenderChat(TypeDispatch):
    type_: Literal['messageSenderChat']
    chat_id: int


class SenderUser(TypeDispatch):
    type_: Literal['messageSenderUser']
    user_id: int


Sender = SenderChat | SenderUser
