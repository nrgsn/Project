from pathlib import Path
from app.library import Library
from app.models import Book

def test_add_and_find_book(tmp_path: Path):
    lib = Library(tmp_path / "lib.json")
    b = Book(title="Test", author="Me", isbn="123")
    lib.add_book(b)
    assert lib.find_book("123") is not None

def test_remove_book(tmp_path: Path):
    lib = Library(tmp_path / "lib.json")
    b = Book(title="Test", author="Me", isbn="123")
    lib.add_book(b)
    assert lib.remove_book("123") is True
    assert lib.find_book("123") is None
