from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import os

PROJECT_PATH = os.path.dirname(__file__)
DBPATH = 'sqlite:///' + os.path.join(PROJECT_PATH, 'sqlite.db')
engine = create_engine(DBPATH, convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
					 bind=engine))

def init_db():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

