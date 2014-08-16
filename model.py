from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapper
from database import metadata, db_session
from datetime import datetime

class Link(object):
    query = db_session.query_property()

    def __init__(self, url=None, title=None):
        self.url = url
        self.title = title
        self.usage_count = 0
        self.last_access = datetime.utcnow()

    def __repr__(self):
        return '<Link %r>' % (self.url)

links = Table('links', metadata,
              Column('id', Integer, primary_key=True),
              Column('url', String(200)),
              Column('title', String(50)),
              Column('usage_count', Integer),
              Column('last_access', DateTime)
             )
mapper(Link, links)

class ReadLater(object):
    query = db_session.query_property()

    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.created = datetime.utcnow()
        self.reader = False

    def __repr__(self):
        return '<ReadLater: %r>' % self.url

read_later = Table('readlaters', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('url', String(200)),
                   Column('title', String(50)),
                   Column('created', DateTime),
                   Column('readed', Boolean)
                  )
mapper(ReadLater, read_later)
