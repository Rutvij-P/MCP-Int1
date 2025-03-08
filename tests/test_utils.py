"""
Tests for the utility functions.
"""
import pytest
from utils import (
    validate_color, validate_number, 
    escape_js_string, validate_animation_duration
)

def test_validate_color():
    """Test color validation."""
    # Valid color formats
    assert validate_color("red") == "red"
    assert validate_color("#FF0000") == "#FF0000"
    assert validate_color("rgb(255, 0, 0)") == "rgb(255, 0, 0)"
    assert validate_color("rgba(255, 0, 0, 0.5)") == "rgba(255, 0, 0, 0.5)"
    
    # Invalid color formats should raise ValueError
    with pytest.raises(ValueError):
        validate_color("not-a-color")
    
    with pytest.raises(ValueError):
        validate_color("#GG0000")  # Invalid hex
    
    with pytest.raises(ValueError):
        validate_color("rgb(300, 0, 0)")  # Out of range

def test_validate_number():
    """Test number validation."""
    # Valid numbers
    assert validate_number(10) == 10
    assert validate_number(10.5) == 10.5
    assert validate_number("10") == 10
    assert validate_number("10.5") == 10.5
    
    # Invalid numbers should raise ValueError
    with pytest.raises(ValueError):
        validate_number("not-a-number")
    
    with pytest.raises(ValueError):
        validate_number(None)

def test_escape_js_string():
    """Test JavaScript string escaping."""
    # Basic string
    assert escape_js_string("hello") == "hello"
    
    # String with quotes
    assert escape_js_string('Say "hello"') == 'Say \\"hello\\"'
    
    # String with single quotes
    assert escape_js_string("Don't do that") == "Don\\'t do that"
    
    # String with newlines and tabs
    assert escape_js_string("hello\nworld\t!") == "hello\\nworld\\t!"
    
    # String with backslashes
    assert escape_js_string("C:\\path\\to\\file") == "C:\\\\path\\\\to\\\\file"

def test_validate_animation_duration():
    """Test animation duration validation."""
    # Valid durations
    assert validate_animation_duration(1) == 1
    assert validate_animation_duration(0.5) == 0.5
    assert validate_animation_duration("1s") == "1s"
    assert validate_animation_duration("500ms") == "500ms"
    
    # Invalid durations should raise ValueError
    with pytest.raises(ValueError):
        validate_animation_duration(-1)
    
    with pytest.raises(ValueError):
        validate_animation_duration("not-a-duration")
    
    with pytest.raises(ValueError):
        validate_animation_duration("1x") 