import sys
from pathlib import Path

import deli

from src.interface import Chat, ChatInfo
from src.slack.attachments import no_mrkdwn
from src.schema import Agent, AgentMessage


def save(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    deli.save(data, path, hint='.json')


root = Path(__file__).resolve().parent.parent.parent
destination = Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'demo'

users = {}
chats = [
    Chat(id='C123DEF456', name='Planning', source='slack'),
    Chat(id='C123ABC', name='Technical', source='slack'),
]
save([x.model_dump(mode='json') for x in chats], destination / 'chats')

for chat in chats:
    messages = []
    for i, x in enumerate(deli.load(root / f'assets/{chat.id}.json')):
        users[x['username']] = x['display_name'], x['is_bot']
        messages.append(AgentMessage(
            id=str(i), timestamp=x['timestamp'], agent_id=x['username'], elements=[no_mrkdwn(x['text'], True)],
            edited=None, reactions=[], shared=[], thread=[],
        ))

    save([x.model_dump(mode='json') for x in messages], destination / 'messages' / chat.source / chat.id)

users = [Agent(id=x, name=name, avatar=None, is_bot=is_bot) for x, (name, is_bot) in users.items()]
for chat in chats:
    save(ChatInfo(agents=users).model_dump(), destination / 'info' / chat.source / chat.id)
