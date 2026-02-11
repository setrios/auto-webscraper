from sqlalchemy import text
from database import engine
from models import metadata_obj


def create_tables():
    metadata_obj.drop_all(engine)
    metadata_obj.create_all(engine)