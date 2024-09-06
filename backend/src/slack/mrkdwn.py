import re

from ..elements import Channel, Link, PlainText, User

# rules: https://api.slack.com/reference/surfaces/formatting#retrieving-messages
pattern = re.compile(r'<([^>]*)>')


def parse(text: str):
    start = 0
    for match in pattern.finditer(text):
        prefix = text[start:match.start()]
        if prefix:
            yield PlainText(text=prefix, emoji=False)
        start = match.end()

        kind, *text = match.group(1).split('|', 1)
        if not text:
            text = None
        else:
            text = text[0]

        if kind.startswith('#C'):
            yield Channel(channel_id=kind.removeprefix('#'), text=text)
        elif kind.startswith('@U') or kind.startswith('@W'):
            yield User(user_id=kind.removeprefix('@'), text=text)
        else:
            assert not kind.startswith('!')
            yield Link(url=kind, text=text)

    if start < len(text):
        yield PlainText(text=text[start:], emoji=False)
