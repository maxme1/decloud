from __future__ import annotations

import datetime
from typing import Literal

from ..utils import FlaggedTimestamp, Subclasses, TypeDispatch
from .media import File, MiniThumbnail


class User(TypeDispatch):
    class UserTypeBase(TypeDispatch):
        pass

    class RegularUser(UserTypeBase):
        type_: Literal['userTypeRegular']

    class DeletedUser(UserTypeBase):
        type_: Literal['userTypeDeleted']

    class BotUser(UserTypeBase):
        type_: Literal['userTypeBot']
        can_be_edited: bool
        can_be_added_to_attachment_menu: bool
        has_main_web_app: bool
        can_join_groups: bool
        can_read_all_group_messages: bool
        is_inline: bool
        inline_query_placeholder: str
        need_location: bool
        can_connect_to_business: bool
        active_user_count: int

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

    class UserStatusBase(TypeDispatch):
        pass

    class Recently(UserStatusBase):
        type_: Literal['userStatusRecently', 'userStatusLastWeek', 'userStatusLastMonth']
        by_my_privacy_settings: bool

    class Offline(UserStatusBase):
        type_: Literal['userStatusOffline']
        was_online: datetime.datetime

    class Online(UserStatusBase):
        type_: Literal['userStatusOnline']
        expires: datetime.datetime

    class Empty(UserStatusBase):
        type_: Literal['userStatusEmpty']

    class EmojiStatus(TypeDispatch):
        type_: Literal['emojiStatus']
        expiration_date: FlaggedTimestamp
        custom_emoji_id: int

    type_: Literal['user']
    id: int
    type: Subclasses[UserTypeBase]
    status: Subclasses[UserStatusBase]
    first_name: str
    last_name: str
    phone_number: str
    usernames: UserNames | None = None
    profile_photo: ProfilePhoto | None = None
    emoji_status: EmojiStatus | None = None

    accent_color_id: int
    background_custom_emoji_id: str
    profile_accent_color_id: int
    profile_background_custom_emoji_id: str
    is_contact: bool
    is_mutual_contact: bool
    is_close_friend: bool
    is_verified: bool
    is_premium: bool
    is_support: bool
    restriction_reason: str
    is_scam: bool
    is_fake: bool
    has_active_stories: bool
    has_unread_active_stories: bool
    restricts_new_chats: bool
    have_access: bool
    language_code: str
    added_to_attachment_menu: bool
