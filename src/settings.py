from dotenv import load_dotenv
from pathlib import Path
import os

project_root = Path(__file__).parent.parent
dotenv_path = project_root / '.env'

load_dotenv(dotenv_path)

DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=int(os.getenv('DB_PORT'))

# Synchronous connection URL (uses psycopg by default in SQLAlchemy 2.0+)
SYNC_DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Asynchronous connection URL
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
