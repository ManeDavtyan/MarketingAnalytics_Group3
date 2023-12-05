#Connecting to DB

import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

# Define the path to the SQLite database
db_path = ".//BookStore.db"


# Create a context manager for connecting to the database
def get_db():
    db = sqlite3.connect(db_path)
    yield db
    db.close()


class Book(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    language: Optional[str] = None
    cover_type: Optional[str] = None
    pages_number: Optional[int] = None
    book_id: int


@app.get("/")
def read_root():
    return {"message": "BookStore API"}


# @app.get("/books/")
# def get_books(db: sqlite3.Connection = Depends(get_db)):
#     # Fetch data from the database instead of the CSV file
#     query = "SELECT * FROM books"
#     books_data = pd.read_sql_query(query, db)
#     return books_data.to_dict(orient="records")


@app.get("/books/{title}")
def get_book(title: str, db: sqlite3.Connection = Depends(get_db)):
    # Fetch data from the database instead of the CSV file
    query = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
    matching_books = pd.read_sql_query(query, db)

    if matching_books.empty:
        raise HTTPException(status_code=404, detail="Book not found")

    return matching_books.to_dict(orient="records")



@app.put("/books/{title}")
def update_book(title: str, book: Book, db: sqlite3.Connection = Depends(get_db)):
    # Fetch data from the database for the specified title
    query = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
    matching_books = pd.read_sql_query(query, db)

    if matching_books.empty:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update the first matching book found (you can modify this logic if needed)
    row = matching_books.iloc[0].copy()  # Create a copy of the row

    for field, value in book.dict(exclude_unset=True).items():
        if field != "book_id" and value is not None:
            row[field] = value

    # Update the row in the database
    update_query = (
        "UPDATE books SET " +
        ", ".join([f'{field} = ?' for field in row.index]) +
        f" WHERE book_id = ?"
    )
    # Pass the values as a tuple, including the book_id
    values = tuple(row) + (row['book_id'],)
    db.execute(update_query, values)
    db.commit()  # Add this line to commit the change
    return {"title": title, **row.to_dict()}

@app.post("/books/", response_model=Book)
def create_book(book: Book, db: sqlite3.Connection = Depends(get_db)):
    # Get the maximum book_id from the database
    max_book_id_query = "SELECT MAX(book_id) FROM books"
    max_book_id = pd.read_sql_query(max_book_id_query, db).iloc[0, 0]
    new_book_id = max_book_id + 1 if max_book_id is not None else 1

    # Set the book_id for the new book
    book.book_id = new_book_id

    # Insert the new book into the database
    # Assuming `values` is a tuple of values to be inserted
    insert_query = (
        "INSERT INTO books (book_id, title, price, isbn, publication_year, language, "
        "\"cover_type\", pages_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )

    # Ensure the values match the expected data types
    values = (
        book.book_id,  # number
        book.title,  # string
        book.price,  # number
        book.isbn,  # string
        book.publication_year,  # number
        book.language,  # string
        book.cover_type,  # string
        book.pages_number  # number
    )

    # Execute the query with parameterized values
    db.execute(insert_query, values)

    return book