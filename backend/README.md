# URL Shortener API Documentation

**Base URL:** `https://urlshortnerapi.fastapicloud.dev`  
**Version:** 1.0.0  
**Built with:** FastAPI + PostgreSQL

---

## Overview

REST API for creating and managing shortened URLs. Supports both anonymous and authenticated usage. Anonymous users can shorten URLs but cannot retrieve their history. Authenticated users get full access to their URL history.

---

## Authentication

Protected endpoints require a Bearer token in the `Authorization` header. Obtain a token from `POST /auth/login`.

```
Authorization: Bearer <access_token>
```

| Property | Value |
|---|---|
| Algorithm | HS256 |
| Token type | Bearer |
| Expiry | 7 days |

---

## Endpoints

### Authentication

---

#### `POST /auth/signup`

Register a new user account.

**Auth required:** No

**Request body**

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | EmailStr | Yes | Valid email address |
| `password` | string | Yes | Minimum 6 characters |

**Example request**

```json
{
  "email": "aditya@example.com",
  "password": "password123"
}
```

**Responses**

| Status | Description |
|---|---|
| `201 Created` | User registered successfully |
| `400 Bad Request` | Email already registered |
| `422 Unprocessable Entity` | Validation error (invalid email or password too short) |

**Example response — 201**

```json
{
  "email": "aditya@example.com",
  "msg": "signup successfull"
}
```

---

#### `POST /auth/login`

Login with credentials and receive a JWT access token.

**Auth required:** No

**Request body**

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | EmailStr | Yes | Registered email address |
| `password` | string | Yes | Account password |

**Example request**

```json
{
  "email": "aditya@example.com",
  "password": "password123"
}
```

**Responses**

| Status | Description |
|---|---|
| `200 OK` | Login successful, returns JWT |
| `401 Unauthorized` | Invalid credentials |
| `422 Unprocessable Entity` | Validation error |

**Example response — 200**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

#### `GET /auth/me`

Get the profile of the currently authenticated user.

**Auth required:** Yes

**Parameters:** None. Identity is derived from the Bearer token.

**Example request**

```
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Responses**

| Status | Description |
|---|---|
| `200 OK` | Returns authenticated user's profile |
| `401 Unauthorized` | Missing or invalid token |

**Example response — 200**

```json
{
  "id": "dc473584-1c93-429f-9a27-6a96380d6515",
  "email": "aditya@example.com",
  "created_at": "2025-06-01T10:23:00.000Z"
}
```

---

### URL Shortener

---

#### `POST /shortner/`

Create a shortened URL. Can be used without authentication, but anonymous URLs are not saved to any account and won't appear in URL history.

**Auth required:** No (optional — provide token to save to account)

**Request body**

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | Full URL to shorten. Must be `http` or `https`. Max 2000 characters. |

**Validation rules**

| Rule | Detail |
|---|---|
| Scheme | Must be `http` or `https`. `ftp://` and others are rejected. |
| Domain | Must include a valid domain containing a dot. |
| Max length | 2000 characters. |

**Example request — authenticated**

```
POST /shortner/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "url": "https://sqlmodel.tiangolo.com/tutorial/insert/"
}
```

**Example request — anonymous**

```
POST /shortner/
Content-Type: application/json

{
  "url": "https://sqlmodel.tiangolo.com/tutorial/insert/"
}
```

**Responses**

| Status | Description |
|---|---|
| `200 OK` | Short URL created successfully |
| `422 Unprocessable Entity` | Invalid URL (bad scheme, missing domain, or exceeds 2000 chars) |

**Example response — 200**

```json
{
  "id": "f3a1bc94-8e21-4d77-a3f2-2b1c7d903ef1",
  "url": "https://sqlmodel.tiangolo.com/tutorial/insert/",
  "short_url": "https://urlshortnerapi.fastapicloud.dev/r/abc123",
  "short_code": "abc123"
}
```

---

#### `GET /shortner/`

Retrieve all shortened URLs belonging to the authenticated user, sorted newest first.

**Auth required:** Yes

**Parameters:** None.

**Example request**

```
GET /shortner/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Responses**

| Status | Description |
|---|---|
| `200 OK` | Returns list of user's URLs |
| `401 Unauthorized` | Missing or invalid token |

**Example response — 200**

```json
{
  "urls": [
    {
      "id": "f3a1bc94-8e21-4d77-a3f2-2b1c7d903ef1",
      "url": "https://sqlmodel.tiangolo.com/tutorial/insert/",
      "short_code": "abc123"
    },
    {
      "id": "a9c22d11-3b44-4e88-b1f7-9c0e5a812fd3",
      "url": "https://fastapi.tiangolo.com",
      "short_code": "xyz789"
    }
  ]
}
```

---

### Redirect

---

#### `GET /r/{short_code}`

Redirect to the original URL associated with the given short code.

**Auth required:** No

**Path parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `short_code` | string | Yes | The short code returned when the URL was created |

**Example request**

```
GET /r/abc123
```

**Responses**

| Status | Description |
|---|---|
| `302 Found` | Redirects to the original URL |
| `404 Not Found` | Short code does not exist |

---

## Error format

All error responses follow this structure:

```json
{
  "detail": "Error message here"
}
```

Validation errors (`422`) return a more detailed structure:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "input": "not-an-email"
    }
  ]
}
```

---

## Quick start

**1. Sign up**

```bash
curl -X POST https://urlshortnerapi.fastapicloud.dev/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "password123"}'
```

**2. Login and save your token**

```bash
TOKEN=$(curl -s -X POST https://urlshortnerapi.fastapicloud.dev/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "password123"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

**3. Shorten a URL**

```bash
curl -X POST https://urlshortnerapi.fastapicloud.dev/shortner/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"url": "https://github.com"}'
```

**4. View your URLs**

```bash
curl https://urlshortnerapi.fastapicloud.dev/shortner/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Interactive docs

FastAPI auto-generates interactive documentation at:

| Interface | URL |
|---|---|
| Swagger UI | `https://urlshortnerapi.fastapicloud.dev/docs` |
| ReDoc | `https://urlshortnerapi.fastapicloud.dev/redoc` |