from flask import jsonify
from sqlalchemy_utils import database_exists
from functools import wraps
from backend.db_daos import BookDAO
from backend.db_connect import engine

def require_db(f):
    dao = BookDAO(engine)
    @wraps(f)
    def db_check(*args, **kwargs):
        if not database_exists(dao.engine.url):
            return jsonify({'status': 'error', 'message': 'Database connection not found.'}), 503
        return f (*args, **kwargs)
    return db_check
