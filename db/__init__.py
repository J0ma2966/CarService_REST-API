import sqlalchemy
from sqlalchemy import create_engine

from config.conf import DB


def make_connection_string(db: DB, async_fallback: bool = False) -> str:
    result = (
        f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.db_name}"
    )

    if async_fallback:
        result += "?async_fallback=True"

    return result


def get_engine(db: DB) -> sqlalchemy.engine.Engine:
    engine: sqlalchemy.engine.Engine = create_engine(
        make_connection_string(db), encoding="utf-8", echo=False
    )

    return engine
