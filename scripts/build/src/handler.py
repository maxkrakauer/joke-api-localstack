import json
from http import HTTPStatus

from .db import get_table
from .jokes_service import JokeService, NoJokesError


# Initialize outside handler for connection reuse
_table = get_table()
_service = JokeService(_table)


def _response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """
    Expected as API Gateway proxy integration.
    Supports:
      - GET /jokes  (returns random joke)
      - POST /jokes (adds a joke)
    """
    method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    try:
        if path.endswith("/jokes") or path == "/jokes":
            if method == "GET":
                return handle_get_joke()
            elif method == "POST":
                return handle_post_joke(event)
            else:
                return _response(
                    HTTPStatus.METHOD_NOT_ALLOWED,
                    {"message": f"Method {method} not allowed"},
                )
        else:
            return _response(HTTPStatus.NOT_FOUND, {"message": "Not found"})

    except Exception as e:
        # Simple error handling, you can refine this
        return _response(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {"message": "Internal server error", "error": str(e)},
        )


def handle_get_joke():
    try:
        joke = _service.get_random_joke()
        return _response(HTTPStatus.OK, joke)
    except NoJokesError:
        return _response(HTTPStatus.NOT_FOUND, {"message": "No jokes available"})


def handle_post_joke(event):
    if "body" not in event or event["body"] is None:
        return _response(HTTPStatus.BAD_REQUEST, {"message": "Missing body"})

    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return _response(HTTPStatus.BAD_REQUEST, {"message": "Body must be JSON"})

    text = body.get("text")
    tags = body.get("tags") or []

    try:
        joke = _service.add_joke(text, tags)
        return _response(HTTPStatus.CREATED, joke)
    except ValueError as ve:
        return _response(HTTPStatus.BAD_REQUEST, {"message": str(ve)})
