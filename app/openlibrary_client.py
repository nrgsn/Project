import httpx

OPENLIBRARY_URL = "https://openlibrary.org/isbn/{isbn}.json"


class OpenLibraryError(Exception):
    pass


def fetch_by_isbn(isbn: str) -> dict:
    try:
        resp = httpx.get(OPENLIBRARY_URL.format(isbn=isbn), timeout=10.0)
        if resp.status_code == 404:
            raise OpenLibraryError("Kitap bulunamadı (404).")
        resp.raise_for_status()
        return resp.json()
    except httpx.RequestError as e:
        raise OpenLibraryError(f"Ağ hatası: {e}") from e
    except httpx.HTTPStatusError as e:
        raise OpenLibraryError(f"HTTP hatası: {e}") from e
