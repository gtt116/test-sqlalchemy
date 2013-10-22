"""
The script show how the reflect a database to model.
Also show the way to check the column of model.
"""
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base

sql_connection_str = 'mysql://root:password@127.0.0.1/nova?charset=utf8'

Base = declarative_base()
ENGINE = sqlalchemy.create_engine(sql_connection_str)


def get_session():
    return sessionmaker(bind=ENGINE)()


class Service(Base):
    """Represents a running service on a host."""
    __table__ = Table('services', Base.metadata, autoload=True,
                      autoload_with=ENGINE)

assert isinstance(Service.__table__.c.created_at.type, sqlalchemy.DATETIME)
assert isinstance(Service.__table__.c.binary.type, sqlalchemy.String)
print 'check passed.'
