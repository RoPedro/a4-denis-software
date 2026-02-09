import pytest
import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker, scoped_session


# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app as test_app
from backend.db_connect import engine

@pytest.fixture
def app():
    test_app.config['TESTING'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False  # if using forms
    
    connection = engine.connect() # The engine here HAS the URL, so we just need to "Connect to the URL" 
    transaction = connection.begin()
    Session = scoped_session(sessionmaker(bind=connection))

    yield test_app
    Session.remove()
 
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app):
    return app.test_client()


