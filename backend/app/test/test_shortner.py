"""Tests for the /shortner endpoint."""

from fastapi.testclient import TestClient

BASE_URL = "https://example.com/"
MAX_URL_LENGTH = 2000


class TestShortnerLengthValidation:
    """Tests for URL length validation."""

    def test_accepts_url_under_limit(self, client: TestClient) -> None:
        """URLs shorter than 2000 characters should be accepted."""
        url = BASE_URL + ("a" * 1000)

        response = client.post("/shortner/", json={"url": url})

        assert response.status_code == 200
        assert response.json()["url"] == url

    def test_accepts_url_at_limit(self, client: TestClient) -> None:
        """URLs exactly 2000 characters long should be accepted."""
        url = BASE_URL + ("a" * (MAX_URL_LENGTH - len(BASE_URL)))

        response = client.post("/shortner/", json={"url": url})

        assert response.status_code == 200
        assert response.json()["url"] == url

    def test_rejects_url_exceeding_limit(self, client: TestClient) -> None:
        """URLs longer than 2000 characters should be rejected."""
        url = BASE_URL + ("a" * MAX_URL_LENGTH)

        response = client.post("/shortner/", json={"url": url})

        assert response.status_code == 422
        assert "at most 2000 characters" in response.json()["detail"][0]["msg"]


class TestShortnerUrlValidation:
    """Tests for URL format validation."""

    def test_rejects_non_http_scheme(self, client: TestClient) -> None:
        """Only HTTP and HTTPS URLs should be accepted."""
        response = client.post(
            "/shortner/",
            json={"url": "ftp://example.com"},
        )

        assert response.status_code == 422
        assert "http or https" in response.json()["detail"][0]["msg"]

    def test_rejects_invalid_domain(self, client: TestClient) -> None:
        """URLs without a valid domain should be rejected."""
        response = client.post(
            "/shortner/",
            json={"url": "https://invalid"},
        )

        assert response.status_code == 422
        assert "valid domain" in response.json()["detail"][0]["msg"]


class TestShortnerResponse:
    """Tests for successful response payload."""

    def test_returns_expected_response_schema(
        self,
        client: TestClient,
    ) -> None:
        """A valid request should return the expected response fields."""
        response = client.post(
            "/shortner/",
            json={"url": "https://google.com/abcdkjfkjdkfjf"},
        )

        assert response.status_code == 200

        data = response.json()

        assert "id" in data
        assert "url" in data
        assert "short_code" in data
        assert "short_url" in data

        assert data["url"] == "https://google.com/abcdkjfkjdkfjf"