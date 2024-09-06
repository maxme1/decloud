import deli
from jboc import collect

from ..interface import Chat, ChatInfo, ChatInterface
from ..schema import Agent
from ..settings import settings
from .convert import convert
from .schema import AnyMessage


class Telegram(ChatInterface):
    def load(self, x):
        return deli.load(settings.telegram_root / f'{x}.json')['messages']

    def validate(self, msg):
        return AnyMessage.validate_python(msg)

    def convert(self, msg):
        return convert(msg)

    @collect
    def gather_chats(self):
        for chat in settings.telegram_root.glob('*.json'):
            chat = deli.load(chat)
            yield Chat(id=str(chat['id']), name=chat['name'], source='telegram')

    def gather_agents(self):
        agents = {}
        for chat in settings.telegram_root.glob('*.json'):
            chat = deli.load(chat)
            if chat['type'] == 'personal_chat':
                agents[f'user{chat["id"]}'] = chat['name']

            for message in chat['messages']:
                if message.get('from_id') and message.get('from'):
                    agents.setdefault(message['from_id'], message['from'])

        return [Agent(id=x, name=u, avatar=None, is_bot=False) for x, u in agents.items()]

    def resolve(self, file):
        absolute = settings.telegram_root / 'storage' / file
        return absolute, absolute.suffix
