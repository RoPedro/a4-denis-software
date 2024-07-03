from sqlalchemy import text
from db_queries import Book

class BookDAO:
    def __init__(self, connection):
        self.connection = connection
        
    def list_all(self): # Retorna uma lista com todos os livros
        try:
            query = text("SELECT title, author, num_copies, id FROM books;")
            result = self.connection.execute(query)
            
            # Popula uma lista com os livros
            book_list = []
            for row in result:
                book = Book(*row)
                book_list.append(book)
            
            return book_list
            
        except Exception as e:
            print(e)
            return []