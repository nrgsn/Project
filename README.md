# Python 202 – OOP → API Projesi (Kütüphane)

Bu proje **OOP → Harici API → FastAPI** adımlarıyla ilerleyen basit bir kütüphane uygulamasıdır.
- **Aşama 1 (OOP)**: `Book` ve `Library` sınıfları, JSON dosyasında veri saklama, CLI.
- **Aşama 2 (Harici API)**: Open Library ile ISBN'den kitap bilgisi çekme.
- **Aşama 3 (FastAPI)**: Kütüphane işlevlerini HTTP endpoint'lerine açma.

## Kurulum
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Çalıştırma
### 1) CLI (Aşama 1-2)
```bash
python app/main.py
```

### 2) API (Aşama 3)
```bash
uvicorn app.api:app --reload
```
Tarayıcı: <http://127.0.0.1:8000/docs>

## Dosya Yapısı
```
python202_library_api/
├─ app/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ library.py
│  ├─ openlibrary_client.py
│  ├─ main.py
│  └─ api.py
├─ data/
│  └─ library.json
├─ requirements.txt
└─ app/tests/
   ├─ test_library.py
   └─ test_api.py
```

## Notlar
- `data/library.json` veri dosyası otomatik oluşur.
- İnternet hatalarında CLI ve API anlamlı hata döndürür.
- Testlerde (özellikle `test_api.py`) basit örnekler ve mocking gösterilmiştir.
