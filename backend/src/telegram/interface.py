import deli

from ..interface import ChatInfo, ChatInterface
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

    def info(self, x):
        users = deli.load(settings.telegram_root / 'chats.json')
        return ChatInfo(
            agents=[Agent(id=f'user{x}', name=u, avatar=None, is_bot=False) for x, u in users.items()],
        )

    def resolve(self, file):
        absolute = settings.telegram_root / 'storage' / file
        return absolute, absolute.suffix
