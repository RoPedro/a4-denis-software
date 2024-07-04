from sqlalchemy import text
from backend.db_livro import Book
import logging

# Inicializando LOGS
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            
            logger.info(f"Tabela recuperada com sucesso." )
            return book_list
            
        except Exception as e:
            logger.error(f"Erro ao recuperar a tabela: {e}")
            print(e)
            return []
        
    def list_authors(self): # Retorna uma lista com todos os autores
        try:
            # Inicializando LOGS
            logging.basicConfig(level=logging.INFO)
             
            query = text("SELECT DISTINCT author FROM books;")
            result = self.connection.execute(query)
            
            # Popula uma lista com os autores
            author_list = []
            for row in result:
                author = row[0]
                author_list.append(author)
            
            
            return author_list
            
        except Exception as e:
            print(e)
            return []
    
    # Adiciona um novo livro 
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
                logger.info(f"Novo livro adicionado com sucesso.")
            return True
        except Exception as e:
            if transaction:
                transaction.rollback()  # Cancela a transação apenas se foi iniciada
                logger.error(f"ROLLBACK acionado, erro adicionando novo livro: {e}")
            print(f"Erro adicionando livro: {e}")
            return False
    
    # Exclui um livro pelo ID
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
                logger.info("Nenhum registro foi modificado. rowcount = 0")
            else:
                if transaction: # Confirma a transação apenas se foi iniciada
                    transaction.commit() # Confirma a transação
                    logger.info(f"Novo livro excluído com sucesso.")
                return True
        except Exception as e:
            print(f"Error deleting book by ID: {e}")
            logger.error(f"ROLLBACK acionado, erro excluindo novo livro: {e}")
            transaction.rollback()
            return False 
    
    # Atualiza um livro (Todos os dados são opcionais, atualização parcial permitida)
    def update_book(self,
                    book_id,
                    new_title=None,
                    new_author=None,
                    new_num_copies=None
                    ):
        transaction = None 
        try:
            updates = []
            params = {"book_id": book_id}

            if new_title is not None:
                updates.append("title = :new_title")
                params["new_title"] = new_title
            if new_author is not None:
                updates.append("author = :new_author")
                params["new_author"] = new_author
            if new_num_copies is not None:
                updates.append("num_copies = :new_num_copies")
                params["new_num_copies"] = new_num_copies

            if updates:
                query_string = f"UPDATE books SET {', '.join(updates)} WHERE id = :book_id"
                query = text(query_string)
                
                if not self.connection.in_transaction(): 
                    transaction = self.connection.begin()
                    
                self.connection.execute(query, params)
                
                if transaction:
                    transaction.commit()
                    logger.info(f"Novo livro atualizado com sucesso.")
                return True
        except Exception as e:
            print(f"Erro atualizando livro: {e}")
            if transaction:
                transaction.rollback()
                logger.error(f"ROLLBACK acionado, erro atualizando livro: {e}")
            return False