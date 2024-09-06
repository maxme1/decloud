from __future__ import annotations

from typing import Literal, Union

from .media import File, MiniThumbnail
from ..utils import TypeDispatch


class User(TypeDispatch, extra='ignore'):
    class UserTypeBase(TypeDispatch):
        pass

    class RegularUser(UserTypeBase):
        type_: Literal['userTypeRegular']

    class DeletedUser(UserTypeBase):
        type_: Literal['userTypeDeleted']

    class BotUser(UserTypeBase, extra='ignore'):
        type_: Literal['userTypeBot']

    class ProfilePhoto(TypeDispatch):
        type_: Literal['profilePhoto']
        id: int
        has_animation: bool
        is_personal: bool
        small: File
        big: File
        minithumbnail: MiniThumbnail

    type_: Literal['user']
    id: int
    first_name: str
    last_name: str
    usernames: dict | None = None
    profile_photo: ProfilePhoto | None = None
    type: Union[*UserTypeBase.__subclasses__()]
