from __future__ import annotations

import multimethod

from ..blocks import Context, File, Image, RichText, Section, Tombstone
from ..elements import EmojiBase, ImageElement, Link, PlainText
from ..schema import AgentMessage, Reaction, Shared, SystemMessage
from .elements import Mrkdwn, custom_emojis
from .schema import BotMessage, EventMessage, ThreadBroadcast, UserMessage
from .utils import file_url, standard_emojis


@multimethod.multimethod
def convert(msg):
    raise NotImplementedError(type(msg))


@convert.register
def convert(msg: UserMessage | BotMessage | ThreadBroadcast):
    replies = msg.replies
    if replies:
        assert replies[0].ts == msg.ts
        replies = replies[1:]

    reactions = []
    for reaction in msg.reactions:
        reaction_name, *tone = reaction.name.split('::')
        reactions.append(Reaction(
            emoji=EmojiBase(
                name=reaction_name, unicode=standard_emojis().get(reaction_name),
                # TODO: skin
                url=custom_emojis().get(reaction_name), skin_tone=None,
            ),
            users=reaction.users
        ))

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

            if attachment.is_share and attachment.message_blocks:
                # dump.pop('message_blocks')
                assert attachment.channel_id
                assert attachment.author_id
                assert attachment.is_msg_unfurl
                assert len(attachment.message_blocks) == 1

                dump.pop('is_share')
                dump.pop('is_msg_unfurl')
                dump.pop('channel_id')
                dump.pop('author_id')
                dump.pop('ts')

                shared.append(Shared(message=AgentMessage(
                    blocks=[x.convert() for x in attachment.message_blocks[0].message.blocks],
                    id=attachment.ts, reactions=[], agent_id=attachment.author_id, shared=[], reply_to=[],
                    timestamp=attachment.ts, thread=[],
                ), channel_id=attachment.channel_id))

                continue

            if attachment.author_name or attachment.author_icon:
                elts = []
                if attachment.author_icon:
                    elts.append(ImageElement(url=attachment.author_icon))
                if attachment.author_name:
                    elts.append(
                        Link(text=attachment.author_name, url=attachment.author_link) if attachment.author_link else
                        PlainText(text=attachment.author_name, emoji=False)
                    )

                dump.pop('author_icon', None)
                dump.pop('author_link', None)
                dump.pop('author_name', None)
                blocks.append(Context(elements=elts))

            # TODO: convert from mrkdwn
            markdown = attachment.mrkdwn_in
            if attachment.pretext:
                dump.pop('pretext')

                blocks.append(Section(elements=[
                    PlainText(text=attachment.pretext, emoji=False) if 'pretext' not in markdown else
                    no_mrkdwn(attachment.pretext)
                ]))

            if attachment.text:
                dump.pop('text')

                blocks.append(Section(elements=[
                    PlainText(text=attachment.text, emoji=False) if 'text' not in markdown else
                    no_mrkdwn(attachment.text)
                ]))

            if attachment.title:
                dump.pop('title')
                dump.pop('title_link')

                blocks.append(Section(elements=[
                    PlainText(text=attachment.title, emoji=False) if not attachment.title_link else
                    Link(url=attachment.title_link, text=attachment.title)
                ]))

            dump.pop('fields')
            for field in attachment.fields:
                if field.title:
                    blocks.append(Section(elements=[no_mrkdwn(field.title)]))
                if field.value:
                    blocks.append(Section(elements=[no_mrkdwn(field.value)]))
                # TODO: short

            if attachment.footer:
                dump.pop('footer')

                blocks.append(Context(elements=[
                    PlainText(text=attachment.footer, emoji=False)
                ]))

            dump.pop('fallback')
            dump.pop('ts')
            dump.pop('id')
            dump.pop('color')

        blocks.extend(
            Section(elements=[PlainText(text=f'\nATTACHMENT: !!!! {x}', emoji=False)]) for x in att_blocks if x
        )

    # files
    blocks.extend(map(convert_file, getattr(msg, 'files', [])))

    return AgentMessage(
        blocks=blocks, id=msg.ts, agent_id=msg.user or msg.bot_id, timestamp=msg.ts,
        thread=list(map(convert, replies)), reactions=reactions, reply_to=replied, shared=shared,
    )


def no_mrkdwn(text):
    return Mrkdwn(text=text, verbatim=False, type='mrkdwn').convert()


@convert.register
def convert(msg: EventMessage):
    return SystemMessage(
        id=msg.ts, blocks=[], timestamp=msg.ts, thread=[], event=msg.subtype, reactions=[],
        agents=[msg.user] if msg.user else [],
    )


def convert_file(file):
    if file.mode == 'tombstone':
        return Tombstone()

    if file.mimetype.startswith('image/'):
        return Image(url=file_url(file.id))

    return File(url=file_url(file.id), name=file.name)
