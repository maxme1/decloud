import deli

from ..interface import ChatInfo, ChatInterface
from ..schema import Agent
from ..settings import settings
from .convert import convert
from .schema import AnyMessage


class Slack(ChatInterface):
    def load(self, x):
        return deli.load(settings.slack_root / f'{x}.json')

    def validate(self, msg):
        return AnyMessage.validate_python(msg)

    def convert(self, msg):
        return convert(msg)

    def info(self, x):
        users = deli.load(settings.slack_root / 'users.json')
        bots = deli.load(settings.slack_root / 'bots.json')
        return ChatInfo(
            agents=[
                       Agent(
                           id=x['id'], name=x['name'], avatar=x.get('profile', {}).get('image_48'),
                           is_bot=x['name'] == 'slackbot',
                       ) for x in users
                   ] + [
                       Agent(id=x['id'], name=x['name'], avatar=None, is_bot=True) for x in bots
                   ],
        )

    def resolve(self, file):
        absolute = settings.slack_root / 'files' / file
        kind = deli.load(absolute.with_suffix('.meta.json'))['mimetype']
        return absolute, kind
