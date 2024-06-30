from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_uri import database_uri

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

def db_connection():
    mysql_engine = create_engine(database_uri(), pool_size=1000, pool_recycle=3600, max_overflow=0)
    Session = sessionmaker(bind=mysql_engine)
    session = Session()
    return session