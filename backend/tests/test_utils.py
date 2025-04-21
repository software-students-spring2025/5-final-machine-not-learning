# tests/test_utils.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils import match_cocktails_smart

mock_cocktails = [
    {
        "strDrink": "Test Cocktail 1",
        "strInstructions": "Mix and serve",
        "strIngredient1": "vodka",
        "strIngredient2": "lime juice",
        "strIngredient3": "triple sec",
        "strIngredient4": None,
        "strDrinkThumb": "https://example.com/test1.jpg"
    },
    {
        "strDrink": "Test Cocktail 2",
        "strInstructions": "Shake and drink",
        "strIngredient1": "rum",
        "strIngredient2": "coke",
        "strIngredient3": None,
        "strDrinkThumb": "https://example.com/test2.jpg"
    }
]


def test_match_full_match():
    owned = ["vodka", "lime juice", "triple sec"]
    results = match_cocktails_smart(mock_cocktails, owned)
    assert any("Test Cocktail 1" in d["name"] for d in results)

def test_match_partial_match():
    owned = ["vodka", "lime juice"]
    results = match_cocktails_smart(mock_cocktails, owned)
    assert any(d["name"] == "Test Cocktail 1" and "triple sec" in d["missing"] for d in results)

def test_no_match():
    owned = ["beer"]
    results = match_cocktails_smart(mock_cocktails, owned)
    assert len(results) == 0
