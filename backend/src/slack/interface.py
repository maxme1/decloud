import deli
from jboc import collect

from ..interface import Chat, ChatInfo, ChatInterface
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

    def gather_chats(self):
        return [
            Chat(id=x['id'], name=x['name'], source='slack')
            for x in sorted(deli.load(settings.slack_root / 'conversations.json'), key=lambda x: -x['updated'])
        ]

    @collect
    def gather_agents(self):
        profiles = {}
        for c in deli.load(settings.slack_root / 'conversations.json'):
            if not (settings.slack_root / f'{c["id"]}.json').exists():
                continue

            for m in deli.load(settings.slack_root / f'{c["id"]}.json'):
                if m.get('user'):
                    profile = profiles.setdefault(m['user'], {})
                    profile.setdefault('is_bot', False)

                    if m.get('username'):
                        profile['name'] = m['username']
                    if m.get('user_profile'):
                        profile.setdefault('profile', {}).update(m['user_profile'])

                if m.get('bot_id'):
                    profile = profiles.setdefault(m['bot_id'], {})
                    profile.setdefault('is_bot', True)

                    if m.get('username'):
                        profile['name'] = m['username']
                    if m.get('bot_profile'):
                        profile.setdefault('profile', {}).update(m['bot_profile'])

                for att in m.get('attachments', []):
                    if att.get('author_id'):
                        profile = profiles.setdefault(att['author_id'], {})

                        if att.get('author_name'):
                            profile.setdefault('profile', {}).setdefault('real_name', att['author_name'])
                        if att.get('author_icon'):
                            profile.setdefault('profile', {}).setdefault('image_48', att['author_icon'])
                        if att.get('author_subname'):
                            profile.setdefault('profile', {}).setdefault('real_name', att['author_subname'])

        users = {x['id']: x for x in deli.load(settings.slack_root / 'users.json')}
        for i, profile in profiles.items():
            if set(profile) <= {'id', 'is_bot'}:
                continue

            profile['id'] = i
            if i in users:
                p = profile.setdefault('profile', {})
                p.update(users[i]['profile'])
                profile.update(users[i])
                profile['profile'] = p

            users[i] = profile

        for profile in users.values():
            p = profile.get('profile', {})
            name = p.get('display_name') or p.get('name') or profile.get('name')
            assert name, profile

            images = [
                int(x.removeprefix('image_'))
                for x in p if x.startswith('image_') and x.removeprefix('image_').isdigit()
            ]
            image = None
            if images:
                # 48 is optimal
                image = min(images, key=lambda x: abs(x - 48))
                image = p[f'image_{image}']

            yield Agent(
                id=profile['id'], name=name, avatar=image,
                is_bot=profile['id'] == 'USLACKBOT' or profile.get('is_bot', False),
            )

    def resolve(self, file):
        absolute = settings.slack_root / 'files' / file
        kind = deli.load(absolute.with_suffix('.meta.json'))['mimetype']
        return absolute, kind
