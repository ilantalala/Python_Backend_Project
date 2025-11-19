from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL='postgresql://fastapi_database_8lk5_user:YURVuJwhn2RPlg6zcje1bjBlrSU2pjtq@dpg-d44vanngi27c73ajqjt0-a/fastapi_database_8lk5'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

