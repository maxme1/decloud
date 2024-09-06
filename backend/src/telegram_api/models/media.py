from __future__ import annotations

from typing import Literal

from ..utils import Subclasses, TypeDispatch


class Sticker(TypeDispatch):
    class Format(TypeDispatch):
        type_: Literal['stickerFormatWebp', 'stickerFormatWebm', 'stickerFormatTgs']

    class TypeBase(TypeDispatch):
        pass

    class Regular(TypeBase):
        type_: Literal['stickerFullTypeRegular']
        premium_animation: File | None = None

    class CustomEmoji(TypeBase):
        type_: Literal['stickerFullTypeCustomEmoji']
        custom_emoji_id: int
        needs_repainting: bool

    type_: Literal['sticker']
    id: int
    set_id: int
    width: int
    height: int
    emoji: str
    format: Format
    full_type: Subclasses[TypeBase]
    thumbnail: Thumbnail
    sticker: File
    outline: list

    @property
    def mimetype(self):
        return {
            'stickerFormatWebp': 'image/webp',
            'stickerFormatWebm': 'video/webm',
            'stickerFormatTgs': 'video/tgs',
        }[self.format.type_]


class Thumbnail(TypeDispatch):
    class Format(TypeDispatch):
        type_: Literal['thumbnailFormatJpeg', 'thumbnailFormatWebp', 'thumbnailFormatMpeg4']

    type_: Literal['thumbnail']
    format: Format
    width: int
    height: int
    file: File


class MiniThumbnail(TypeDispatch):
    type_: Literal['minithumbnail']
    width: int
    height: int
    data: bytes


class PhotoSize(TypeDispatch):
    type_: Literal['photoSize']
    type: Literal['m', 's', 'w', 'x', 'y', 'a', 'b', 'c']
    photo: File
    width: int
    height: int
    progressive_sizes: list[int]


class File(TypeDispatch):
    class RemoteFile(TypeDispatch):
        type_: Literal['remoteFile']
        id: str
        unique_id: str
        is_uploading_active: bool
        is_uploading_completed: bool
        uploaded_size: int

    class LocalFile(TypeDispatch):
        type_: Literal['localFile']
        path: str
        can_be_downloaded: bool
        can_be_deleted: bool
        is_downloading_active: bool
        is_downloading_completed: bool
        download_offset: int
        downloaded_prefix_size: int
        downloaded_size: int

    type_: Literal['file']
    id: int
    size: int
    expected_size: int
    local: LocalFile
    remote: RemoteFile
