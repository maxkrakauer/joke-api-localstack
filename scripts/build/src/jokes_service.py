import uuid
import random
from typing import List, Dict, Any

from .image_utils import build_image_url


class NoJokesError(Exception):
    pass


class JokeService:
    def __init__(self, table):
        self.table = table

    def add_joke(self, text: str, tags: List[str]) -> Dict[str, Any]:
        if not text or not isinstance(text, str):
            raise ValueError("text is required and must be a string")

        tags = tags or []
        if not isinstance(tags, list):
            raise ValueError("tags must be a list")

        joke_id = str(uuid.uuid4())
        item = {
            "id": joke_id,
            "text": text,
            "tags": tags,
        }
        self.table.put_item(Item=item)
        return item

    def get_random_joke(self) -> Dict[str, Any]:
        # For small datasets, scan + random is fine
        resp = self.table.scan()
        items = resp.get("Items", [])
        if not items:
            raise NoJokesError("No jokes in database")

        joke = random.choice(items)
        tags = joke.get("tags") or []
        joke["imageUrl"] = build_image_url(tags)
        return joke
