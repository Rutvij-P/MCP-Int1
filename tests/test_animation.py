"""
Tests for the animation functionality of shapes.
"""
import pytest
from svg_animation_mcp import MCP

def test_attribute_animation(mcp, mock_browser):
    """Test animating an attribute of a shape."""
    svg = mcp.create_svg()
    circle = svg.add_circle(cx=100, cy=100, r=50, fill="blue")
    
    # Clear the mock browser to isolate the animation creation
    mock_browser.executed_js = []
    
    # Animate the circle's radius
    animation = circle.animate("r", from_value=50, to_value=100, duration=2, repeat_count=3)
    
    # Check the animation was created
    assert animation is not None
    assert animation.startswith("anim_")
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "animate" in js_code
    assert "attributeName=\"r\"" in js_code
    assert "from=\"50\"" in js_code
    assert "to=\"100\"" in js_code
    assert "dur=\"2s\"" in js_code
    assert "repeatCount=\"3\"" in js_code

def test_transform_animation(mcp, mock_browser):
    """Test animating a transform of a shape."""
    svg = mcp.create_svg()
    rect = svg.add_rectangle(x=50, y=50, width=100, height=50, fill="red")
    
    # Clear the mock browser to isolate the animation creation
    mock_browser.executed_js = []
    
    # Animate rotation
    animation = rect.animate_transform("rotate", from_value="0 100 75", to_value="360 100 75", 
                                      duration=5, repeat_count="indefinite")
    
    # Check the animation was created
    assert animation is not None
    assert animation.startswith("anim_")
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "animateTransform" in js_code
    assert "attributeName=\"transform\"" in js_code
    assert "type=\"rotate\"" in js_code
    assert "from=\"0 100 75\"" in js_code
    assert "to=\"360 100 75\"" in js_code
    assert "dur=\"5s\"" in js_code
    assert "repeatCount=\"indefinite\"" in js_code

def test_remove_animation(mcp, mock_browser):
    """Test removing an animation from a shape."""
    svg = mcp.create_svg()
    circle = svg.add_circle(cx=100, cy=100, r=50)
    
    # Add an animation
    animation_id = circle.animate("r", from_value=50, to_value=100, duration=2)
    
    # Clear the mock browser to isolate the remove operation
    mock_browser.executed_js = []
    
    # Remove the animation
    circle.remove_animation(animation_id)
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct operation
    assert f"document.getElementById('{animation_id}')" in js_code
    assert "remove()" in js_code

def test_multiple_animations(mcp, mock_browser):
    """Test adding multiple animations to a shape."""
    svg = mcp.create_svg()
    rect = svg.add_rectangle(x=0, y=0, width=100, height=100, fill="green")
    
    # Add multiple animations
    rect.animate("x", from_value=0, to_value=200, duration=3)
    rect.animate("fill", from_value="green", to_value="blue", duration=2)
    rect.animate_transform("scale", from_value="1", to_value="2", duration=4)
    
    # We don't need to check the specific JavaScript here,
    # just confirming that multiple animations can be added without errors
    
    # Check that appropriate entries were added to the element map
    # Get all animation IDs for this rectangle
    animation_ids = [key for key in mcp.element_map if key.startswith("anim_")]
    assert len(animation_ids) == 3 