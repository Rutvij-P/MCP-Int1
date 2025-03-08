"""
MCP (Machine Communication Protocol) for SVG animations.

This package provides a Python interface for creating and manipulating SVG animations
through a browser-based communication protocol.
"""

from svg_animation_mcp import MCP, SVG, Shape, Rectangle, Circle, Path, Text
from browser_integration import execute_js, init_browser_environment, clear_svg_animations
import utils

__version__ = "0.1.0"
__all__ = [
    'MCP', 'SVG', 'Shape', 'Rectangle', 'Circle', 'Path', 'Text',
    'execute_js', 'init_browser_environment', 'clear_svg_animations',
    'utils'
] 