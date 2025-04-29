# tests/test_cocktaildb.py

"""
Unit test for cocktaildb module, specifically testing JSON cache loading behavior.
"""

import json
import tempfile
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import cocktaildb

def test_load_cached_json(monkeypatch):
    """
    Test that the get_all_cocktails function correctly loads JSON data from a cache file.
    A temporary file is created and monkeypatched to simulate the cache path.
    """

    # Create a temporary cocktail_cache.json file
    fake_data = [
        {
            "strDrink": "Mocktail", 
            "strInstructions": "None", 
            "strIngredient1": "lime"
        }
    ]

    #use a temporary directory to isolate the test file
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / "cocktail_cache.json"
        json_path.write_text(json.dumps(fake_data), encoding="utf-8")

        # Patch cocktaildb module to use this path
        monkeypatch.setattr(cocktaildb, "Path", lambda _: json_path.parent / "cocktail_cache.json")

        # Clear cache
        cocktaildb.cocktail_cache = []

        # Load and test
        result = cocktaildb.get_all_cocktails()
        assert isinstance(result, list)
        assert result[0]["strDrink"] == "Mocktail"
