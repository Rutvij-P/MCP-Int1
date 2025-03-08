"""
Browser Integration Module for SVG Animation MCP.

This module provides utilities for integrating with BrowserTools MCP
to execute JavaScript in the browser.
"""

# Import the BrowserTools MCP if available
try:
    from mcp_browsertools import BrowserMCP
    _has_browser_mcp = True
except ImportError:
    _has_browser_mcp = False

# Create BrowserMCP instance if available
if _has_browser_mcp:
    try:
        browser_mcp = BrowserMCP()
    except Exception as e:
        print(f"Warning: Failed to initialize BrowserMCP: {str(e)}")
        _has_browser_mcp = False


class BrowserIntegrationError(Exception):
    """Custom exception class for browser integration errors."""
    pass


# Fallback implementation for testing
class MockBrowserMCP:
    """
    Mock implementation of BrowserMCP for testing without a browser.
    
    This class logs JavaScript code to the console instead of executing it.
    """
    
    def execute_js(self, code):
        """
        Log the JavaScript code to the console.
        
        Args:
            code: JavaScript code to execute
            
        Returns:
            None
        """
        print("Mock browser executing JavaScript:")
        print(code)
        return None
    
    def load_html(self, html):
        """
        Log the HTML to the console.
        
        Args:
            html: HTML content to load
            
        Returns:
            None
        """
        print("Mock browser loading HTML:")
        print(html)
        return None


def execute_js(code, throw_on_error=True):
    """
    Execute JavaScript code in the browser.
    
    This function uses BrowserTools MCP if available,
    or falls back to a mock implementation.
    
    Args:
        code: JavaScript code to execute
        throw_on_error: Whether to raise an exception on error
        
    Returns:
        Result of the JavaScript execution, or None
        
    Raises:
        BrowserIntegrationError: If JavaScript execution fails and throw_on_error is True
    """
    try:
        if _has_browser_mcp:
            # Use BrowserTools MCP to execute JavaScript
            result = browser_mcp.execute_js(code)
            return result
        else:
            # Use mock implementation
            mock_browser = MockBrowserMCP()
            return mock_browser.execute_js(code)
    except Exception as e:
        if throw_on_error:
            raise BrowserIntegrationError(f"Failed to execute JavaScript: {str(e)}")
        print(f"Warning: JavaScript execution failed: {str(e)}")
        return None


def init_browser_environment():
    """
    Initialize the browser environment for SVG animations.
    
    This function sets up the necessary HTML and CSS for SVG animations.
    
    Returns:
        True if initialization was successful, False otherwise
    """
    try:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
          <title>SVG Animation MCP</title>
          <style>
            body {
              margin: 0;
              padding: 0;
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
              background-color: #f0f0f0;
            }
            #animation-container {
              background-color: white;
              border: 1px solid #ccc;
              box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
          </style>
        </head>
        <body>
          <div id="animation-container"></div>
        </body>
        </html>
        """
        
        # Execute JavaScript to set up the browser environment
        if _has_browser_mcp:
            # Use BrowserTools MCP to load HTML
            browser_mcp.load_html(html)
        else:
            # Log the HTML to the console
            mock_browser = MockBrowserMCP()
            mock_browser.load_html(html)
        
        # Validate that the environment was set up correctly
        validation_code = """
        document.querySelector('#animation-container') !== null
        """
        result = execute_js(validation_code, throw_on_error=False)
        
        if result is not True and _has_browser_mcp:
            print("Warning: Browser environment initialization may have failed. Animation container not found.")
            return False
            
        return True
    except Exception as e:
        print(f"Error initializing browser environment: {str(e)}")
        return False


def clear_svg_animations():
    """
    Clear all SVG animations from the browser.
    
    This function removes all SVG elements from the animation container.
    
    Returns:
        True if clearing was successful, False otherwise
    """
    try:
        js_code = """
        var container = document.getElementById('animation-container');
        if (container) {
            while (container.firstChild) {
                container.removeChild(container.firstChild);
            }
            return true;
        }
        return false;
        """
        result = execute_js(js_code, throw_on_error=False)
        return result is True
    except Exception as e:
        print(f"Error clearing SVG animations: {str(e)}")
        return False


def is_browser_available():
    """
    Check if a browser environment is available.
    
    Returns:
        True if a browser environment is available, False otherwise
    """
    if not _has_browser_mcp:
        return False
        
    try:
        js_code = "true"
        result = execute_js(js_code, throw_on_error=False)
        return result is True
    except Exception:
        return False 