"""
The script show out a result that when insert execute cocurrent up to
10,000 sqlalchemy will be bottleneck. Sqlite vs alchemy is 40/ 62
"""
import sqlite3
import time
import sqlalchemy
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_connection_str = 'sqlite:///test.sqlite'
ENGINE = sqlalchemy.create_engine(sql_connection_str)

Base = declarative_base()
Base.metadata.bind = ENGINE


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)


def get_session():
    return sessionmaker(bind=ENGINE)()


def insert_alchemy():
    session = get_session()
    session.add(User(name='alchemy', age=1))
    session.commit()
    session.close()


class SqliteManage(object):
    def __init__(self, database):
        self._database = database
        self._conn = None

    def connect(self):
        if not self._conn:
            self._conn = sqlite3.connect(self._database)
        return self._conn

    def insert(self):
        with self.connect() as conn:
            conn.execute("insert into [users] (name, age) values ('sqlite3',1)")


def timeit(func):
    startpoint = time.time()
    for i in xrange(10000):
        func()
    print time.time() - startpoint

Base.metadata.create_all()

lite = SqliteManage('test.sqlite')
lite.connect()
timeit(lite.insert)

timeit(insert_alchemy)
