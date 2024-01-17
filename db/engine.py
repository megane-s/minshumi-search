import os
from functools import cache

from sqlalchemy import create_engine


@cache
def get_engine():
    db_uri = os.environ['DATABASE_URL']
    engine = create_engine(
        db_uri, connect_args={
            "application_name": "docs_simplecrud_sqlalchemy",
        },
    )
    return engine
