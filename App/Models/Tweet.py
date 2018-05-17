from sqlalchemy import Column, DateTime, String, Integer
# from sqlalchemy.orm import relationship, backref
from Models.base import Base

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    text = Column(String(300))
    positive_words = Column(Integer)
    negative_words = Column(Integer)
    date = Column(DateTime)
