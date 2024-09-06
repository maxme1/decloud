from __future__ import annotations

from jboc import collect

from .mrkdwn import convert_mrkdwn
from .schema import Attachment, UnknownFile
from ..elements import Context, File, Icon, Image, Link, Section, Sequence, Text
from ..schema import Shared
from ..utils import split_into_segments


@collect
def convert_files(files, context):
    for is_image, group in split_into_segments(
            files, lambda x: hasattr(x, 'mimetype') and x.mimetype.startswith('image/')
    ):
        if is_image:
            yield Sequence.wrap([Image(url=context.get_file_url(file.id), name=file.name) for file in group])

        else:
            for file in group:
                if isinstance(file, UnknownFile):
                    yield File(url=context.get_file_url(file.id), name=None, mimetype=None, thumbnail=None)

                elif file.mode == 'tombstone':
                    yield File(url=None, name=None, mimetype=None, thumbnail=None)

                else:
                    yield File(
                        url=context.get_file_url(file.id), name=file.name, mimetype=file.mimetype, thumbnail=None
                    )


def convert_attachments(attachments: list[Attachment], context):
    # https://api.slack.com/messaging/attachments-to-blocks#switching_to_blocks
    elements, att_blocks, shared = [], [], []
    for attachment in attachments:
        dump = attachment.model_dump(exclude_none=True, exclude_unset=True)
        att_blocks.append(dump)
        # att_blocks.append(attachment.model_dump())

        # TODO: color?
        if attachment.blocks:
            continue

        dump.pop('fallback', None)
        dump.pop('ts', None)
        dump.pop('id', None)
        dump.pop('color', None)
        markdown = set(attachment.mrkdwn_in)
        if markdown <= {'pretext', 'text', 'title', 'fields', 'footer'}:
            dump.pop('mrkdwn_in', None)

        if attachment.is_share and attachment.ts and attachment.channel_id:
            # assert attachment.channel_id
            # assert attachment.author_id, attachment
            # assert attachment.is_msg_unfurl

            dump.pop('is_share')
            dump.pop('is_msg_unfurl', None)
            dump.pop('is_reply_unfurl', None)
            dump.pop('is_thread_root_unfurl', None)
            dump.pop('channel_id', None)
            dump.pop('author_id', None)
            dump.pop('text', None)
            dump.pop('files', None)
            dump.pop('footer', None)
            dump.pop('from_url', None)
            for k in [x for x in dump if x.startswith('author_')]:
                dump.pop(k, None)

            if attachment.message_blocks:
                assert len(attachment.message_blocks) == 1
                dump['message_blocks'][0].pop('message')
                if not dump['message_blocks'][0]:
                    dump.pop('message_blocks')

                content = [x.convert(context) for x in attachment.message_blocks[0].message.blocks]
            elif attachment.text:
                content = [no_mrkdwn(attachment.text, 'text' in markdown)]
            else:
                content = []

            shared.append(Shared(
                elements=content + convert_files(attachment.files, context), id=attachment.ts,
                agent_id=attachment.author_id, timestamp=attachment.ts, channel_id=attachment.channel_id
            ))

            continue

        if attachment.author_name or attachment.author_icon:
            elts = []
            if attachment.author_icon:
                elts.append(Icon(url=attachment.author_icon, name=attachment.author_name))
            if attachment.author_name:
                elts.append(
                    Link(element=Text(text=attachment.author_name), url=attachment.author_link)
                    if attachment.author_link else Text(text=attachment.author_name)
                )

            dump.pop('author_icon', None)
            dump.pop('author_link', None)
            dump.pop('author_name', None)
            elements.append(Context(elements=elts))

        if attachment.pretext:
            dump.pop('pretext')

            elements.append(Section(element=no_mrkdwn(attachment.pretext, True)))

        if attachment.title:
            dump.pop('title')
            dump.pop('title_link', None)
            title = no_mrkdwn(attachment.title, True)

            elements.append(Section(
                element=title if not attachment.title_link else Link(url=attachment.title_link, element=title)
            ))

        if attachment.text:
            dump.pop('text')

            elements.append(Section(element=no_mrkdwn(attachment.text, 'text' in markdown)))

        dump.pop('fields', None)
        for field in attachment.fields:
            elts = []
            if field.title:
                elts.append(no_mrkdwn(field.title, True))
            if field.value:
                elts.append(no_mrkdwn(field.value, True))
            # TODO: short
            if len(elts) == 2:
                elts.insert(1, Text(text=' '))
            elements.append(Section(element=Sequence(elements=elts)))

        if attachment.footer:
            dump.pop('footer')
            dump.pop('footer_icon', None)

            elts = []
            if attachment.footer_icon:
                elts.append(Icon(url=attachment.footer_icon, name=None))
            elts.append(no_mrkdwn(attachment.footer, True))

            elements.append(Context(elements=elts))

    elements.extend(
        Section(element=Text(text=f'\nATTACHMENT: !!!! {x}')) for x in att_blocks if x
    )
    return elements, shared


def no_mrkdwn(text, unpack):
    if not unpack:
        return Text(text=text)

    return Sequence(elements=convert_mrkdwn(text))
