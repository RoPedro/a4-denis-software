import logging
from sqlalchemy import text
from backend.db_livro import Book
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class BookDAO:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        
    def list_all(self):
        session = self.Session()
        try:
            query = text("SELECT id, title, author, num_copies FROM books;")
            result = session.execute(query).fetchall()
            book_list = [Book(id=row[0], title=row[1], author=row[2], num_copies=row[3]) for row in result]
            logger.info("Tabela recuperada com sucesso.")
            return book_list
        except Exception as e:
            logger.error(f"Erro ao recuperar a tabela: {e}")
            print(e)
            return []
        finally:
            session.close()
        
    def list_authors(self):
        session = self.Session()
        try:
            query = text("SELECT DISTINCT author FROM books;")
            result = session.execute(query).fetchall()
            authors = [{"id": i + 1, "name": author[0]} for i, author in enumerate(result)]
            logger.info("Autores recuperados com sucesso.")
            return authors
        except Exception as e:
            logger.error(f"Erro ao recuperar a lista de autores: {e}")
            print(e)
            return []
        finally:
            session.close()
            
    def list_books_by_author(self, author_name):
        session = self.Session()
        try:
            logger.info("Trying to connect to database...")
            query = text("SELECT id, title, author, num_copies FROM books WHERE author = :author_name;")
            result = session.execute(query, {"author_name": author_name}).fetchall()
            book_list = [Book(id=row[0], title=row[1], author=row[2], num_copies=row[3]) for row in result]
            logger.info(f"Retrieved {len(book_list)} books for author '{author_name}'.")
            return book_list
        except Exception as e:
            logger.error(f"Error retrieving books for author '{author_name}': {e}")
            return []
        finally:
            session.close()
             
    # Adiciona um novo livro 
    def add_book(self, title, author, num_copies):
        session = self.Session()
        transaction = None
        try:
            query = text(
                "INSERT INTO books (title, author, num_copies) VALUES (:title, :author, :num_copies);"
            )
            transaction = session.begin()

            session.execute(
                query,
                {
                    "title": title,
                    "author": author,
                    "num_copies": num_copies,
                },
            )

            # Confirma a transação
            transaction.commit()
            logger.info("Novo livro adicionado com sucesso.")
            logger.debug(
                f"""Livro adicionado - 
                Título: {title},
                Autor: {author},
                Número de Cópias: {num_copies}"""
            )
            return True
        except Exception as e:
            if transaction:
                transaction.rollback() # Rollback pra manter a integridade caso falhe 
                logger.error(f"ROLLBACK acionado, erro adicionando novo livro: {e}")
            logger.error(f"Erro adicionando livro: {e}")
            return False
        finally:
            session.close()
    
    # Exclui um livro pelo ID
    def delete_book(self, book_id):
        session = self.Session()
        transaction = None
        try:
            query = text("DELETE FROM books WHERE id = :book_id")

            if not session.in_transaction():
                transaction = session.begin()

            # Executa a query
            session.execute(query, {"book_id": book_id})

            if transaction:  # Confirma a transação apenas se foi iniciada
                transaction.commit()  # Confirma a transação
                logger.info(f"Livro com ID {book_id} excluído com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Erro excluindo livro pelo ID: {e}")
            logger.info(f"ROLLBACKING transaction for book ID: {book_id}")
            if transaction:
                transaction.rollback()
            return False
        finally:
            session.close()

    
    # Atualiza um livro (Todos os dados são opcionais, atualização parcial permitida)
    def update_book(self, book_id, new_title=None, new_author=None, new_num_copies=None):
        session = self.Session()
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
                session.execute(query, params)
                session.commit()
                logger.info(f"Livro com ID {book_id} atualizado com sucesso.")
                return True
            else:
                logger.warning(f"Nenhuma atualização fornecida para o livro com ID {book_id}.")
                return False
        except Exception as e:
            session.rollback()
            logger.error(f"ROLLBACK acionado, erro atualizando livro: {e}")
            return False
        finally:
            session.close()