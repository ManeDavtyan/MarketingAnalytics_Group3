import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional
import sqlite3
from bookstore.model.model import get_combined_recommendations

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
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None

@app.get("/")
def read_root():
    return {"message": "BookStore API"}


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
    cursor = db.cursor()
    cursor.execute(query)
    matching_books = cursor.fetchall()

    if not matching_books:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update the first matching book found (you can modify this logic if needed)
    book_data = book.dict(exclude={"book_id"})  # Exclude book_id as it shouldn't be updated

    update_query = f'''
        UPDATE books
        SET price = ?
        WHERE book_id = ?
    '''

    # Update the book data in the database
    update_values = (book_data['price'] , matching_books[0][0])
    cursor.execute(update_query, update_values)
    db.commit()

    return {"price": book_data['price']}



@app.post("/books/", response_model=Book)
def create_book(book: Book, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Prepare the INSERT query using parameterized values
        insert_query = (
            "INSERT INTO books (title, price, isbn, publication_year, language, "
            "cover_type, pages_number) VALUES (?, ?, ?, ?, ?, ?, ?)"
        )

        # Ensure the values match the expected data types
        values = (
            book.title,
            book.price,
            book.isbn,
            book.publication_year,
            book.language,
            book.cover_type,
            book.pages_number
        )

        # Execute the query with parameterized values
        db.execute(insert_query, values)
        db.commit()  # Commit the transaction to the database

        return book
    except sqlite3.Error as e:
        # Handle any potential errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/recommendations/{title}")
def get_recommendations(title: str, db: sqlite3.Connection = Depends(get_db)):
    recommendations = get_combined_recommendations(title, db_path)

    if recommendations.empty:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return recommendations.to_dict(orient="records")