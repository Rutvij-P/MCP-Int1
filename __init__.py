"""
SVG Animation MCP Package.

This package provides a Machine Communication Protocol (MCP)
for creating and animating SVG elements in a web browser.
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