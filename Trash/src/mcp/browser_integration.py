"""
Browser Integration Module for SVG Animation MCP.

This module provides a simple interface for executing JavaScript in a browser.
It's designed to be monkey-patched by browser_connection.py with a real implementation.
"""

class BrowserIntegrationError(Exception):
    """Exception raised when browser integration fails."""
    pass

def execute_js(code, throw_on_error=True):
    """
    Execute JavaScript code in the browser.
    
    This function is intended to be monkey-patched by browser_connection.py
    with a real implementation that uses an actual browser or HTML renderer.
    
    Args:
        code: JavaScript code to execute
        throw_on_error: Whether to raise an exception on error
        
    Returns:
        Result of the JavaScript execution, or None
        
    Raises:
        BrowserIntegrationError: If JavaScript execution fails and throw_on_error is True
    """
    raise BrowserIntegrationError(
        "No browser integration implementation available. "
        "Make sure to import browser_connection before using this module."
    )

def initialize():
    """
    Initialize browser integration.
    This function is intended to be monkey-patched by browser_connection.py.
    """
    pass

def shutdown():
    """
    Shut down browser integration.
    This function is intended to be monkey-patched by browser_connection.py.
    """
    pass 