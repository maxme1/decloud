from __future__ import annotations

from typing import Iterable, Literal

from pydantic import BaseModel

from ... import elements
from ..utils import Subclasses, TypeDispatch
from .media import File, MiniThumbnail, PhotoSize, Sticker, Thumbnail
from .sender import Sender
from .text import FormattedText
from ...utils import Maybe


class ContentBase(TypeDispatch):
    type_: str

    def get_files(self) -> Iterable[File]:
        return []

    def get_user_ids(self) -> Iterable[int]:
        return []

    def convert(self, context):
        name = type(self).__name__
        if name not in _printed:
            _printed.add(name)
            print(name)
        return elements.Text(text=name)


_printed = set()


class MessageAnimatedEmoji(ContentBase):
    class AnimatedEmoji(TypeDispatch):
        type_: Literal['animatedEmoji']
        sticker: Sticker
        sticker_width: int
        sticker_height: int
        fitzpatrick_type: int
        sound: Maybe[File]

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
            url=context.get_file_url(self.animated_emoji.sticker.sticker),
            mimetype=self.animated_emoji.sticker.mimetype,
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
        album_cover_minithumbnail: Maybe[MiniThumbnail]
        album_cover_thumbnail: Maybe[Thumbnail]

    type_: Literal['messageAudio']
    audio: Audio
    caption: FormattedText

    def get_files(self):
        return [self.audio.audio]

    def convert(self, context):
        return elements.Sequence(elements=[
            elements.Audio(url=context.get_file_url(self.audio.audio), name=None, thumbnail=None),
            self.caption.convert(),
        ])


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
    class DiceStickers(TypeDispatch):
        type_: Literal['diceStickersRegular']
        sticker: Sticker

    type_: Literal['messageDice']
    initial_state: DiceStickers
    final_state: DiceStickers
    emoji: str
    value: int
    success_animation_frame_number: int

    def get_files(self):
        return [self.initial_state.sticker.sticker, self.final_state.sticker.sticker]

    def convert(self, context):
        return elements.Bold(element=elements.Text(text=f'Dice roll: {self.emoji} {self.value}'))


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

    def convert(self, context):
        return elements.Location(
            name=self.venue.title, address=self.venue.address,
            latitude=self.venue.location.latitude, longitude=self.venue.location.longitude,
        )


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
            url=context.get_file_url(self.sticker.sticker), mimetype=self.sticker.mimetype,
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
            url=context.get_file_url(self.video_note.video), name=None,
            thumbnail=context.get_file_url(self.video_note.thumbnail.file) if self.video_note.thumbnail else None,
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
            elements.Audio(url=context.get_file_url(self.voice_note.voice), name=None, thumbnail=None),
            self.caption.convert(),
        ])


class MessageDocument(ContentBase):
    class Document(TypeDispatch):
        type_: Literal['document']
        file_name: str
        mime_type: str
        minithumbnail: Maybe[MiniThumbnail]
        thumbnail: Maybe[Thumbnail]
        document: File

    type_: Literal['messageDocument']
    document: Document
    caption: FormattedText

    def get_files(self):
        return [self.document.document, *thumbnail(self.document.thumbnail)]

    def convert(self, context):
        return elements.File(
            url=context.get_file_url(self.document.document), name=self.document.file_name,
            mimetype=self.document.mime_type,
            thumbnail=context.get_file_url(self.document.thumbnail.file) if self.document.thumbnail else None,
        )


class MessageText(ContentBase):
    type_: Literal['messageText']
    text: Maybe[FormattedText]
    link_preview: Maybe[dict]
    link_preview_options: Maybe[dict]

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
        minithumbnail: Maybe[MiniThumbnail]
        sizes: list[PhotoSize]
        has_stickers: bool

    type_: Literal['messagePhoto']
    photo: Photo

    def get_files(self):
        return [size.photo for size in self.photo.sizes]

    def convert(self, context):
        element = elements.Image(
            url=context.get_file_url(max(self.photo.sizes, key=lambda x: x.photo.size).photo), name=None
        )
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
    minithumbnail: Maybe[MiniThumbnail]
    thumbnail: Maybe[Thumbnail]


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
            url=context.get_file_url(self.video.video), name=self.video.file_name,
            thumbnail=context.get_file_url(self.video.thumbnail.file) if self.video.thumbnail else None,
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
            element = elements.Image(url=context.get_file_url(self.animation.animation), name=self.animation.file_name)
        else:
            element = elements.Video(
                url=context.get_file_url(self.animation.animation), name=self.animation.file_name,
                thumbnail=context.get_file_url(self.animation.thumbnail.file) if self.animation.thumbnail else None,
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

    def convert(self, context):
        return elements.Section(element=elements.Sequence(elements=[
            elements.Header(element=self.poll.question.convert()),
            elements.List(elements=[option.text.convert() for option in self.poll.options], style='ordered'),
        ]))


def thumbnail(x):
    if x is not None:
        yield x.file
