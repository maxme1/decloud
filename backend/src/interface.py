from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from .schema import Agent, AnyMessage
from .settings import settings


_registry = {}


class ChatInterface:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def load(self, x):
        pass

    def validate(self, msg):
        pass

    def convert(self, msg) -> AnyMessage:
        pass

    def gather_agents(self):
        pass

    def gather_chats(self):
        pass

    def resolve(self, file):
        pass

    def __init_subclass__(cls, **kwargs):
        _registry[cls.__name__.lower()] = cls

    @classmethod
    def find(cls, name) -> ChatInterface:
        return cls.all()[name]

    @classmethod
    def all(cls):
        # TODO: fixme
        from .slack.interface import Slack  # noqa
        from .telegram.interface import Telegram  # noqa
        from .telegram_api.interface import TelegramAPI  # noqa

        names = []
        if settings.telegram_api_root:
            names.append(('telegramapi', settings.telegram_api_root))
        if settings.slack_root:
            names.append(('slack', settings.slack_root))
        if settings.telegram_root:
            names.append(('telegram', settings.telegram_root))

        return {name: _registry[name](root) for name, root in names}


class ChatInfo(BaseModel):
    agents: list[Agent]


class Chat(BaseModel):
    id: str
    name: str
    source: str
