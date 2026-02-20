import logging
import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from dotenv import load_dotenv
from backend.db_livro import Base

logger = logging.getLogger(__name__)

load_dotenv()
# URL to connect to postgres
db_url = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
)

DB_NAME = os.getenv('POSTGRES_DB') # Separate DB name from the URL so we can have a test DB
engine = create_engine(f"{db_url}{DB_NAME}", echo=True)

if not database_exists(engine.url):
    logger.debug(f"DB URL: {db_url}{os.getenv('POSTGRES_DB')}")
    logger.error("[ERROR] Database does not exist.")
   
def init_db():
    Base.metadata.create_all(bind=engine) 
