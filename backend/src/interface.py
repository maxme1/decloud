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

    def info(self, x):
        pass

    def resolve(self, file):
        pass

    def __init_subclass__(cls, **kwargs):
        _registry[cls.__name__.lower()] = cls

    @classmethod
    def find(cls, name):
        return _registry[name]()


class ChatInfo(BaseModel):
    agents: list[Agent]
