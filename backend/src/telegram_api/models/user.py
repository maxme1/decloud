from __future__ import annotations

from typing import Literal

from ..utils import Subclasses, TypeDispatch
from .media import File, MiniThumbnail


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

    class UserNames(TypeDispatch):
        type_: Literal['usernames']
        active_usernames: list[str]
        disabled_usernames: list[str]
        editable_username: str

    type_: Literal['user']
    id: int
    first_name: str
    last_name: str
    usernames: UserNames | None = None
    profile_photo: ProfilePhoto | None = None
    type: Subclasses[UserTypeBase]
