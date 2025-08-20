from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_get_books_empty(monkeypatch, tmp_path):
    # Force library path to tmp by patching DATA_PATH in api module
    from app import api as api_module
    api_module.DATA_PATH = tmp_path / "lib.json"

    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

def test_post_conflict(monkeypatch, tmp_path):
    # Patch DATA_PATH to tmp and mock fetch_by_isbn
    from app import api as api_module
    api_module.DATA_PATH = tmp_path / "lib.json"

    def fake_fetch(isbn: str):
        return {"title": "Mock Book", "authors": [{"name": "Mock Author"}]}

    monkeypatch.setattr(api_module, "fetch_by_isbn", fake_fetch)

    # First create
    r1 = client.post("/books", json={"isbn": "111"})
    assert r1.status_code == 201

    # Duplicate -> 409
    r2 = client.post("/books", json={"isbn": "111"})
    assert r2.status_code == 409
