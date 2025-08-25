from sqlalchemy import create_engine,Column, Integer, String, DateTime, func,Boolean,TIMESTAMP
from sqlalchemy.orm import declarative_base
from database import Base_model


class Posts_table(Base_model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable= False)
    published = Column(Boolean,nullable= False,server_default = "TRUE")
    created_at = Column(DateTime(timezone=True),nullable= False,server_default=func.now())