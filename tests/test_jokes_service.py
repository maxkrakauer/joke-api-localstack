import pytest
from src.jokes_service import JokeService, NoJokesError


class FakeTable:
    def __init__(self, items=None):
        self.items = items or []

    def put_item(self, Item):
        self.items.append(Item)

    def scan(self):
        return {"Items": list(self.items)}


def test_add_joke_happy_path():
    table = FakeTable()
    service = JokeService(table)

    joke = service.add_joke("A funny joke", ["tag1", "tag2"])
    assert "id" in joke
    assert joke["text"] == "A funny joke"
    assert joke["tags"] == ["tag1", "tag2"]
    assert len(table.items) == 1


def test_get_random_joke_raises_when_empty():
    table = FakeTable()
    service = JokeService(table)

    with pytest.raises(NoJokesError):
        service.get_random_joke()


def test_get_random_joke_returns_image_url():
    table = FakeTable(items=[{"id": "1", "text": "Joke", "tags": ["cat"]}])
    service = JokeService(table)

    joke = service.get_random_joke()
    assert joke["text"] == "Joke"
    assert "imageUrl" in joke
    assert "cat" in joke["imageUrl"] or "random" in joke["imageUrl"]
