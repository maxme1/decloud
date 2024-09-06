from __future__ import annotations

import multimethod
from jboc import collect

from .attachments import convert_attachments, convert_files
from .elements import custom_emojis
from .schema import BotMessage, EventMessage, ThreadBroadcast, UserMessage
from .utils import standard_emojis, to_unicode
from ..elements import EmojiBase
from ..schema import AgentMessage, Reaction


@multimethod.multimethod
def convert(msg, context):
    raise NotImplementedError(type(msg))


@convert.register
def convert(msg: UserMessage | BotMessage | ThreadBroadcast, context):
    thread = get_thread(msg.replies, msg, context)
    reactions = get_reactions(msg)

    elements = [x.convert(context) for x in msg.blocks]
    shared = []
    if msg.attachments and not elements:
        # assert not blocks, (blocks, msg.attachments)
        elts, sh = convert_attachments(msg.attachments, context)
        elements.extend(elts)
        shared.extend(sh)

    # files
    elements.extend(convert_files(getattr(msg, 'files', []), context))

    return AgentMessage(
        elements=elements, id=msg.ts, agent_id=msg.user or msg.bot_id, timestamp=msg.ts,
        thread=thread, reactions=reactions, shared=shared,
        edited=msg.edited.ts if msg.edited else None,
    )


@convert.register
def convert(msg: EventMessage, context):
    kwargs = dict(agents=[msg.user] if msg.user else [])
    kwargs.update(msg.kwargs())
    element = msg.get_element()
    return msg.get_event_class()(
        id=msg.ts, timestamp=msg.ts, thread=get_thread(getattr(msg, 'replies', []), msg, context),
        event=msg.get_event(), reactions=get_reactions(msg), **kwargs,
        elements=[element] if element is not None else [],
    )


def get_thread(thread, msg, context):
    if thread:
        assert thread[0].ts == msg.ts
        thread = thread[1:]
    return [convert(t, context) for t in thread]


@collect
def get_reactions(msg):
    for reaction in msg.reactions:
        reaction_name, *tone = reaction.name.split('::')
        yield Reaction(
            emoji=EmojiBase(
                name=reaction_name, unicode=to_unicode(standard_emojis().get(reaction_name)),
                # TODO: skin
                url=custom_emojis().get(reaction_name), skin_tone=None,
            ),
            users=reaction.users
        )
