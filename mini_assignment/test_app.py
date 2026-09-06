import pytest

from app import (
    calculate_total,
    contains_substring
)


def test_calculate_total():
    assert calculate_total(2, 3) == 5


def test_contains_substring():
    assert contains_substring("Python in Docker", "Docker") is True


def test_calculate_total_rejects_text():
    with pytest.raises(TypeError, match="first_number must be numeric. Ex: 1 or 1.0"):
        calculate_total("2", 3)


def test_calculate_total_rejects_text_of_second_number():
    with pytest.raises(TypeError, match="second_number must be numeric. Ex: 1 or 1.0"):
        calculate_total(2, "3")


def test_contains_substring_rejects_non_string_message():
    with pytest.raises(TypeError, match="message must be a string"):
        contains_substring(123, "Docker")


def test_contains_substring_rejects_empty_substring():
    with pytest.raises(ValueError, match="both message and substring cannot be empty"):
        contains_substring("Python", "")


def test_contains_substring_rejects_empty_message():
    with pytest.raises(ValueError, match="both message and substring cannot be empty"):
        contains_substring("", "Python")