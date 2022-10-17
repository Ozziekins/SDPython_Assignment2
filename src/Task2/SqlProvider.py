from sqlalchemy import create_engine
from Models import Base, LoadedDay, AggregateEntry


class SqlProvider:
    _instance = None
    engine = create_engine('postgresql://postgres:example@127.0.0.1/app', echo=False)
    connection = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SqlProvider, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self.connection is None:
            self.connection = self.engine.connect()

    def execute(self, query):
        self.cursor.execute(query)

    def create_tables(self):
        Base.metadata.create_all(self.engine, checkfirst=True)
