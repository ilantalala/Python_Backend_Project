from sqlalchemy import Column,Boolean,String,Integer,ForeignKey
from sqlalchemy.orm import relationship  
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__='posts'

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='TRUE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    rating = Column(Integer, nullable=True)
    owner_id=Column(Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    owner=relationship('User')
class User(Base):
    __tablename__='users'    
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))