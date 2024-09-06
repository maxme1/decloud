import deli
from jboc import collect

from ..interface import ChatDescription, ChatInterface
from ..schema import Agent
from .convert import convert
from .schema import AnyMessage


class TelegramExport(ChatInterface):
    name = 'telegram-export'

    def load(self, x):
        return deli.load(self.root / f'{x}.json')['messages']

    def validate(self, msg):
        return AnyMessage.validate_python(msg)

    def convert(self, msg):
        return convert(msg, self)

    @collect
    def gather_chats(self):
        for chat in self.root.glob('*.json'):
            chat = deli.load(chat)
            yield ChatDescription(id=str(chat['id']), name=chat['name'])

    def gather_agents(self):
        agents = {}
        for chat in self.root.glob('*.json'):
            chat = deli.load(chat)
            if chat['type'] == 'personal_chat':
                agents[f'user{chat["id"]}'] = chat['name']

            for message in chat['messages']:
                if message.get('from_id') and message.get('from'):
                    agents.setdefault(message['from_id'], message['from'])

        return [Agent(id=x, name=u, avatar=None, is_bot=False) for x, u in agents.items()]

    def get_file_id(self, x):
        if x == MISSING_FILE or not (self.root / x).exists():
            return
        return x.removeprefix('storage/')

    def resolve(self, file_id):
        absolute = self.root / 'storage' / file_id
        return absolute, absolute.suffix


MISSING_FILE = '(File not included. Change data exporting settings to download.)'
