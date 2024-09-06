from __future__ import annotations

import multimethod
from jboc import collect

from ..blocks import Context, File, RichText, Section, Tombstone
from ..elements import EmojiBase, Icon, Image, Link, Text
from ..schema import AgentMessage, Reaction, Shared, SystemMessage
from .elements import Mrkdwn, custom_emojis
from .schema import BotMessage, EventMessage, ThreadBroadcast, UnknownFile, UserMessage
from .utils import file_url, standard_emojis
from ..utils import split_into_segments


@multimethod.multimethod
def convert(msg):
    raise NotImplementedError(type(msg))


@convert.register
def convert(msg: UserMessage | BotMessage | ThreadBroadcast):
    thread = get_thread(msg.replies, msg)
    reactions = get_reactions(msg)

    blocks = [x.convert() for x in msg.blocks]
    replied = []
    shared = []
    if msg.attachments and not blocks:
        # TODO: migrate with https://api.slack.com/messaging/attachments-to-blocks#switching_to_blocks
        # assert not blocks, (blocks, msg.attachments)
        att_blocks = []
        for attachment in msg.attachments:
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

            if attachment.is_share and attachment.ts:
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
                # TODO: use this info if the user is not known
                for k in [x for x in dump if x.startswith('author_')]:
                    dump.pop(k, None)

                if attachment.message_blocks:
                    assert len(attachment.message_blocks) == 1
                    dump['message_blocks'][0].pop('message')
                    if not dump['message_blocks'][0]:
                        dump.pop('message_blocks')

                    content = [x.convert() for x in attachment.message_blocks[0].message.blocks]
                elif attachment.text:
                    content = [RichText(elements=[no_mrkdwn(attachment.text, 'text' in markdown)])]
                else:
                    content = []

                shared.append(Shared(
                    message=AgentMessage(
                        blocks=content + list(convert_files(attachment.files)),
                        id=attachment.ts, reactions=[], agent_id=attachment.author_id, shared=[], reply_to=[],
                        timestamp=attachment.ts, thread=[],
                    ),
                    channel_id=attachment.channel_id
                ))

                continue

            if attachment.author_name or attachment.author_icon:
                elts = []
                if attachment.author_icon:
                    elts.append(Icon(url=attachment.author_icon))
                if attachment.author_name:
                    elts.append(
                        Link(text=Text(text=attachment.author_name), url=attachment.author_link)
                        if attachment.author_link else Text(text=attachment.author_name)
                    )

                dump.pop('author_icon', None)
                dump.pop('author_link', None)
                dump.pop('author_name', None)
                blocks.append(Context(elements=elts))

            if attachment.pretext:
                dump.pop('pretext')

                blocks.append(Section(elements=[no_mrkdwn(attachment.pretext, True)]))

            if attachment.title:
                dump.pop('title')
                dump.pop('title_link', None)
                title = no_mrkdwn(attachment.title, True)

                blocks.append(Section(elements=[
                    title if not attachment.title_link else
                    Link(url=attachment.title_link, text=title)
                ]))

            if attachment.text:
                dump.pop('text')

                blocks.append(Section(elements=[no_mrkdwn(attachment.text, 'text' in markdown)]))

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
                blocks.append(Section(elements=elts))

            if attachment.footer:
                dump.pop('footer')
                dump.pop('footer_icon', None)

                elts = []
                if attachment.footer_icon:
                    elts.append(Icon(url=attachment.footer_icon))
                elts.append(no_mrkdwn(attachment.footer, True))

                blocks.append(Context(elements=elts))

        blocks.extend(
            Section(elements=[Text(text=f'\nATTACHMENT: !!!! {x}')]) for x in att_blocks if x
        )

    # files
    blocks.extend(convert_files(getattr(msg, 'files', [])))

    return AgentMessage(
        blocks=blocks, id=msg.ts, agent_id=msg.user or msg.bot_id, timestamp=msg.ts,
        thread=thread, reactions=reactions, reply_to=replied, shared=shared,
    )


def no_mrkdwn(text, unpack):
    if not unpack:
        return Text(text=text)

    return Mrkdwn(text=text, verbatim=False, type='mrkdwn').convert()


@convert.register
def convert(msg: EventMessage):
    events = dict(
        huddle_thread='call',
        channel_join='join',
        channel_leave='leave',
        channel_purpose='purpose',
    ) | dict.fromkeys(('reminder_add',), 'custom')

    blocks = []
    if msg.subtype == 'reminder_add':
        blocks.append(RichText(elements=[Text(text=msg.text)]))
    if msg.subtype == 'channel_purpose':
        blocks.append(RichText(elements=[Text(text=msg.purpose)]))

    if msg.subtype not in events and msg.subtype not in ['channel_canvas_updated']:
        print('missing subtype', msg.subtype)

    return SystemMessage(
        id=msg.ts, blocks=blocks, timestamp=msg.ts, thread=get_thread(getattr(msg, 'replies', []), msg),
        event=events.get(msg.subtype, msg.subtype),
        reactions=get_reactions(msg), agents=[msg.user] if msg.user else [],
    )


def get_thread(thread, msg):
    if thread:
        assert thread[0].ts == msg.ts
        thread = thread[1:]
    return list(map(convert, thread))


@collect
def get_reactions(msg):
    for reaction in msg.reactions:
        reaction_name, *tone = reaction.name.split('::')
        yield Reaction(
            emoji=EmojiBase(
                name=reaction_name, unicode=standard_emojis().get(reaction_name),
                # TODO: skin
                url=custom_emojis().get(reaction_name), skin_tone=None,
            ),
            users=reaction.users
        )


def convert_files(files):
    for is_image, group in split_into_segments(
            files, lambda x: hasattr(x, 'mimetype') and x.mimetype.startswith('image/')
    ):
        if is_image:
            yield RichText(elements=[Image(url=file_url(file.id), name=file.name) for file in group])

        else:
            for file in group:
                if isinstance(file, UnknownFile):
                    yield File(url=file_url(file.id), name=None)

                elif file.mode == 'tombstone':
                    yield Tombstone()

                else:
                    yield File(url=file_url(file.id), name=file.name, mimetype=file.mimetype)
