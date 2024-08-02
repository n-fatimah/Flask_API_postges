from typing import Union
from .base import Base, db
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "book"
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    available_quantity = Column(Integer, nullable=False, default=1)

    issued_books = relationship("IssuedBook", back_populates="book")

    @classmethod
    def get_by_title_author(
        cls, book_id: int, title: str, author: str
    ) -> Union["Book", None]:
        """
        Get Book by title and author

        Args:
            title: book title and author

        Returns:
            Book
        """
        return (
            db.session.query(cls)
            .filter(Book.title == title, Book.author == author, Book.id != book_id)
            .first()
        )

    @classmethod
    def get_all_available(cls, page: int, per_page: int):
        """
        Get all available based on their available quantity

        Returns:
            List
        """

        return (
            db.session.query(cls)
            .filter(cls.available_quantity > 0)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
