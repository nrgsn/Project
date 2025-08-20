from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .library import Library
from .models import Book
from .openlibrary_client import fetch_by_isbn, OpenLibraryError

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "library.json"
app = FastAPI(title="Python 202 Library API", version="1.0.0")

class ISBNBody(BaseModel):
    isbn: str

@app.get("/books", response_model=list[Book])
def get_books():
    lib = Library(DATA_PATH)
    return lib.list_books()

@app.post("/books", response_model=Book, status_code=201)
def create_book(body: ISBNBody):
    lib = Library(DATA_PATH)
    try:
        data = fetch_by_isbn(body.isbn)
        title = data.get("title") or "Untitled"
        author = "Unknown"
        authors = data.get("authors")
        if isinstance(authors, list) and authors:
            author = authors[0].get('name') if isinstance(authors[0], dict) and 'name' in authors[0] else "Unknown"
        book = Book(title=title, author=author, isbn=body.isbn)
        return lib.add_book(book)
    except OpenLibraryError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.delete("/books/{isbn}", status_code=204)
def delete_book(isbn: str):
    lib = Library(DATA_PATH)
    ok = lib.remove_book(isbn)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return
