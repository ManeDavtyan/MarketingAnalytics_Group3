from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional
from fuzzywuzzy import fuzz

# Define your SQLAlchemy models
Base = declarative_base()

from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    language: Optional[str] = None
    cover_type: Optional[str] = None
    pages_number: Optional[int] = None
    book_id: int

# Connect to the database (replace 'sqlite:///./test.db' with your database connection string)
DATABASE_URL = "sqlite:///./BookStore.db"
engine = create_engine(DATABASE_URL)

# Create a Session class for the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Create a FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "BookStore API"}

@app.get("/books/")
def get_books(db: SessionLocal = Depends(get_db)):
    return db.query(Book).all()

@app.get("/books/{title}")
def get_book(title: str, db: SessionLocal = Depends(get_db)):
    matching_books = get_matching_books(title)
    if not matching_books:
        raise HTTPException(status_code=404, detail="Book not found")
    return matching_books

@app.put("/books/{title}", response_model=None)
def update_book(title: str, book: Book, db: SessionLocal = Depends(get_db)):
    matching_books = get_matching_books(title, db)
    if not matching_books:
        raise HTTPException(status_code=404, detail="Book not found")

    for matched_book in matching_books:
        for field, value in book.dict(exclude_unset=True).items():
            if value is not None:
                setattr(matched_book, field, value)

    db.commit()
    return {"title": title, "message": "Book updated successfully"}

@app.post("/books/", response_model=Book)
def create_book(book: Book, db: SessionLocal = Depends(get_db)):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_matching_books(title: str, db: SessionLocal = Depends(get_db)):
    threshold = 80
    return db.query(Book).filter(fuzz.token_sort_ratio(Book.title, title) > threshold).all()
