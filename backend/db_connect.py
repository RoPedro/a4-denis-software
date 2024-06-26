from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging
import os

load_dotenv()

db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

logging.debug(f"DB URL: {db_url}")

engine = create_engine(db_url)