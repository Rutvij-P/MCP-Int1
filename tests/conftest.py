"""
Pytest configuration file for SVG Animation MCP tests.

This file provides fixtures for testing the MCP without requiring
a real browser environment.
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the MCP classes
from svg_animation_mcp import MCP
from browser_integration import execute_js, BrowserIntegrationError

# Mock the browser integration for testing
class MockBrowserIntegration:
    def __init__(self):
        self.executed_js = []
        self.should_fail = False
        self.exception_message = "Browser integration error"
    
    def execute_js(self, code, return_value=None):
        print(f"Mock browser executing JavaScript:\n{code}")
        self.executed_js.append(code)
        if self.should_fail:
            raise BrowserIntegrationError(self.exception_message)
        
        # Return a fake animation ID if the code is creating an animation
        if 'animation.setAttribute' in code:
            # Extract the animation ID from the code
            for line in code.split('\n'):
                if "animation.setAttribute('id'" in line:
                    anim_id = line.split("'")[3]
                    return anim_id
        
        return return_value or '{"status":"success"}'

@pytest.fixture
def mock_browser():
    """Fixture that creates a mock browser integration for testing."""
    mock = MockBrowserIntegration()
    
    # Save the original execute_js function
    original_execute_js = execute_js
    
    # Replace with our mock function
    import browser_integration
    browser_integration.execute_js = mock.execute_js
    
    # Also patch the module in src.mcp if it exists
    try:
        import src.mcp.browser_integration
        src.mcp.browser_integration.execute_js = mock.execute_js
    except ImportError:
        pass
    
    yield mock
    
    # Restore the original function after the test
    browser_integration.execute_js = original_execute_js
    try:
        src.mcp.browser_integration.execute_js = original_execute_js
    except (ImportError, NameError):
        pass

@pytest.fixture
def mcp(mock_browser):
    """Fixture that provides an initialized MCP instance."""
    return MCP() 