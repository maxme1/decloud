import multimethod

from ..blocks import *
from ..elements import *
from ..schema import AgentMessage, SystemMessage
from .schema import *
from ..settings import settings


@multimethod.multimethod
def convert(msg):
    raise NotImplementedError(type(msg))


@convert.register
def convert(msg: Message):
    blocks = list(generate_blocks(msg))

    if msg.text_entities:
        blocks.append(RichText(elements=list(map(convert_element, msg.text_entities))))

    return AgentMessage(
        id=str(msg.id), timestamp=msg.date_unixtime, thread=[], blocks=blocks,
        reactions=[], reply_to=[], shared=[],
        agent_id=msg.from_id,
    )


@convert.register
def convert(msg: Service):
    return SystemMessage(
        id=str(msg.id), timestamp=msg.date_unixtime, thread=[], blocks=[], reactions=[],
        event=type(msg).__name__, agents=[msg.actor_id],
    )


def file_url(x: str) -> str | None:
    if x is None or x == MISSING_FILE:
        return None
    return f'{settings.base_url}/files/telegram/' + x.removeprefix('storage/')


@multimethod.multimethod
def convert_element(entity):
    raise NotImplementedError(type(entity), entity)


@convert_element.register
def convert_element(entity: Pre):
    return Preformat(element=Text(text=entity.text), language=entity.language)


@convert_element.register
def convert_element(entity: TextLink):
    return Link(url=entity.href, text=entity.text)


@convert_element.register
def convert_element(entity: MentionName):
    # TODO: entity.text
    return User(user_id=str(entity.user_id))


@convert_element.register
def convert_element(entity: CustomEmoji):
    assert not entity.text, entity.text
    return Emoji(name=entity.text, url=file_url(entity.document_id))


@convert_element.register
def convert_element(entity: BlockQuote):
    # TODO: collapsed
    return Quote(element=Text(text=entity.text))


@convert_element.register
def convert_element(entity: PlainLike):
    assert type(entity) is PlainLike, entity
    text = entity.text

    match entity.type:
        case 'link':
            return Link(url=text)
        case 'mention':
            return User(user_id=text)

    return Text(text=text)


def generate_blocks(msg: Message):
    def image(**kwargs):
        return RichText(elements=[Image(**kwargs)])

    if msg.photo:
        yield image(
            url=file_url(msg.photo)
        )

    match msg.media_type:
        case 'sticker':
            if msg.file.endswith('.tgs'):
                yield image(
                    url=file_url(msg.thumbnail)
                )
            else:
                yield image(
                    url=file_url(msg.file)
                )

        case 'animation':
            if msg.mime_type == 'image/gif':
                yield image(
                    url=file_url(msg.file)
                )
            else:
                # TODO: autoplay
                yield Video(
                    url=file_url(msg.file), thumbnail=file_url(msg.thumbnail),
                )

        case 'video_file' | 'video_message':
            # TODO: thumbnail
            yield Video(
                url=file_url(msg.file), thumbnail=file_url(msg.thumbnail),
            )

        case 'audio_file' | 'voice_message':
            yield Audio(
                url=file_url(msg.file),
            )

        case _ as mt:
            if mt:
                raise ValueError(f'Unknown media type: {mt}')
            if msg.file:
                yield File(url=file_url(msg.file), name=msg.file_name)

    if msg.location_information:
        yield RichText(type='rich_text', elements=[
            Text(text=f'{msg.location_information.latitude}, {msg.location_information.longitude}')
        ])

    if msg.contact_information:
        yield RichText(type='rich_text', elements=[
            Text(
                text=f'{msg.contact_information.phone_number}, {msg.contact_information.first_name}, '
                     f'{msg.contact_information.last_name}'
            )
        ])

    if msg.live_location_period_seconds is not None:
        yield RichText(type='rich_text', elements=[
            Text(text=str(msg.live_location_period_seconds))
        ])
