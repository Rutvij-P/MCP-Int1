"""
Integration tests for the MCP, simulating full workflows.
"""
import pytest
from svg_animation_mcp import MCP

def test_complete_animation_workflow(mcp, mock_browser):
    """Test a complete workflow to create and animate SVG elements."""
    # Create an SVG canvas
    svg = mcp.create_svg(width=800, height=600)
    mock_browser.executed_js = []  # Clear mock to focus on the workflow
    
    # Create multiple shapes
    circle = svg.add_circle(cx=400, cy=300, r=50, fill="red", stroke="black", stroke_width=2)
    rect = svg.add_rectangle(x=100, y=100, width=200, height=100, fill="blue", rx=10, ry=10)
    text = svg.add_text(x=400, y=500, text="SVG Animation", font_family="Arial", font_size=24, fill="green")
    
    # Apply animations to shapes
    circle_anim1 = circle.animate("r", from_value=50, to_value=100, duration=2, repeat_count="indefinite")
    circle_anim2 = circle.animate("fill", from_value="red", to_value="yellow", duration=3, repeat_count="indefinite")
    
    rect_anim = rect.animate_transform("translate", from_value="0 0", to_value="300 200", 
                                     duration=5, repeat_count="indefinite")
    
    text_anim = text.animate("font-size", from_value=24, to_value=48, duration=4, repeat_count="indefinite")
    
    # Modify properties
    circle.set_attribute("fill-opacity", 0.7)
    rect.set_attribute("stroke", "purple")
    text.set_text("SVG Animation MCP")
    
    # Remove an animation
    circle.remove_animation(circle_anim2)
    
    # Verify that the appropriate IDs were generated and stored
    assert svg.id in mcp.element_map
    assert circle.id in mcp.element_map
    assert rect.id in mcp.element_map
    assert text.id in mcp.element_map
    assert circle_anim1 in mcp.element_map
    assert rect_anim in mcp.element_map
    assert text_anim in mcp.element_map
    
    # circle_anim2 should have been removed
    assert circle_anim2 not in mcp.element_map
    
    # JavaScript should have been executed multiple times
    assert len(mock_browser.executed_js) > 0

def test_complex_path_animation(mcp, mock_browser):
    """Test creating and animating complex paths."""
    svg = mcp.create_svg()
    
    # Create a star path
    star_path = "M100,10 L40,180 L190,60 L10,60 L160,180 Z"
    star = svg.add_path(d=star_path, fill="gold", stroke="orange", stroke_width=2)
    
    # Clear mock to focus on animations
    mock_browser.executed_js = []
    
    # Animate path morphing (path data animation)
    circle_path = "M100,100 m-75,0 a75,75 0 1,0 150,0 a75,75 0 1,0 -150,0"
    morph_anim = star.animate("d", from_value=star_path, to_value=circle_path, 
                            duration=3, repeat_count="indefinite")
    
    # Animate other properties
    color_anim = star.animate("fill", from_value="gold", to_value="red", 
                            duration=2, repeat_count="indefinite")
    
    rotate_anim = star.animate_transform("rotate", from_value="0 100 100", 
                                      to_value="360 100 100", duration=5, 
                                      repeat_count="indefinite")
    
    # Verify animations were created
    assert morph_anim in mcp.element_map
    assert color_anim in mcp.element_map
    assert rotate_anim in mcp.element_map
    
    # JavaScript should have been executed for each animation
    assert len(mock_browser.executed_js) == 3

def test_error_handling(mcp, mock_browser):
    """Test that errors are handled properly during a workflow."""
    svg = mcp.create_svg()
    rect = svg.add_rectangle(x=0, y=0, width=100, height=100)
    
    # Make the browser integration fail
    mock_browser.should_fail = True
    
    # Attempting to animate should raise an MCPError
    with pytest.raises(MCPError):
        rect.animate("width", from_value=100, to_value=200, duration=2)
    
    # Reset for other tests
    mock_browser.should_fail = False 