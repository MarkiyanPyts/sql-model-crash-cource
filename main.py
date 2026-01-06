from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship

engine = create_engine("sqlite:///orm.db")

class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=50, unique=True)

    books: list["Book"] = Relationship(back_populates="author")

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str
    author_id: int = Field(foreign_key="author.id")

    author: Author = Relationship(back_populates="books")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    author1 = Author(name="Jane Doe", email="alice@example.com")
    author2 = Author(name="John Smith", email="john@example.com")
    book1 = Book(title="First Book", content="Content of the first book", author=author1)
    book2 = Book(title="Second Book", content="Content of the second book", author=author1)
    book3 = Book(title="Third Book", content="Content of the third book", author=author2)

    session.add_all([author1, author2, book1, book2, book3])
    session.commit()

with Session(engine) as session:
    # statement = select(Book).where(Book.title == "First Book")
    # statement = select(Book, Author).join(Author)
    # books_with_authors = session.exec(statement).all()
    # for book, author in books_with_authors:
    #     print(f"Book: {book.title}, Author: {author.name}")
    book_to_update = session.exec(select(Book).where(Book.title == "Second Book")).first()
    if book_to_update:
        book_to_update.content = "Updated content of the second book"
        session.add(book_to_update)
        session.commit()
        session.refresh(book_to_update)
        print(f"Updated Book: {book_to_update.title}, New Content: {book_to_update.content}")

    book_to_delete = session.exec(select(Book).where(Book.title == "Third Book")).first()
    if book_to_delete:
        session.delete(book_to_delete)
        session.commit()
        print(f"Deleted Book: {book_to_delete.title}")
