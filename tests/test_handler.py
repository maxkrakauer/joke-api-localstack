import json
from unittest.mock import patch, MagicMock

from src import handler


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
