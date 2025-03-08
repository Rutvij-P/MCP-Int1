"""
Tests for the SVG class functionality.
"""
import pytest
from svg_animation_mcp import MCP

def test_svg_initialization(mcp, mock_browser):
    """Test that SVG objects are correctly initialized."""
    svg = mcp.create_svg()
    assert svg.mcp == mcp
    assert svg.id == "svg_0"

def test_add_rectangle(mcp, mock_browser):
    """Test adding a rectangle to an SVG."""
    svg = mcp.create_svg()
    # Clear the mock browser to isolate the rectangle creation
    mock_browser.executed_js = []
    
    rectangle = svg.add_rectangle(x=10, y=20, width=100, height=50, fill="blue", stroke="black", stroke_width=2)
    
    # Check the rectangle was created
    assert rectangle is not None
    assert rectangle.id.startswith("rect_")
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "rect" in js_code
    assert "x=\"10\"" in js_code
    assert "y=\"20\"" in js_code
    assert "width=\"100\"" in js_code
    assert "height=\"50\"" in js_code
    assert "fill=\"blue\"" in js_code
    assert "stroke=\"black\"" in js_code
    assert "stroke-width=\"2\"" in js_code

def test_add_circle(mcp, mock_browser):
    """Test adding a circle to an SVG."""
    svg = mcp.create_svg()
    # Clear the mock browser to isolate the circle creation
    mock_browser.executed_js = []
    
    circle = svg.add_circle(cx=150, cy=100, r=30, fill="red")
    
    # Check the circle was created
    assert circle is not None
    assert circle.id.startswith("circle_")
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "circle" in js_code
    assert "cx=\"150\"" in js_code
    assert "cy=\"100\"" in js_code
    assert "r=\"30\"" in js_code
    assert "fill=\"red\"" in js_code

def test_add_path(mcp, mock_browser):
    """Test adding a path to an SVG."""
    svg = mcp.create_svg()
    # Clear the mock browser to isolate the path creation
    mock_browser.executed_js = []
    
    path_data = "M10,10 L50,10 L50,50 L10,50 Z"
    path = svg.add_path(d=path_data, fill="none", stroke="green", stroke_width=3)
    
    # Check the path was created
    assert path is not None
    assert path.id.startswith("path_")
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "path" in js_code
    assert f"d=\"{path_data}\"" in js_code
    assert "fill=\"none\"" in js_code
    assert "stroke=\"green\"" in js_code
    assert "stroke-width=\"3\"" in js_code

def test_add_text(mcp, mock_browser):
    """Test adding text to an SVG."""
    svg = mcp.create_svg()
    # Clear the mock browser to isolate the text creation
    mock_browser.executed_js = []
    
    text = svg.add_text(x=100, y=50, text="Hello SVG", font_family="Arial", font_size=16, fill="black")
    
    # Check the text was created
    assert text is not None
    assert text.id.startswith("text_")
    
    # Check the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "text" in js_code
    assert "x=\"100\"" in js_code
    assert "y=\"50\"" in js_code
    assert "Hello SVG" in js_code
    assert "font-family=\"Arial\"" in js_code
    assert "font-size=\"16\"" in js_code
    assert "fill=\"black\"" in js_code 