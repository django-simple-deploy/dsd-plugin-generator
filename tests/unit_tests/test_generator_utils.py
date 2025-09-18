"""Tests for generator utility functions."""

from utils import generator_utils as gu

def test_get_platform_name_lower():
    name = "NewFly"
    assert gu._get_platform_name_lower(name) == "newfly"

    name = "New Fly"
    assert gu._get_platform_name_lower(name) == "newfly"