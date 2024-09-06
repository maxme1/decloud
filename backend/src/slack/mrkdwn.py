import re

from ..elements import Broadcast, Channel, Link, PlainText, User


# rules: https://api.slack.com/reference/surfaces/formatting#retrieving-messages
pattern = re.compile(r'<([^>]*)>')


def parse(text: str):
    start = 0
    for match in pattern.finditer(text):
        prefix = text[start:match.start()]
        if prefix:
            yield PlainText(text=prefix, emoji=False)
        start = match.end()

        kind, *context = match.group(1).split('|', 1)
        kind = kind.strip()
        if not context:
            context = None
        else:
            context = context[0]

        if kind.startswith('#C'):
            yield Channel(channel_id=kind.removeprefix('#'), text=context)
        elif kind.startswith('@U') or kind.startswith('@W'):
            yield User(user_id=kind.removeprefix('@'), text=context)
        elif kind.startswith('!'):
            kind = kind.removeprefix('!')
            assert kind in ('channel', 'here', 'everyone')
            assert not context or context == kind, text
            yield Broadcast(range=kind)
        else:
            yield Link(url=kind, text=context)

    if start < len(text):
        yield PlainText(text=text[start:], emoji=False)
