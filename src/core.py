from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import engine, SessionLocal
from models import Base, Advertisement
from pydantic_models import CarListing
from typing import List


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Tables created successfully')


def pydantic_to_sqlalchemy(car):
    return Advertisement(
        url=car.url,
        title=car.title,
        price_usd=car.price_usd,
        odometer=car.odometer,
        username=car.username,
        phone_number=car.phone_number,
        image_url=car.image_url,
        images_count=car.images_count,
        car_number=car.car_number,
        car_vin=car.car_vin,
        datetime_found=car.datetime_found
    )


def insert_car(db, car):

    db_car = pydantic_to_sqlalchemy(car)
    
    try:
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        print(f'Inserted: {car.title}')
        return db_car
    except IntegrityError:
        db.rollback()
        print(f'Duplicate URL skipped: {car.url}')
        return None


def insert_cars_bulk(db, cars):

    inserted_count = 0
    
    for car in cars:
        db_car = pydantic_to_sqlalchemy(car)
        
        try:
            db.add(db_car)
            db.commit()
            inserted_count += 1
            print(f'Inserted {inserted_count}/{len(cars)}: {car.title}')
        except IntegrityError:
            db.rollback()
            print(f'Duplicate URL skipped: {car.url}')
    
    return inserted_count


def get_all_cars(db):
    return db.query(Advertisement).all()


def get_car_by_url(db, url):
    return db.query(Advertisement).filter(Advertisement.url == url).first()


def delete_all_cars(db):
    db.query(Advertisement).delete()
    db.commit()
    print('All records deleted')