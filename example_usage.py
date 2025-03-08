#!/usr/bin/env python3
"""
Example of how to use the SVG Animation MCP.
"""

from svg_animation_mcp import MCP
from browser_integration import init_browser_environment

def basic_example():
    """
    Create a simple SVG animation using the MCP.
    """
    print("Initializing browser environment...")
    # Initialize the browser environment first
    init_browser_environment()
    
    print("Creating MCP instance...")
    # Create MCP instance
    mcp = MCP()
    
    print("Creating SVG canvas...")
    # Create an SVG canvas with dimensions 800x600
    svg = mcp.create_svg(width=800, height=600)
    
    print("Adding shapes to the canvas...")
    # Add a rectangle
    rect = svg.add_rectangle(
        x=50, y=50, 
        width=200, height=100, 
        fill="blue", 
        stroke="black", 
        stroke_width=2
    )
    
    # Add a circle
    circle = svg.add_circle(
        cx=400, cy=300, 
        r=80, 
        fill="red"
    )
    
    # Add some text
    text = svg.add_text(
        x=400, y=100, 
        text="SVG Animation MCP", 
        font_family="Arial", 
        font_size=24, 
        text_anchor="middle"
    )
    
    print("Creating animations...")
    # Animate the rectangle - move it from left to right
    rect.animate_transform(
        "translate", 
        from_value=(0, 0), 
        to_value=(500, 0), 
        duration=3, 
        repeat_count="indefinite"
    )
    
    # Animate the circle - make it pulse by changing the radius
    circle.animate(
        "r", 
        from_value=80, 
        to_value=100, 
        duration=2, 
        repeat_count="indefinite"
    )
    
    # Animate the text - change its color
    text.animate(
        "fill", 
        from_value="black", 
        to_value="purple", 
        duration=4, 
        repeat_count="indefinite"
    )
    
    print("Animation is now running in the browser!")
    print("Keep this script running to maintain the browser connection.")
    print("Press Ctrl+C to exit.")
    
    # Keep the script running to maintain animations
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting animation script.")

if __name__ == "__main__":
    basic_example() 