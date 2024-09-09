from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pydantic import BaseModel

from .schema import Agent, AnyMessage
from .settings import settings


_registry = {}


class ChatInterface:
    name: str

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

    def gather_chats(self) -> Iterable[ChatDescription]:
        pass

    def get_chats(self) -> list[Chat]:
        return [Chat(**x.model_dump(), source=self.name) for x in self.gather_chats()]

    # files handling

    def get_file_url(self, x):
        if x is None:
            return

        fid = self.get_file_id(x)
        if fid is not None:
            if settings.base_url is None:
                raise ValueError('`base_url` is not set in your config')

            return f'{settings.base_url}/files/{self.name}/{fid}'

    def get_file_id(self, x) -> str | None:
        pass

    def resolve(self, file_id):
        pass

    # subclasses

    def __init_subclass__(cls, **kwargs):
        _registry[cls.name] = cls

    @classmethod
    def find(cls, name) -> ChatInterface:
        return cls.all()[name]

    @classmethod
    def all(cls) -> dict[str, ChatInterface]:
        # TODO: fixme
        from .slack.interface import Slack
        from .telegram_export.interface import TelegramExport
        from .telegram_sdk.interface import TelegramSDK

        names = []
        if settings.telegram_sdk:
            names.append((TelegramSDK, settings.telegram_sdk))
        if settings.slack:
            names.append((Slack, settings.slack))
        if settings.telegram_export:
            names.append((TelegramExport, settings.telegram_export))

        return {cls.name: cls(root) for cls, root in names}


class ChatInfo(BaseModel):
    agents: list[Agent]


class ChatDescription(BaseModel):
    id: str
    name: str


class Chat(ChatDescription):
    source: str
