import logging
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

load_dotenv()
# URL to connect to postgres
db_url = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

logger.debug(f"DB URL: {db_url}")

engine = create_engine(db_url)
if not database_exists(engine.url):
    logger.error("[ERROR] Database does not exist.")
    
