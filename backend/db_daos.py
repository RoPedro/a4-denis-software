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
        
    def add_book(self, title, author, num_copies):
        transaction = None
        try:
            query = text(
                "INSERT INTO books (title, author, num_copies) VALUES (:title, :author, :num_copies);"
            )
            # Inicia a transação apenas se nenhuma transação estiver ativa
            if not self.connection.in_transaction():
                transaction = self.connection.begin()
            
            self.connection.execute(
                query,
                {
                    "title": title,
                    "author": author,
                    "num_copies": num_copies,
                },
            )
            
            if transaction:
                transaction.commit()  # Confirma a transação apenas se foi iniciada
            return True
        except Exception as e:
            if transaction:
                transaction.rollback()  # Cancela a transação apenas se foi iniciada
            print(f"Erro adicionando livro: {e}")
            return False
        
    def delete_book(self, book_id):
        transaction = None
        try:
            query = text("DELETE FROM books WHERE id = :book_id")
            
            if not self.connection.in_transaction():
                transaction = self.connection.begin()
            
            # Executa a query
            result = self.connection.execute(query, {"book_id": book_id})
            
            # Checa se algum registro foi modificado 
            if result.rowcount == 0:
                return False
            else:
                if transaction:
                    transaction.commit()  # Confirma a transação apenas se foi iniciada
                return True
        except Exception as e:
            if transaction:
                transaction.rollback()  # Cancela a transação apenas se foi iniciada
            print(f"Error deleting book by ID: {e}")
            return False 