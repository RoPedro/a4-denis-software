from db_connect import engine
from sqlalchemy import text

connection = engine.connect()

class Book:
    def __init__(self, title, author, num_copies, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.num_copies = num_copies

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