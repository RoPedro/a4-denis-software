import pytest
import sys
import os
from pathlib import Path
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from dotenv import load_dotenv

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app as test_app
from backend.db_connect import db_url

load_dotenv()
DB_NAME = os.getenv('DB_TEST')

@pytest.fixture
def app():
    test_app.config['TESTING'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False  # if using forms
    
    test_engine = create_engine(f"{db_url}{DB_NAME}", echo=True)
    
    if not database_exists(test_engine.url):
        create_database(test_engine.url)
        
    connection = test_engine.connect() # The engine here HAS the URL, so we just need to "Connect to the URL" 
    
    transaction = connection.begin()
    Session = scoped_session(sessionmaker(bind=connection))

    yield test_app
    Session.remove()
 
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app):
    return app.test_client()


