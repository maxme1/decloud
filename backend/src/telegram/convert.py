import multimethod

from ..elements import *
from ..schema import AgentMessage, Shared
from ..settings import settings
from .schema import *


@multimethod.multimethod
def convert(msg, context):
    raise NotImplementedError(type(msg))


@convert.register
def convert(msg: Message, context):
    elements = list(generate_blocks(msg, context)) + [x.convert(context) for x in msg.text_entities]
    shared = []
    if msg.forwarded_from:
        shared.append(Shared(elements=elements, id=None, agent_id=None, timestamp=None, channel_id=None))
        elements = []

    return AgentMessage(
        id=str(msg.id), timestamp=msg.date_unixtime, thread=[], elements=elements,
        reactions=[], reply_to=[], shared=shared, agent_id=msg.from_id, edited=msg.edited_unixtime,
    )


@convert.register
def convert(msg: Service, context):
    return msg.convert(context)


def generate_blocks(msg: Message, context):
    name = msg.file_name or msg.title or None
    if msg.photo:
        yield Image(
            url=context.get_context.get_file_url(msg.photo), name=name,
        )

    thumbnail = context.get_file_url(msg.thumbnail)
    url = context.get_file_url(msg.file)
    match msg.media_type:
        case 'sticker':
            if msg.file.endswith('.tgs'):
                yield Image(url=thumbnail, name=name)
            else:
                yield Image(url=url, name=name)

        case 'animation':
            if msg.mime_type == 'image/gif':
                yield Image(url=url, name=name)
            else:
                yield Video(
                    url=url, thumbnail=thumbnail, name=name,
                    size=None if url is None else (settings.telegram_root / msg.file).stat().st_size,
                )

        case 'video_file' | 'video_message':
            yield Video(
                url=url, thumbnail=thumbnail, name=name,
                size=None if url is None else (settings.telegram_root / msg.file).stat().st_size,
            )

        case 'audio_file' | 'voice_message':
            yield Audio(
                url=url, thumbnail=thumbnail, name=name,
            )

        case _ as mt:
            if mt:
                raise ValueError(f'Unknown media type: {mt}')
            if msg.file:
                yield File(
                    url=url, name=name,
                    mimetype=msg.mime_type, thumbnail=thumbnail,
                )

    if msg.location_information or msg.place_name or msg.address:
        yield Location(
            name=msg.place_name, address=msg.address,
            latitude=msg.location_information.latitude, longitude=msg.location_information.longitude,
        )

    if msg.contact_information:
        yield Contact(
            name=f'{msg.contact_information.first_name} {msg.contact_information.last_name}',
            phone=msg.contact_information.phone_number,
        )
