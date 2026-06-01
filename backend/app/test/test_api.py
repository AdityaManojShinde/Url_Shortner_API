"""Tests for URL shortener endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient


def unique_email() -> str:
    return f"{uuid4().hex[:6]}@test.com"


class TestRootEndpoints:
    """Tests for root endpoints."""

    def test_api_root(
        self,
        client: TestClient,
    ) -> None:

        response = client.get("/")

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == "Api running"
        assert "timestamp" in data

    def test_shortner_root(
        self,
        client: TestClient,
    ) -> None:

        response = client.get("/shortner/")

        assert response.status_code == 200
        assert response.json() == {
            "message": "url shortner api"
        }


class TestCreateShortUrl:
    """Tests for URL creation."""

    def test_create_short_url_anonymous(
        self,
        client: TestClient,
    ) -> None:

        response = client.post(
            "/shortner/",
            json={
                "url": "https://google.com"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "id" in data
        assert "url" in data
        assert "short_code" in data
        assert "short_url" in data

        assert data["url"].rstrip("/") == "https://google.com"

    def test_create_short_url_authenticated(
        self,
        client: TestClient,
    ) -> None:

        email = unique_email()

        client.post(
            "/auth/signup",
            json={
                "email": email,
                "password": "password123"
            },
        )

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "password123"
            },
        )

        token = login_response.json()["access_token"]

        response = client.post(
            "/shortner/",
            json={
                "url": "https://github.com"
            },
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "id" in data
        assert "short_code" in data
        assert "short_url" in data
        assert data["url"].rstrip("/") == "https://github.com"


class TestRedirect:
    """Tests for redirect endpoint."""

    def test_redirect_existing_short_url(
        self,
        client: TestClient,
    ) -> None:

        create_response = client.post(
            "/shortner/",
            json={
                "url": "https://google.com"
            },
        )

        short_code = create_response.json()["short_code"]

        response = client.get(
            f"/r/{short_code}",
            follow_redirects=False,
        )

        assert response.status_code == 307

        assert (
            response.headers["location"]
            == "https://google.com"
        )

    def test_redirect_nonexistent_short_url(
        self,
        client: TestClient,
    ) -> None:

        response = client.get(
            "/r/notfound",
            follow_redirects=False,
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Short URL not found"
        }

    def test_redirect_preserves_target_url(
        self,
        client: TestClient,
    ) -> None:

        target_url = (
            "https://example.com/test/path"
        )

        create_response = client.post(
            "/shortner/",
            json={
                "url": target_url
            },
        )

        short_code = create_response.json()["short_code"]

        response = client.get(
            f"/r/{short_code}",
            follow_redirects=False,
        )

        assert response.status_code == 307
        assert response.headers["location"] == target_url