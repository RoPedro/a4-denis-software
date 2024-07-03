from db_queries import Book

class BookDAO:

    def __init__(self):
        pass

    def get_all_books(self):
        return Book.list_all()
    
    def add_book(self, title, author, num_copies):
        return Book.add_book(title, author, num_copies)
    
    def delete_book(self, book_id):
        return Book.delete_book(book_id)
    
    def update_book_details(self, book_id, new_title, new_author):
        return Book.update_book_details(book_id, new_title, new_author)
    
    def update_num_copies(self, book_id, new_num_copies):
        return Book.update_num_copies(book_id, new_num_copies)