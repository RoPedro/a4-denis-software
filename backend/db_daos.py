import logging
from sqlalchemy import text
from backend.db_livro import Book
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, delete, update

logger = logging.getLogger(__name__)

class BookDAO:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        
    def list_all(self):
        session = self.Session()
        try:
            stmt = select(Book)
            book_list = session.execute(stmt).scalars().all() # scalars() because only 1 entity is fetchand execute works with tuples by default.
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
            stmt = select(Book.author).distinct()
            result = session.execute(stmt).all() # We expect tuples here so no scalars().
            logger.debug(f"AUTHORS (Truncated): {str(result)[:20]}")
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
            stmt = select(Book).filter_by(author = author_name) # Use = to assign author to author_name
            book_list = session.execute(stmt).scalars().all()
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
            transaction = session.begin()
            
            stmt = insert(Book).values(title = title, author = author, num_copies = num_copies)
            session.execute(stmt)
            logger.info("Novo livro adicionado com sucesso.")
            logger.debug(
                f"""Livro adicionado - 
                Título: {title},
                Autor: {author},
                Número de Cópias: {num_copies}"""
            )
            
            transaction.commit()
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
            if not session.in_transaction():
                transaction = session.begin()

            # Executa a query
            stmt = delete(Book).where(Book.id == book_id) # Use == because we need to match, not assign.
            session.execute(stmt)

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

    
    # All arguments are optional, so to enable partial updates we set all new_* to None.
    def update_book(self, book_id, new_title=None, new_author=None, new_num_copies=None):
        session = self.Session()
        try:
            stmt = update(Book).where(Book.id == book_id).values(title = new_title, author = new_author, num_copies = new_num_copies)
            session.execute(stmt)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"ROLLBACK acionado, erro atualizando livro: {e}")
            return False
        finally:
            session.close()