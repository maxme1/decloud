import multimethod

from .schema import *
from .utils import file_url
from ..elements import *
from ..schema import AgentMessage, Shared, SystemMessage


@multimethod.multimethod
def convert(msg):
    raise NotImplementedError(type(msg))


@convert.register
def convert(msg: Message):
    elements = list(generate_blocks(msg)) + [x.convert() for x in msg.text_entities]
    shared = []
    if msg.forwarded_from:
        shared.append(Shared(elements=elements, id=None, agent_id=None, timestamp=None, channel_id=None))
        elements = []

    return AgentMessage(
        id=str(msg.id), timestamp=msg.date_unixtime, thread=[], elements=elements,
        reactions=[], reply_to=[], shared=shared, agent_id=msg.from_id, edited=msg.edited_unixtime,
    )


@convert.register
def convert(msg: Service):
    return msg.convert()


def generate_blocks(msg: Message):
    if msg.photo:
        yield Image(
            url=file_url(msg.photo)
        )

    thumbnail = file_url(msg.thumbnail)
    name = msg.file_name or msg.title or None
    match msg.media_type:
        case 'sticker':
            if msg.file.endswith('.tgs'):
                yield Image(
                    url=thumbnail, name=name,
                )
            else:
                yield Image(
                    url=file_url(msg.file), name=name,
                )

        case 'animation':
            if msg.mime_type == 'image/gif':
                yield Image(
                    url=file_url(msg.file), name=name,
                )
            else:
                # TODO: autoplay
                yield Video(
                    url=file_url(msg.file), thumbnail=thumbnail, name=name,
                )

        case 'video_file' | 'video_message':
            # TODO: thumbnail
            yield Video(
                url=file_url(msg.file), thumbnail=thumbnail, name=name,
            )

        case 'audio_file' | 'voice_message':
            yield Audio(
                url=file_url(msg.file), thumbnail=thumbnail, name=name,
            )

        case _ as mt:
            if mt:
                raise ValueError(f'Unknown media type: {mt}')
            if msg.file:
                yield File(
                    url=file_url(msg.file), name=name,
                    mimetype=msg.mime_type, thumbnail=thumbnail,
                )

    if msg.location_information:
        yield Text(text=f'{msg.location_information.latitude}, {msg.location_information.longitude}')

    if msg.contact_information:
        yield Contact(
            name=f'{msg.contact_information.first_name} {msg.contact_information.last_name}',
            phone=msg.contact_information.phone_number,
        )

    if msg.live_location_period_seconds is not None:
        yield Text(text=str(msg.live_location_period_seconds))
