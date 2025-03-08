"""
Tests for the core MCP functionality.
"""
import pytest
from svg_animation_mcp import MCP, MCPError

def test_mcp_initialization(mcp):
    """Test that MCP initializes correctly."""
    assert mcp.element_id_counter == 0
    assert mcp.element_map == {}

def test_generate_id(mcp):
    """Test that _generate_id creates unique IDs."""
    id1 = mcp._generate_id()
    id2 = mcp._generate_id()
    id3 = mcp._generate_id("custom")
    
    assert id1 == "element_0"
    assert id2 == "element_1"
    assert id3 == "custom_2"
    assert mcp.element_id_counter == 3

def test_create_svg(mcp, mock_browser):
    """Test creating an SVG element."""
    svg = mcp.create_svg(width=800, height=600, parent_selector="#container")
    
    # Check that the SVG was created
    assert svg is not None
    assert svg.id == "svg_0"
    
    # Check that the JavaScript was executed
    assert len(mock_browser.executed_js) == 1
    js_code = mock_browser.executed_js[0]
    
    # Verify the JavaScript contains the correct attributes
    assert "width=\"800\"" in js_code
    assert "height=\"600\"" in js_code
    assert "#container" in js_code
    assert "svg_0" in js_code

def test_create_svg_failure(mcp, mock_browser):
    """Test handling of errors when creating SVG elements."""
    # Make the browser integration fail
    mock_browser.should_fail = True
    
    # Attempting to create an SVG should raise an MCPError
    with pytest.raises(MCPError):
        mcp.create_svg()

    # Reset for other tests
    mock_browser.should_fail = False

def test_js_execution_wrapper(mcp, mock_browser):
    """Test the execute_js wrapper method."""
    # Execute some JavaScript
    mcp.execute_js("console.log('test');")
    
    # Check that it was passed to the browser integration
    assert len(mock_browser.executed_js) == 1
    assert mock_browser.executed_js[0] == "console.log('test');"
    
    # Test error handling
    mock_browser.should_fail = True
    with pytest.raises(MCPError):
        mcp.execute_js("console.log('should fail');")
    mock_browser.should_fail = False 