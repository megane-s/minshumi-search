
from typing import Any, Generator, Iterable, TypeVar

T = TypeVar("T")


def group_by_count(iter: Iterable[T], count: int) -> Generator[list[T], Any, None]:
    values = []
    for value in iter:
        if len(values) == count:
            yield values
            values = []
        else:
            values.append(value)
    if len(values) != 0:
        yield values
