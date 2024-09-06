from __future__ import annotations

from typing import Iterable, Literal

from pydantic import BaseModel

from ... import elements
from ..utils import Subclasses, TypeDispatch
from .media import File, MiniThumbnail, PhotoSize, Sticker, Thumbnail, file_url
from .sender import Sender
from .text import FormattedText


class ContentBase(TypeDispatch):
    type_: str

    def get_files(self) -> Iterable[File]:
        return []

    def convert(self, context):
        print(type(self).__name__)
        return elements.Text(text=type(self).__name__)


class MessageAnimatedEmoji(ContentBase):
    class AnimatedEmoji(TypeDispatch):
        type_: Literal['animatedEmoji']
        sticker: Sticker
        sticker_width: int
        sticker_height: int
        fitzpatrick_type: int
        sound: File | None = None

    type_: Literal['messageAnimatedEmoji']
    animated_emoji: AnimatedEmoji
    emoji: str

    def get_files(self):
        yield self.animated_emoji.sticker.sticker
        if self.animated_emoji.sound:
            yield self.animated_emoji.sound

    def convert(self, context):
        return elements.Sticker(
            emoji=elements.Emoji(unicode=self.emoji, name=None, skin_tone=None, url=None),
            url=file_url(self.animated_emoji.sticker.sticker), mimetype=self.animated_emoji.sticker.mimetype,
        )


class MessageAudio(ContentBase):
    class Audio(TypeDispatch):
        type_: Literal['audio']
        duration: int
        title: str
        performer: str
        file_name: str
        mime_type: str
        external_album_covers: list[dict]
        audio: File
        album_cover_minithumbnail: MiniThumbnail | None = None
        album_cover_thumbnail: Thumbnail | None = None

    type_: Literal['messageAudio']
    audio: Audio
    caption: FormattedText

    def get_files(self):
        return [self.audio.audio]

    def convert(self, context):
        return elements.Sequence(elements=[
            elements.Audio(url=file_url(self.audio.audio), name=None, thumbnail=None),
            self.caption.convert(),
        ])


class MessageCall(ContentBase):
    class Reason(TypeDispatch):
        type_: Literal[
            'callDiscardReasonHungUp', 'callDiscardReasonMissed', 'callDiscardReasonDisconnected',
            'callDiscardReasonDeclined',
        ]

    type_: Literal['messageCall']
    is_video: bool
    duration: int
    discard_reason: Reason

    def convert(self, context):
        return elements.CallElement()


class MessageContact(ContentBase):
    class Contact(TypeDispatch):
        type_: Literal['contact']
        phone_number: str
        first_name: str
        last_name: str
        vcard: str
        user_id: int

    type_: Literal['messageContact']
    contact: Contact

    def convert(self, context):
        return elements.Contact(
            name=f'{self.contact.first_name} {self.contact.last_name}',
            phone=self.contact.phone_number,
        )


class MessageDice(ContentBase):
    type_: Literal['messageDice']
    initial_state: dict
    final_state: dict
    emoji: str
    value: int
    success_animation_frame_number: int


class MessageVenue(ContentBase):
    class Venue(TypeDispatch):
        type_: Literal['venue']
        location: Location
        title: str
        address: str
        provider: str
        id: str
        type: str

    type_: Literal['messageVenue']
    venue: Venue


class Location(TypeDispatch):
    type_: Literal['location']
    latitude: float
    longitude: float
    horizontal_accuracy: float


class MessageLocation(ContentBase):
    type_: Literal['messageLocation']
    location: Location
    live_period: int
    expires_in: int
    heading: int
    proximity_alert_radius: int

    def convert(self, context):
        return elements.Location(
            name=None, address=None,
            latitude=self.location.latitude, longitude=self.location.longitude,
        )


class MessageSticker(ContentBase):
    type_: Literal['messageSticker']
    sticker: Sticker
    is_premium: bool

    def get_files(self):
        return [self.sticker.sticker]

    def convert(self, context):
        return elements.Sticker(
            emoji=elements.Emoji(unicode=self.sticker.emoji, name=None, skin_tone=None, url=None),
            url=file_url(self.sticker.sticker), mimetype=self.sticker.mimetype,
        )


class MessageVideoNote(ContentBase):
    class VideoNote(TypeDispatch):
        type_: Literal['videoNote']
        duration: int
        length: int
        minithumbnail: MiniThumbnail
        thumbnail: Thumbnail
        waveform: str
        video: File

    type_: Literal['messageVideoNote']
    video_note: VideoNote
    is_secret: bool
    is_viewed: bool

    def get_files(self):
        return [self.video_note.video, *thumbnail(self.video_note.thumbnail)]

    def convert(self, context):
        return elements.Video(
            url=file_url(self.video_note.video), name=None,
            thumbnail=file_url(self.video_note.thumbnail.file) if self.video_note.thumbnail else None,
            size=self.video_note.video.size,
        )


