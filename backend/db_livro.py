from db_connect import engine
from sqlalchemy import text

connection = engine.connect()

class Book:
    def __init__(self, title, author, num_copies, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.num_copies = num_copies

"""
    Códigos para testar o backend vão aqui.
"""