from typing import List, Optional
import urllib.parse

def build_image_url(tags: Optional[List[str]]) -> str:
    """
    Build a random image URL related to the first tag, if present.
    Falls back to a generic random image.
    """
    base = "https://source.unsplash.com/800x600/"
    if tags:
        # Use first tag as query
        query = "?"+urllib.parse.quote(tags[0])
        return base + query
    # generic random image
    return base + "?random"
