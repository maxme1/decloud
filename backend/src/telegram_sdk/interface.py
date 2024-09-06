from functools import cached_property

import deli
from jboc import collect

from ..interface import ChatDescription, ChatInterface
from ..schema import Agent
from .models.chat import Chat
from .models.message import Message
from .models.user import User


class TelegramSDK(ChatInterface):
    name = 'telegram-sdk'

    def _get_users(self):
        return {x['id']: User.model_validate(x) for x in deli.load(self.root / 'users.json')}

    def _get_chats(self):
        return {x['id']: Chat.model_validate(x) for x in deli.load(self.root / 'chats.json')}

    @cached_property
    def id_to_file(self):
        return {x['remote_uid']: x['filename'] for x in deli.load(self.root / 'files/files.json')}

    @cached_property
    def custom_emojis(self):
        # TODO
        return {}
        # return {x['id']: x['emoji'] for x in deli.load(self.root / 'custom-emojis.json')}

    def load(self, x):
        return sorted(deli.load(self.root / f'messages/{x}.json'), key=lambda v: v['date'])

    def validate(self, msg):
        return Message.model_validate(msg)

    def convert(self, msg):
        return msg.convert(self)

    @collect
    def gather_chats(self):
        for chat in sorted(
                deli.load(self.root / 'chats.json'),
                key=lambda x: x.get('last_message', {}).get('date', 0), reverse=True,
        ):
            chat = Chat.model_validate(chat)
            # skip missing chats
            if not (self.root / f'messages/{chat.id}.json').exists():
                continue
            # and empty ones
            if chat.last_message and chat.last_message['content']['@type'] == 'messageContactRegistered':
                continue

            # exclude bots
            # if (
            #         isinstance(chat.type, Chat.ChatTypePrivate)
            #         and chat.type.user_id in users and
            #         isinstance(users[chat.type.user_id].type, User.BotUser)
            # ):
            #     continue

            # telegram_export main channel: 777000
            # if chat.id == 777000:
            #     continue

            yield ChatDescription(id=str(chat.id), name=chat.title)
        # for chat in settings.telegram_api_root.glob('messages/*.json'):
        #     yield Chat(id=chat.stem, name=chat.stem, source='telegramapi')
        # chat = deli.load(chat)
        # yield Chat(id=str(chat['id']), name=chat['name'], source='telegramapi')

    def gather_agents(self):
        users = self._get_users()
        return [
            Agent(
                id=str(user.id), name=(user.first_name + ' ' + user.last_name).strip(),
                avatar=self.get_file_url(user.profile_photo.small) if user.profile_photo else None,
                is_bot=isinstance(user.type, User.BotUser)
            )
            for user in users.values()
        ]

    def get_file_id(self, x) -> str | None:
        file_id = x.remote.unique_id
        if file_id not in self.id_to_file:
            return
        return file_id

    def resolve(self, file_id):
        absolute = self.root / 'files' / self.id_to_file[file_id]
        return absolute, absolute.suffix
