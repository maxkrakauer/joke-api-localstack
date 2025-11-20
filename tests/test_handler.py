import json
from unittest.mock import patch

from src import handler
from src.jokes_service import NoJokesError


def test_post_joke_success():
    fake_joke = {"id": "123", "text": "hello", "tags": []}

    with patch.object(handler, "_service") as mock_service:
        mock_service.add_joke.return_value = fake_joke

        event = {
            "httpMethod": "POST",
            "path": "/jokes",
            "body": json.dumps({"text": "hello", "tags": []}),
        }

        resp = handler.lambda_handler(event, None)

        assert resp["statusCode"] == 201
        body = json.loads(resp["body"])
        assert body["id"] == "123"
        assert body["text"] == "hello"


def test_get_joke_success():
    fake_joke = {"id": "999", "text": "hi", "tags": []}

    with patch.object(handler, "_service") as mock_service:
        mock_service.get_random_joke.return_value = fake_joke

        event = {
            "httpMethod": "GET",
            "path": "/jokes",
        }

        resp = handler.lambda_handler(event, None)

        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert body["id"] == "999"
        assert body["text"] == "hi"


def test_get_joke_no_jokes():
    """Service raises NoJokesError → handler should return a 404-style response."""
    with patch.object(handler, "_service") as mock_service:
        mock_service.get_random_joke.side_effect = NoJokesError("No jokes available")

        event = {
            "httpMethod": "GET",
            "path": "/jokes",
        }

        resp = handler.lambda_handler(event, None)

        # Adjust this if your handler uses a different status code
        assert resp["statusCode"] == 404
        body = json.loads(resp["body"])
        assert "No jokes" in body.get("message", "")


def test_unknown_path_returns_404():
    """Any path other than /jokes should return 404 (or 400 if you chose that)."""
    event = {
        "httpMethod": "GET",
        "path": "/unknown",
    }

    resp = handler.lambda_handler(event, None)

    # If your handler returns 400 instead, change this accordingly
    assert resp["statusCode"] in (400, 404)


def test_unsupported_method_returns_405():
    """PUT /jokes (or any unsupported method) should return something like 405."""
    event = {
        "httpMethod": "PUT",
        "path": "/jokes",
        "body": json.dumps({"text": "blah", "tags": []}),
    }

    resp = handler.lambda_handler(event, None)

    # If you used 400 or 501 instead, adjust this
    assert resp["statusCode"] in (400, 405, 501)
