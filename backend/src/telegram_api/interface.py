import deli
from jboc import collect

from .models.chat import Chat
from .models.user import User
from .utils import id_to_file
from ..interface import Chat as MainChat, ChatInterface
from ..schema import Agent
from ..settings import settings
from .models.message import Message


class TelegramAPI(ChatInterface):
    def _get_users(self):
        return {x['id']: User.model_validate(x) for x in deli.load(settings.telegram_api_root / 'users.json')}

    def _get_chats(self):
        return {x['id']: Chat.model_validate(x) for x in deli.load(settings.telegram_api_root / 'chats.json')}

    def load(self, x):
        return sorted(deli.load(settings.telegram_api_root / f'messages/{x}.json'), key=lambda v: v['date'])

    def validate(self, msg):
        return Message.model_validate(msg)

    def convert(self, msg):
        return msg.convert()

    @collect
    def gather_chats(self):
        users = self._get_users()
        for chat in sorted(
                deli.load(settings.telegram_api_root / 'chats.json'),
                key=lambda x: x.get('last_message', {}).get('date', 0), reverse=True,
        ):
            chat = Chat.model_validate(chat)
            # skip missing chats
            if not (settings.telegram_api_root / f'messages/{chat.id}.json').exists():
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

            # telegram main channel: 777000
            # if chat.id == 777000:
            #     continue

            yield MainChat(id=str(chat.id), name=chat.title, source='telegramapi')
        # for chat in settings.telegram_api_root.glob('messages/*.json'):
        #     yield Chat(id=chat.stem, name=chat.stem, source='telegramapi')
        # chat = deli.load(chat)
        # yield Chat(id=str(chat['id']), name=chat['name'], source='telegramapi')

    def gather_agents(self):
        users = self._get_users()
        return [
            Agent(
                id=str(user.id), name=(user.first_name + ' ' + user.last_name).strip(), avatar=None,
                is_bot=isinstance(user.type, User.BotUser)
            )
            for user in users.values()
        ]

    def resolve(self, file):
        file = int(file)
        absolute = settings.telegram_api_root / 'files' / id_to_file()[file]
        return absolute, absolute.suffix
