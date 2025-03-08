"""
Pytest configuration file for SVG Animation MCP tests.

This file provides fixtures for testing the MCP without requiring
a real browser environment.
"""
import pytest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from svg_animation_mcp import MCP
from browser_integration import execute_js, BrowserIntegrationError

# Mock the browser integration for testing
class MockBrowserIntegration:
    def __init__(self):
        self.executed_js = []
        self.should_fail = False
        self.exception_message = "Browser integration error"
    
    def execute_js(self, code, return_value=None):
        self.executed_js.append(code)
        if self.should_fail:
            raise BrowserIntegrationError(self.exception_message)
        return return_value or "{}"

@pytest.fixture
def mock_browser():
    """Fixture that creates a mock browser integration for testing."""
    mock = MockBrowserIntegration()
    
    # Save the original execute_js function
    original_execute_js = execute_js
    
    # Replace with our mock function
    import browser_integration
    browser_integration.execute_js = mock.execute_js
    
    yield mock
    
    # Restore the original function after the test
    browser_integration.execute_js = original_execute_js

@pytest.fixture
def mcp(mock_browser):
    """Fixture that provides an initialized MCP instance."""
    return MCP() 