# URL Shortener API

A lightweight URL Shortener built with FastAPI, SQLModel, and SQLite.

## Features

* Create shortened URLs
* Redirect users using short codes
* Unique short code generation
* Database persistence with SQLModel
* Automatic UUID-based records
* URL validation using Pydantic
* Clean service-layer architecture
* Database transaction handling and rollback support
* Expiration support (planned)
* User authentication support (planned)

---

## Tech Stack

* FastAPI
* SQLModel
* SQLite
* Pydantic
* Uvicorn

---

## Project Structure

```text
app/
├── api/
│   └── v1/
│       └── url_shortner.py
│
├── db/
│   ├── schema.py
│   └── session.py
│
├── models/
│   └── shortner_models.py
│
├── services/
│   └── url_shortner.py
│
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone git@github.com:AdityaManojShinde/Url_Shortner_API.git
cd url-shortener
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

Server starts at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "Api running"
}
```

---

### Create Short URL

```http
POST /shortner/
```

Request:

```json
{
  "url": "https://example.com"
}
```

Response:

```json
{
  "url": "https://example.com",
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123"
}
```

---

### Redirect to Original URL

```http
GET /{short_code}
```

Example:

```http
GET /abc123
```

Response:

```text
307 Temporary Redirect
```

---

## Database Schema

### User

| Field         | Type     |
| ------------- | -------- |
| id            | UUID     |
| email         | Email    |
| password_hash | String   |
| created_at    | Datetime |

### ShortUrl

| Field      | Type               |
| ---------- | ------------------ |
| id         | UUID               |
| user_id    | UUID               |
| url        | String             |
| short_code | String             |
| created_at | Datetime           |
| expires_at | Datetime (planned) |

---

## Error Handling

The API includes:

* Validation errors
* Database transaction rollback
* Unique short code protection
* 404 for missing short codes
* 500 for database failures

---

## Future Improvements

* JWT Authentication
* User Accounts
* URL Expiration
* Click Analytics
* Custom Short Codes
* QR Code Generation
* Rate Limiting
* PostgreSQL Support
* Docker Deployment
* Admin Dashboard

---

## License

MIT License

## Author

Aditya Shinde
