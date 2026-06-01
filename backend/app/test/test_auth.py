from uuid import uuid4
from fastapi.testclient import TestClient


def unique_email() -> str:
    return f"{uuid4().hex[:3]}@test.com"


class TestAuthentication:
    """Authentication endpoint tests."""

    def test_signup_success(
        self,
        client: TestClient,
    ) -> None:

        email = unique_email()

        response = client.post(
            "/auth/signup",
            json={
                "email": email,
                "password": "password123"
            },
        )

        assert response.status_code in (200, 201)

        data = response.json()

        assert data["email"] == email

    def test_login_success(
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

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "password123"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(
        self,
        client: TestClient,
    ) -> None:

        response = client.post(
            "/auth/login",
            json={
                "email": unique_email(),
                "password": "password123"
            },
        )

        assert response.status_code == 401

    def test_me_requires_authentication(
        self,
        client: TestClient,
    ) -> None:

        response = client.get("/auth/me")

        assert response.status_code == 401

    def test_get_current_user(
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

        response = client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert response.status_code == 200
        assert response.json()["email"] == email

    def test_authenticated_user_can_shorten_url(
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
                "url": "https://google.com"
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