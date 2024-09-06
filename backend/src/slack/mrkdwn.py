import re

import marko
import multimethod
from marko.block import BlankLine, Paragraph, Document
from marko.ext.gfm.elements import Strikethrough
from marko.inline import Emphasis, LineBreak, RawText, StrongEmphasis

from ..elements import Bold, Broadcast, Channel, Italic, Link, Strike, Text, User


# rules: https://api.slack.com/reference/surfaces/formatting#retrieving-messages
pattern = re.compile(r'<([^>]*)>')


def parse(text: str):
    # TODO: convert stuff like `&amp;` to `&`
    start = 0
    for match in pattern.finditer(text):
        prefix = text[start:match.start()]
        start = match.end()

        if prefix:
            yield from convert_markdown(prefix)

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
        yield from convert_markdown(text[start:])


def convert_markdown(text: str):
    return list(_unpack(marko.Markdown().parse(text)))


@multimethod.multimethod
def _unpack(x):
    raise TypeError(x)


@_unpack.register
def _unpack(x: Document | Paragraph):
    for child in x.children:
        yield from _unpack(child)


@_unpack.register
def _unpack(x: RawText):
    yield Text(text=x.children)


@_unpack.register
def _unpack(x: StrongEmphasis):
    assert len(x.children) == 1
    child, = _unpack(x.children[0])
    yield Bold(element=child)


@_unpack.register
def _unpack(x: Emphasis):
    assert len(x.children) == 1
    child, = _unpack(x.children[0])
    yield Italic(element=child)


@_unpack.register
def _unpack(x: Strikethrough):
    assert len(x.children) == 1
    child, = _unpack(x.children[0])
    yield Strike(element=child)


@_unpack.register
def _unpack(x: LineBreak):
    assert x.children == '\n'
    yield Text(text='\n')


@_unpack.register
def _unpack(x: BlankLine):
    assert x.children == []
    yield Text(text='\n')
