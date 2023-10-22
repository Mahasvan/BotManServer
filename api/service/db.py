import sqlite3
import sqlalchemy as db
from sqlalchemy import Table, create_engine, Column
from sqlalchemy.orm import Session


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if Database._instance is None:
            Database._instance = object.__new__(cls)
            Database._instance.__init__(*args, **kwargs)

        return Database._instance

    def __init__(self, dbfile: str = "log.db"):
        self.engine = create_engine(f"sqlite:///{dbfile}")
        self.engine.connect()
        self.meta = db.MetaData()

        self._errors = Table(
            "errors", self.meta,
            Column("file", db.String),
            Column("error_type", db.String),
            Column("error", db.String),
            Column("time", db.DateTime))

        self._warnings = Table(
            "warnings", self.meta,
            Column("file", db.String),
            Column("warning", db.String),
            Column("time", db.DateTime)
        )

        self._info = Table(
            "info", self.meta,
            Column("file", db.String),
            Column("info", db.String),
            Column("time", db.DateTime)
        )

        self.meta.create_all(self.engine)

    def error(self, error: Exception, file_or_context: str = "N/A"):
        with Session(self.engine) as session:
            command = self._errors.insert().values(
                error_type=type(error).__name__,
                error=str(error),
                file=file_or_context,
                time=db.func.now()
            )
            session.execute(command)
            session.commit()

    def warning(self, warning: str, file_or_context: str = "N/A"):
        with Session(self.engine) as session:
            command = self._warnings.insert().values(
                warning=warning,
                file=file_or_context,
                time=db.func.now()
            )
            session.execute(command)
            session.commit()

    def info(self, info: str, file_or_context: str = "N/A"):
        with Session(self.engine) as session:
            command = self._info.insert().values(
                info=info,
                file=file_or_context,
                time=db.func.now()
            )
            session.execute(command)
            session.commit()
