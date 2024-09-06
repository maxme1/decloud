from __future__ import annotations

from pydantic import BaseModel

from .schema import Agent, AnyMessage


_registry = {}


class ChatInterface:
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
        return _registry[name]()


class ChatInfo(BaseModel):
    agents: list[Agent]


class Chat(BaseModel):
    id: str
    name: str
    source: str
