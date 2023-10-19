import sqlite3
import sqlalchemy as db
from sqlalchemy import Table, create_engine, Column

class Database:
    def __init__(self, dbfile: str = "service/log.db"):
        self.engine = create_engine(f"sqlite:///{dbfile}")
        self.meta = db.MetaData(bind=self.engine)

        self.errors = Table(
            "errors", self.meta,
            Column("file", db.String),
            Column("error_type", db.String),
            Column("error", db.String),
            Column("time", db.DateTime))

        self.warnings = Table(
            "warnings", self.meta,
            Column("file", db.String),
            Column("warning", db.String),
            Column("time", db.DateTime)
        )

        self.info = Table(
            "info", self.meta,
            Column("info", db.String),
            Column("time", db.DateTime)
        )


    def error(self, error: Exception, file_or_context: str = "N/A"):
        pass

    def warning(self, warning: str, file_or_context: str = "N/A"):
        pass

    def info(self, info: str):
        pass

    def commit(self):
        pass
    def __del__(self):
        self.connection.close()

