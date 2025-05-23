import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Author(db.Model):
    """Represents an author in the database.

     Attributes:
         id (int): Primary key identifier for the author.
         name (str): Full name of the author.
         birth_date (datetime.date): Author's date of birth.
         date_of_death (datetime.date, optional): Author's date of death (if applicable).
         books (list[Book]): Relationship to the books written by the author.

     Methods:
         __str__(): Returns the author's name as a string.
         __repr__(): Returns a string representation of the author instance.
     """

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[datetime.date] = mapped_column(nullable=False)
    date_of_death: Mapped[datetime.date] = mapped_column(nullable=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name}, birth_date={self.birth_date}, death={self.date_of_death})"


class Book(db.Model):
    """Represents a book in the database.

    Attributes:
        id (int): Primary key identifier for the book.
        isbn (str): ISBN of the book.
        title (str, optional): Title of the book.
        publication_year (int, optional): Year the book was published.
        author_id (int): Foreign key linking the book to its author.
        author (Author): Relationship to the author of the book.

    Methods:
        __str__(): Returns a string representation of the book with its ISBN.
        __repr__(): Returns a detailed string representation of the book instance.
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=True)
    publication_year: Mapped[int] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped["Author"] = relationship(back_populates="books")

    def __str__(self):
        return f"{self.title} (ISBN {self.isbn})"

    def __repr__(self):
        return f"Book(id={self.id}, isbn={self.isbn}, title={self.title}, year={self.publication_year}, author_id={self.author_id})"
