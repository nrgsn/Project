import json
from pathlib import Path
from typing import List, Optional
from .models import Book


class Library:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._books: List[Book] = []
        self.load_books()

    # ---------- Persistence ----------
    def load_books(self) -> None:
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self._books = [Book(**b) for b in data]
            except Exception:
                # Corrupt file fallback
                self._books = []
        else:
            self._books = []
            self.save_books()

    def save_books(self) -> None:
        data = [b.model_dump() for b in self._books]
        self.storage_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------- Operations ----------
    def list_books(self) -> List[Book]:
        return list(self._books)

    def find_book(self, isbn: str) -> Optional[Book]:
        for b in self._books:
            if b.isbn == isbn:
                return b
        return None

    def add_book(self, book: Book) -> Book:
        if self.find_book(book.isbn):
            raise ValueError(f"Book with ISBN {book.isbn} already exists.")
        self._books.append(book)
        self.save_books()
        return book

    def remove_book(self, isbn: str) -> bool:
        before = len(self._books)
        self._books = [b for b in self._books if b.isbn != isbn]
        removed = len(self._books) != before
        if removed:
            self.save_books()
        return removed
