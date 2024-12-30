import pytest
from app import greet

def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"
    assert greet("") == "Hello, !"