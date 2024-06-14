from db_connect import engine
from sqlalchemy import text

connection = engine.connect()

result = connection.execute(text("SELECT * FROM books;"))
for row in result:
    print(row)