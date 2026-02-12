from pydantic import BaseModel, Field, field_validator
import re 
from datetime import datetime

class CarListing(BaseModel):
    url: str = ''
    title: str = ''
    price_usd: int = 0
    odometer: int = 0
    username: str = ''
    phone_number: int = 0
    image_url: str = ''
    images_count: int = 0
    car_number: str = ''
    car_vin: str = ''
    datetime_found: datetime = Field(default_factory=datetime.now)

    @field_validator('title', mode='before')
    @classmethod
    def convert_title(cls, v):
        if not v:
            return 'Title not found'
        return v

    @field_validator('price_usd', mode='before')
    @classmethod
    def convert_price_usd(cls, v):
        if not v:
            return 0
        v = re.sub(r'[^0-9]+', '', v)
        try:
            return int(v)
        except:
            return 0

    @field_validator('odometer', mode='before')
    @classmethod
    def convert_odometer(cls, v):
        if not v:
            return 0
        v = re.sub(r'[^0-9]+', '', v)
        try:
            return int(v) * 1000
        except:
            return 0
    
    @field_validator('username', mode='before')
    @classmethod
    def convert_username(cls, v):
        if not v:
            return 'Username not found'
        return v
    
    @field_validator('image_url', mode='before')
    @classmethod
    def convert_image_url(cls, v):
        if not v:
            return 'Image url not found'
        return v

    @field_validator('images_count', mode='before')
    @classmethod
    def convert_images_count(cls, v):
        if not v:
            return 0
        try:
            return int(v)
        except:
            return 0
        
    @field_validator('car_number', mode='before')
    @classmethod
    def convert_car_number(cls, v):
        if not v:
            return 'Seller did not provide car number'
        return v
    
    @field_validator('car_vin', mode='before')
    @classmethod
    def convert_car_vin(cls, v):
        if not v:
            return 'Seller did not provide car vin'
        return v

    
    @field_validator('phone_number', mode='before')
    @classmethod
    def convert_phone(cls, v):
        if not v:
            return 0
        v = re.sub(r'[^0-9]+', '', v)
        v = '38' + v
        try:
            return int(v)
        except:
            return 0