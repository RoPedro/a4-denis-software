import logging
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

logger = logging.getLogger(__name__)
class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    author: Mapped[str] = mapped_column(String(128))
    num_copies: Mapped[int] = mapped_column()
        
    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, num_copies={self.num_copies}, id={self.id})"

    def __str__(self):
        return f"{self.title} by {self.author}, {self.num_copies} copies, ID: {self.id}"

"""
    Códigos para testar o backend vão aqui.
"""