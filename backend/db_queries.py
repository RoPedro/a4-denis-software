from db_connect import engine
from sqlalchemy import text

connection = engine.connect()

class Book:
    def __init__(self, title, author, num_copies, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.num_copies = num_copies

    # Método para listar todos os livros
    @classmethod
    def list_all(cls):
        try:
            query = text("SELECT title, author, num_copies, id FROM books;")
            result = connection.execute(query)
            
            book_list = []
            for row in result:
                book = cls(*row)
                book_list.append(book)
            
            return book_list
            
        except Exception as e:
            print(e)
            return []
    
    # Método para adicionar um novo livro 
    @classmethod
    def add_book(cls, title, author, num_copies):
        try:
            with engine.begin() as conn: # Begin para começar uma transação
                query = text(
                    "INSERT INTO books (title, author, num_copies) VALUES (:title, :author, :num_copies);"
                    )
                conn.execute(query, {"title": title, "author": author, "num_copies": num_copies})  # Pass parameters as a dictionary
            return True
        except Exception as e:
            print(f"Erro adicionando livro: {e}")
            return False
    
    # Método para excluir um livro por ID
    @classmethod
    def delete_book(cls, book_id):
        try:
            with engine.begin() as conn: # Begin para começar uma transação
                query = text("DELETE FROM books WHERE id = :book_id")
                conn.execute(query, {"book_id": book_id})
            return True
        except Exception as e:
            print(f"Error deleting book by ID: {e}")
            return False 
   
    # Método para atualizar o título e o autor
    @classmethod
    def update_title_author(cls, book_id, new_title=None, new_author=None):
        try:
            with engine.begin() as conn:
                updates = []
                params = {"book_id": book_id}
                
                if new_title is not None:
                    updates.append("title = :new_title")
                    params["new_title"] = new_title
                if new_author is not None:
                    updates.append("author = :new_author")
                    params["new_author"] = new_author
                    
                if updates:
                    query_string = f"UPDATE books SET {', '.join(updates)} WHERE id = :book_id"
                    query = text(query_string)
                    conn.execute(query, params)
                    return True
        except Exception as e:
            print(f"Erro atualizando livro: {e}")
            return False
        
    # Método para atualizar o número de cópias de um livro
    def update_num_copies(cls, book_id, new_num_copies):
        try:
            with engine.begin() as conn:
                query = text(
                    "UPDATE books SET num_copies = :new_num_copies WHERE id = :book_id"
                )
                conn.execute(query, {"new_num_copies": new_num_copies, "book_id": book_id})
                
        except Exception as e:
            print(f"Erro atualizando livro: {e}")
            return False

"""
    Códigos para testar o backend vão aqui.
"""