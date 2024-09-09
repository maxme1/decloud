from __future__ import annotations

import datetime
from typing import Literal, Union

from .content import ContentBase
from .events import SystemEvent
from .sender import Sender, SenderChat, SenderUser
from ..utils import FlaggedTimestamp, Subclasses, TypeDispatch
from ...elements import EmojiBase
from ...schema import AgentMessage, Reaction, Shared
from ...utils import Maybe


Content = Union[*ContentBase.__subclasses__()]


class Message(TypeDispatch):
    type_: Literal['message']

    id: int
    chat_id: int
    sender_id: Sender

    content: Content
    date: datetime.datetime
    edit_date: FlaggedTimestamp

    interaction_info: Maybe[InteractionInfo]
    forward_info: Maybe[ForwardInfo]
    reply_to: Maybe[ReplyTo]
    reply_markup: Maybe[Markup]

    author_signature: str
    auto_delete_in: int
    can_be_saved: bool
    contains_unread_mention: bool
    effect_id: int
    has_sensitive_content: bool
    has_timestamped_media: bool
    is_channel_post: bool
    is_from_offline: bool
    is_outgoing: bool
    is_pinned: bool
    is_topic_message: bool
    media_album_id: int
    message_thread_id: int
    restriction_reason: str
    saved_messages_topic_id: int
    self_destruct_in: float
    sender_boost_count: int
    sender_business_bot_user_id: int
    unread_reactions: list
    via_bot_user_id: int

    def get_user_ids(self):
        yield from self.content.get_user_ids()
        if isinstance(self.sender_id, SenderUser):
            yield self.sender_id.user_id
        if self.reply_to and self.reply_to.origin:
            uid = self.reply_to.origin.get_ids()[0]
            if uid is not None:
                yield uid
        if self.forward_info and self.forward_info.origin:
            uid = self.forward_info.origin.get_ids()[0]
            if uid is not None:
                yield uid

    def convert(self, context):
        reactions = []
        if self.interaction_info and self.interaction_info.reactions:
            for reaction in self.interaction_info.reactions.reactions:
                if isinstance(reaction.type, EmojiReaction):
                    emoji = reaction.type.emoji
                else:
                    # TODO
                    emoji = context.custom_emojis.get(reaction.type.custom_emoji_id, reaction.type.custom_emoji_id)

                reactions.append(Reaction(
                    emoji=EmojiBase(unicode=emoji, name=None, skin_tone=None, url=None),
                    # TODO
                    users=[''] * reaction.total_count,
                ))

        if isinstance(self.sender_id, SenderChat):
            sender = self.sender_id.chat_id
        else:
            sender = self.sender_id.user_id
        sender = str(sender)

        if isinstance(self.content, SystemEvent):
            kwargs = dict(agents=[])
            kwargs.update(self.content.kwargs(self))
            kwargs['agents'] = list(map(str, kwargs['agents']))
            element = self.content.convert(context)
            return self.content.event_class(
                id=str(self.id), timestamp=self.date, thread=[], elements=[element] if element else [],
                reactions=reactions, event=self.content.get_event(), **kwargs,
            )

        elements = [self.content.convert(context)]
        shared = []
        if self.forward_info:
            message_id = channel_id = agent_id = None
            if self.forward_info.source:
                message_id = self.forward_info.source.message_id
                channel_id = self.forward_info.source.chat_id
            elif self.forward_info.origin:
                agent_id, channel_id = self.forward_info.origin.get_ids()

            shared.append(Shared(
                id=str(message_id) if message_id is not None else None,
                channel_id=str(channel_id) if channel_id is not None else None,
                agent_id=str(agent_id) if agent_id is not None else None,
                timestamp=self.forward_info.date, elements=elements,
            ))
            elements = []

        if self.reply_to:
            agent_id, _ = self.reply_to.origin.get_ids() if self.reply_to.origin else (None, None)
            shared.append(Shared(
                id=str(self.reply_to.message_id), channel_id=str(self.reply_to.chat_id),
                timestamp=self.reply_to.origin_send_date,
                agent_id=str(agent_id) if agent_id is not None else None,
                elements=[self.reply_to.content.convert(context)] if self.reply_to.content else [],
            ))

        return AgentMessage(
            id=str(self.id), timestamp=self.date, thread=[], elements=elements,
            reactions=reactions, shared=shared, edited=self.edit_date, agent_id=sender,
        )


class InteractionInfo(TypeDispatch):
    class Reactions(TypeDispatch):
        class Reaction(TypeDispatch):
            type_: Literal['messageReaction']
            type: ReactionType
            total_count: int
            is_chosen: bool
            used_sender_id: Maybe[Sender]
            recent_sender_ids: list[Sender]

        type_: Literal['messageReactions']
        reactions: list[Reaction]
        are_tags: bool
        paid_reactors: list
        can_get_added_reactions: bool

    class ReplyInfo(TypeDispatch):
        type_: Literal['messageReplyInfo']
        reply_count: int
        recent_replier_ids: list[dict]
        last_read_inbox_message_id: int
        last_read_outbox_message_id: int
        last_message_id: int

    type_: Literal['messageInteractionInfo']
    reactions: Maybe[Reactions]
    reply_info: Maybe[ReplyInfo]
    view_count: int
    forward_count: int


class ReactionTypeBase(TypeDispatch):
    pass


class EmojiReaction(ReactionTypeBase):
    type_: Literal['reactionTypeEmoji']
    emoji: str


class CustomEmojiReaction(ReactionTypeBase):
    type_: Literal['reactionTypeCustomEmoji']
    custom_emoji_id: str


ReactionType = Union[*ReactionTypeBase.__subclasses__()]


class ForwardInfo(TypeDispatch):
    class Source(TypeDispatch):
        type_: Literal['forwardSource']
        chat_id: int
        sender_id: Maybe[Sender]
        message_id: int
        sender_name: str
        date: datetime.datetime
        is_outgoing: bool

    type_: Literal['messageForwardInfo']
    source: Maybe[Source]
    origin: Maybe[Origin]
    date: FlaggedTimestamp
    public_service_announcement_type: str


class OriginBase(TypeDispatch):
    def get_ids(self):
        raise NotImplementedError


class UserOrigin(OriginBase):
    type_: Literal['messageOriginUser']
    sender_user_id: int

    def get_ids(self):
        return self.sender_user_id, None


class HiddenUserOrigin(OriginBase):
    type_: Literal['messageOriginHiddenUser']
    sender_name: str

    def get_ids(self):
        return None, None


class ChannelOrigin(OriginBase):
    type_: Literal['messageOriginChannel']
    chat_id: int
    message_id: int
    author_signature: str

    def get_ids(self):
        return None, self.chat_id


class ChatOrigin(OriginBase):
    type_: Literal['messageOriginChat']
    sender_chat_id: int
    author_signature: str

    def get_ids(self):
        return None, self.sender_chat_id


Origin = Subclasses[OriginBase]


class ReplyTo(TypeDispatch):
    type_: Literal['messageReplyToMessage']
    origin: Maybe[Origin]
    content: Maybe[Content]
    chat_id: int
    message_id: int
    origin_send_date: FlaggedTimestamp
    quote: Maybe[dict]


class MarkupBase(TypeDispatch):
    pass


class InlineKeyboard(MarkupBase):
    type_: Literal['replyMarkupInlineKeyboard']
    rows: list


class ShowKeyboard(MarkupBase, extra='ignore'):
    type_: Literal['replyMarkupShowKeyboard']


Markup = Union[*MarkupBase.__subclasses__()]
