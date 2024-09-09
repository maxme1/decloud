import contextlib
from typing import Annotated, TypeVar

import deli
import rich
import typer
from jboc import collect
from pydantic import BaseModel, Field
from rich.progress import BarColumn, Progress, TimeElapsedColumn, TimeRemainingColumn
from tqdm.rich import RateColumn


class NoExtra(BaseModel, extra='forbid'):
    pass


T = TypeVar('T')
Maybe = Annotated[T, Field(default=None)]


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


@contextlib.contextmanager
def nested_rich():
    def add(xs, desc=None, leave=True, total=None, **kwargs):
        if total is None:
            try:
                total = len(xs)
            except TypeError:
                pass

        task = progress.add_task(desc or '', total=total, **kwargs)
        for x in xs:
            progress.update(task, advance=1)
            yield x

        if not leave:
            progress.remove_task(task)

    with Progress(
            "[progress.description]{task.description}"
            "[progress.percentage]{task.percentage:>4.0f}%",
            BarColumn(bar_width=None),
            # FractionColumn(),
            "[", TimeElapsedColumn(), "<", TimeRemainingColumn(), ",", RateColumn(), "]"
    ) as progress:
        yield add
