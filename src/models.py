from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = 'advertisement'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    price_usd = Column(Integer, default=0)
    odometer = Column(Integer, default=0)
    username = Column(String, nullable=False)
    phone_number = Column(BigInteger, default=0)  # as numbers like 380932722406 cause 4 byte int overflow
    image_url = Column(String, nullable=False)
    images_count = Column(Integer, default=0)
    car_number = Column(String, nullable=False)
    car_vin = Column(String, nullable=False)
    datetime_found = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Advertisement(id={self.id}, title='{self.title}', price=${self.price_usd})>"