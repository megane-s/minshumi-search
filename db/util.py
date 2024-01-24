from typing import Callable, Concatenate, ParamSpec, TypeVar

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from art.db.model import DbArt
from db.engine import get_engine
from util.log import WithLog

Res = TypeVar("Res")


def transactional():
    def annotated_func(func: Callable[Concatenate[Session, ...], Res]) -> Callable[..., Res]:
        def func_with_transaction(*args, **kwargs) -> Res:
            return run_transaction(
                sessionmaker(bind=get_engine()),
                lambda s: func(s, *args, **kwargs),
            )
        return func_with_transaction
    return annotated_func
