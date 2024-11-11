from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:
    def __init__(self, config):
        self.config = config
        self._engine = None
        self._session_local = None

    def _get_engine(self):
        if not self._engine:
            self._engine = create_engine(
                self.config["DATABASE_URL"], pool_size=10, max_overflow=20)
        return self._engine

    def get_session(self):
        if not self._session_local:
            engine = self._get_engine()
            self._session_local = sessionmaker(
                autocommit=False, autoflush=False, bind=engine)
        return self._session_local()

    def get_engine(self):
        return self._get_engine()
