from pathlib import Path
from .library import Library
from .models import Book
from .openlibrary_client import fetch_by_isbn, OpenLibraryError

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "library.json"


def menu():
    print("""
==== Kütüphane Uygulaması ====
1) Kitap Ekle (ISBN ile otomatik)
2) Kitap Sil
3) Kitapları Listele
4) Kitap Ara
5) Çıkış
""")


def add_book_flow(lib: Library):
    isbn = input("ISBN: ").strip()
    if not isbn:
        print("ISBN boş olamaz."); return
    try:
        data = fetch_by_isbn(isbn)
        title = data.get("title") or "Untitled"
        # authors alanı bazen list/dict/None olabilir
        author = "Unknown"
        authors = data.get("authors")
        if isinstance(authors, list) and authors:
            # bazı kayıtlarda authors listesinde dict -> {'key': '/authors/OL...'} olur
            # basitçe ilk elemanı string'e dönüştürelim
            author = authors[0].get('name') if isinstance(authors[0], dict) and 'name' in authors[0] else "Unknown"

        book = Book(title=title, author=author, isbn=isbn)
        lib.add_book(book)
        print(f"Eklendi: {book.title} – {book.author} (ISBN: {book.isbn})")
    except OpenLibraryError as e:
        print(f"Hata: {e}")
    except ValueError as e:
        print(f"Hata: {e}")


def remove_book_flow(lib: Library):
    isbn = input("Silinecek ISBN: ").strip()
    if lib.remove_book(isbn):
        print("Silindi.")
    else:
        print("Bulunamadı.")


def list_books_flow(lib: Library):
    books = lib.list_books()
    if not books:
        print("Kayıt yok.")
    for b in books:
        print(f"- {b.title} – {b.author} (ISBN: {b.isbn})")


def find_book_flow(lib: Library):
    isbn = input("Aranan ISBN: ").strip()
    b = lib.find_book(isbn)
    if b:
        print(f"Bulundu: {b.title} – {b.author} (ISBN: {b.isbn})")
    else:
        print("Bulunamadı.")


def main():
    lib = Library(DATA_PATH)
    while True:
        menu()
        choice = input("Seçim: ").strip()
        if choice == "1":
            add_book_flow(lib)
        elif choice == "2":
            remove_book_flow(lib)
        elif choice == "3":
            list_books_flow(lib)
        elif choice == "4":
            find_book_flow(lib)
        elif choice == "5":
            print("Çıkılıyor..."); break
        else:
            print("Geçersiz seçim.")


if __name__ == "__main__":
    main()
