import logging

logger = logging.getLogger(__name__)
class Book:
    def __init__(self, title, author, num_copies, id=None):
        self.id = id
        self.title = title
        self.author = author
        
        if not isinstance(num_copies, int):
            logger.error("num_copies must be an integer")
            raise TypeError("num_copies must be an integer")
        self.num_copies = num_copies
        
    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, num_copies={self.num_copies}, id={self.id})"

    def __str__(self):
        return f"{self.title} by {self.author}, {self.num_copies} copies, ID: {self.id}"

"""
    Códigos para testar o backend vão aqui.
"""