class MessageVoiceNote(ContentBase):
    class VoiceNote(TypeDispatch):
        type_: Literal['voiceNote']
        duration: int
        waveform: str
        mime_type: str
        voice: File

    type_: Literal['messageVoiceNote']
    voice_note: VoiceNote
    caption: FormattedText
    is_listened: bool

    def get_files(self):
        return [self.voice_note.voice]

    def convert(self, context):
        return elements.Sequence(elements=[
            elements.Audio(url=file_url(self.voice_note.voice), name=None, thumbnail=None),
            self.caption.convert(),
        ])


class MessageDocument(ContentBase):
    class Document(TypeDispatch):
        type_: Literal['document']
        file_name: str
        mime_type: str
        minithumbnail: MiniThumbnail | None = None
        thumbnail: Thumbnail | None = None
        document: File

    type_: Literal['messageDocument']
    document: Document
    caption: FormattedText

    def get_files(self):
        return [self.document.document, *thumbnail(self.document.thumbnail)]

    def convert(self, context):
        return elements.File(
            url=file_url(self.document.document), name=self.document.file_name, mimetype=self.document.mime_type,
            thumbnail=file_url(self.document.thumbnail.file) if self.document.thumbnail else None,
        )


class MessageVideoChatStarted(ContentBase):
    type_: Literal['messageVideoChatStarted']
    group_call_id: int


class MessageText(ContentBase):
    type_: Literal['messageText']
    text: FormattedText | None = None
    link_preview: dict | None = None
    link_preview_options: dict | None = None

    def convert(self, context):
        return self.text.convert()


# media
class MediaMixin(BaseModel):
    caption: FormattedText
    show_caption_above_media: bool
    has_spoiler: bool
    is_secret: bool


class MessagePhoto(ContentBase, MediaMixin):
    class Photo(TypeDispatch):
        type_: Literal['photo']
        minithumbnail: MiniThumbnail | None = None
        sizes: list[PhotoSize]
        has_stickers: bool

    type_: Literal['messagePhoto']
    photo: Photo

    def get_files(self):
        return [size.photo for size in self.photo.sizes]

    def convert(self, context):
        element = elements.Image(url=file_url(max(self.photo.sizes, key=lambda x: x.photo.size).photo), name=None)
        if self.caption:
            return elements.Sequence(elements=[element, self.caption.convert()])
        return element


class MediaMessageMixin(BaseModel):
    duration: int
    width: int
    height: int
    file_name: str
    mime_type: str
    has_stickers: bool
    minithumbnail: MiniThumbnail | None = None
    thumbnail: Thumbnail | None = None


class MessageVideo(ContentBase, MediaMixin):
    class Video(TypeDispatch, MediaMessageMixin):
        type_: Literal['video']
        video: File
        supports_streaming: bool

    type_: Literal['messageVideo']
    video: Video

    def get_files(self):
        return [self.video.video, *thumbnail(self.video.thumbnail)]

    def convert(self, context):
        element = elements.Video(
            url=file_url(self.video.video), name=self.video.file_name,
            thumbnail=file_url(self.video.thumbnail.file) if self.video.thumbnail else None,
            size=self.video.video.size,
        )
        if self.caption:
            return elements.Sequence(elements=[element, self.caption.convert()])
        return element


class MessageAnimation(ContentBase, MediaMixin):
    class Animation(TypeDispatch, MediaMessageMixin):
        type_: Literal['animation']
        animation: File

    type_: Literal['messageAnimation']
    animation: Animation

    def get_files(self):
        return [self.animation.animation, *thumbnail(self.animation.thumbnail)]

    def convert(self, context):
        kind = self.animation.mime_type
        if kind == 'image/gif':
            element = elements.Image(url=file_url(self.animation.animation), name=self.animation.file_name)
        else:
            element = elements.Video(
                url=file_url(self.animation.animation), name=self.animation.file_name,
                thumbnail=file_url(self.animation.thumbnail.file) if self.animation.thumbnail else None,
                size=self.animation.animation.size,
            )

        if self.caption:
            return elements.Sequence(elements=[element, self.caption.convert()])
        return element


class MessagePoll(ContentBase):
    class Poll(TypeDispatch):
        class PollOption(TypeDispatch):
            type_: Literal['pollOption']
            text: FormattedText
            voter_count: int
            is_chosen: bool
            is_being_chosen: bool
            vote_percentage: int

        class PollType(TypeDispatch):
            pass

        class Regular(PollType):
            type_: Literal['pollTypeRegular']
            allow_multiple_answers: bool

        class Quiz(PollType):
            type_: Literal['pollTypeQuiz']
            explanation: FormattedText
            correct_option_id: int

        type_: Literal['poll']
        id: int
        question: FormattedText
        options: list[PollOption]
        total_voter_count: int
        recent_voter_ids: list[Sender]
        is_anonymous: bool
        type: Subclasses[PollType]
        close_date: int
        open_period: int
        is_closed: bool

    type_: Literal['messagePoll']
    poll: Poll


def thumbnail(x):
    if x is not None:
        yield x.file
