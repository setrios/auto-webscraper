from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime

metadata_obj = MetaData()

advertisement_table = Table(
    'advertisement',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('url', String),
    Column('title', String),
    Column('price_usd', Integer),
    Column('odometr', Integer),
    Column('username', String),
    Column('phone_number', String),
    Column('image_url', String),
    Column('image_count', Integer),
    Column('car_number', String),
    Column('car_vin', String),
    Column('datetime_found', DateTime),
)