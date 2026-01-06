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