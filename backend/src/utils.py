import deli
import rich
import typer
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


def load_backup(path):
    if path.exists():
        try:
            return deli.load(path)
        except Exception as e:
            rich.print(f'Error loading {path}: {e}')
            raise typer.Exit(1) from e

    return []


def save_backup(data, path):
    tmp = path.with_stem('tmp-' + path.stem)
    deli.save(data, tmp)
    if path.exists():
        path.unlink()
    tmp.rename(path)
