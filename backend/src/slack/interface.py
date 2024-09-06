import deli
from jboc import collect

from ..interface import ChatDescription, ChatInterface
from ..schema import Agent
from .convert import convert
from .schema import AnyMessage


class Slack(ChatInterface):
    name = 'slack'

    def load(self, x):
        return deli.load(self.root / f'messages/{x}.json')

    def validate(self, msg):
        return AnyMessage.validate_python(msg)

    def convert(self, msg):
        return convert(msg, self)

    def gather_chats(self):
        return [
            ChatDescription(id=x['id'], name=x['name'])
            for x in sorted(deli.load(self.root / 'conversations.json'), key=lambda x: -x['updated'])
        ]

    @collect
    def gather_agents(self):
        users = deli.load(self.root / 'users.json')
        for user in users:
            p = user.get('profile', {})
            name = p.get('display_name') or p.get('name') or user.get('name') or p.get('real_name')
            assert name, user

            images = [
                int(x.removeprefix('image_'))
                for x in p if x.startswith('image_') and x.removeprefix('image_').isdigit()
            ]
            image = None
            if images:
                # 48 is optimal but larger is preferable otherwise
                image = min(images, key=lambda x: (abs(48 - x), 48 - x))
                image = p[f'image_{image}']

            yield Agent(
                id=user['id'], name=name, avatar=image,
                is_bot=user['id'] == 'USLACKBOT' or user.get('is_bot', False),
            )

    def get_file_id(self, x):
        if x and (self.root / 'files' / x).exists():
            return x

    def resolve(self, file_id):
        absolute = self.root / 'files' / file_id
        kind = deli.load(absolute.with_suffix('.meta.json'))['mimetype']
        return absolute, kind
