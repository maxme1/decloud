from jboc import collect
from pydantic import BaseModel


class NoExtra(BaseModel, extra='forbid'):
    pass


@collect
def split_into_segments(xs, predicate):
    if not xs:
        return []

    value = predicate(xs[0])
    current = [xs[0]]
    for x in xs[1:]:
        if predicate(x) == value:
            current.append(x)
        else:
            yield value, current
            value = predicate(x)
            current = [x]

    yield value, current
