from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Prize(Base):
    __tablename__ = "prizes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String)
    star_price = Column(Integer, default=1)

class UserPrize(Base):
    __tablename__ = "user_prizes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    prize_id = Column(Integer, ForeignKey("prizes.id"), nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    withdrawn = Column(Integer, default=0)  # 0 - не выведен, 1 - выведен

class UserSpins(Base):
    __tablename__ = "user_spins"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    spin_date = Column(DateTime, default=datetime.utcnow) 