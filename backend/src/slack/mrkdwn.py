import datetime
import re

import marko
import multimethod
from marko.block import BlankLine, FencedCode, HTMLBlock, List, ListItem, Paragraph, Document, SetextHeading, \
    ThematicBreak
from marko.ext.gfm.elements import Strikethrough
from marko.inline import AutoLink, CodeSpan, Emphasis, LineBreak, Link, Literal, RawText, StrongEmphasis

from .. import elements


# rules: https://api.slack.com/reference/surfaces/formatting#retrieving-messages
pattern = re.compile(r'<([^>]*)>')


def convert_mrkdwn(text: str):
    # TODO: convert stuff like `&amp;` to `&`
    return list(_unpack(marko.Markdown().parse(text)))


def unpack_mrkdwn(text: str):
    start = 0
    for match in pattern.finditer(text):
        prefix = text[start:match.start()]
        start = match.end()

        if prefix:
            yield elements.Text(text=prefix)

        kind, context = _split_context(match.group(1))
        if kind.startswith('#C'):
            yield elements.Channel(channel_id=kind.removeprefix('#'), text=context)
        elif kind.startswith('@U') or kind.startswith('@W'):
            yield elements.User(user_id=kind.removeprefix('@'), element=context)
        elif kind.startswith('!'):
            kind = kind.removeprefix('!')
            if kind in ('channel', 'here', 'everyone'):
                assert not context or context == kind, text
                yield elements.Broadcast(range=kind)

            else:
                assert kind.startswith('date'), kind
                _, stamp, *_ = kind.split('^')
                stamp = datetime.datetime.fromtimestamp(float(stamp))
                # TODO
                yield elements.Text(text=stamp.isoformat())

        else:
            if context is not None:
                context = elements.Text(text=context)
            yield elements.Link(url=kind, element=context)

    if start < len(text):
        yield elements.Text(text=text[start:])


def _split_context(text):
    kind, *context = text.split('|', 1)
    kind = kind.strip()
    if not context:
        context = None
    else:
        context = context[0]

    return kind, context


@multimethod.multimethod
def _unpack(x):
    raise TypeError(x)


@_unpack.register
def _unpack(x: Document | Paragraph):
    for child in x.children:
        yield from _unpack(child)


@_unpack.register
def _unpack(x: RawText):
    return unpack_mrkdwn(x.children)


@_unpack.register
def _unpack(x: StrongEmphasis):
    yield elements.Bold(element=_unpack_many(x.children))


@_unpack.register
def _unpack(x: Emphasis):
    yield elements.Italic(element=_unpack_many(x.children))


@_unpack.register
def _unpack(x: Strikethrough):
    yield elements.Strike(element=_unpack_many(x.children), position='through')


@_unpack.register
def _unpack(x: LineBreak):
    assert x.children == '\n'
    yield elements.Text(text='\n')


@_unpack.register
def _unpack(x: BlankLine):
    assert x.children == []
    yield elements.Text(text='\n')


@_unpack.register
def _unpack(x: AutoLink):
    assert len(x.children) == 1
    assert isinstance(x.children[0], RawText)
    link, text = _split_context(x.children[0].children)
    if text is not None:
        text = elements.Text(text=text)

    yield elements.Link(url=link, element=text)


@_unpack.register
def _unpack(x: CodeSpan):
    return unpack_mrkdwn(x.children)


@_unpack.register
def _unpack(x: FencedCode):
    yield elements.Code(element=_unpack_many(x.children), language=x.lang or None)


@_unpack.register
def _unpack(x: SetextHeading):
    for child in x.children:
        yield from _unpack(child)


@_unpack.register
def _unpack(x: HTMLBlock):
    assert not x.children, x.children
    return unpack_mrkdwn(x.body)


@_unpack.register
def _unpack(x: Link):
    yield elements.Link(url=x.dest, element=_unpack_many(x.children))


@_unpack.register
def _unpack(x: Literal):
    yield elements.Text(text=x.children)


@_unpack.register
def _unpack(x: ThematicBreak):
    assert not x.children
    yield elements.Text(text='* * *')


@_unpack.register
def _unpack(x: List):
    # TODO: start might not be 1
    # assert x.start == 1, vars(x)
    # assert x.tight, vars(x)

    items = []
    for child in x.children:
        assert isinstance(child, ListItem), child
        items.append(_unpack_many(child.children))
    yield elements.List(elements=items, style='ordered' if x.ordered else 'unordered')


def _unpack_many(xs):
    content = []
    for x in xs:
        content.extend(_unpack(x))
    if len(content) == 1:
        return content[0]
    return elements.Sequence(elements=content)
