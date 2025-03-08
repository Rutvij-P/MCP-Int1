"""
Test script for SVG Animation MCP

This script demonstrates the basic functionality of the SVG Animation MCP
by creating SVG elements and applying animations.
"""

import time
from svg_animation_mcp import create_svg, get_mcp_instance

def main():
    """Test the SVG Animation MCP functionality."""
    print("Starting SVG Animation MCP test...")
    
    # Create an SVG with a test prompt
    svg_id = create_svg(
        width=800, 
        height=600, 
        prompt="Create a colorful scene with shapes", 
        open_browser=True
    )
    print(f"Created SVG with ID: {svg_id}")
    
    # Get the MCP instance
    mcp = get_mcp_instance()
    
    # Add some shapes
    rect1_id = mcp.add_rectangle(
        svg_id, 
        x=50, 
        y=50, 
        width=200, 
        height=100, 
        attributes={"fill": "#3498db", "stroke": "#2980b9", "stroke-width": 2}
    )
    print(f"Added rectangle with ID: {rect1_id}")
    
    rect2_id = mcp.add_rectangle(
        svg_id, 
        x=300, 
        y=50, 
        width=150, 
        height=150, 
        attributes={"fill": "#2ecc71", "stroke": "#27ae60", "stroke-width": 2}
    )
    print(f"Added rectangle with ID: {rect2_id}")
    
    circle_id = mcp.add_circle(
        svg_id, 
        cx=150, 
        cy=250, 
        r=75, 
        attributes={"fill": "#e74c3c", "stroke": "#c0392b", "stroke-width": 2}
    )
    print(f"Added circle with ID: {circle_id}")
    
    text_id = mcp.add_text(
        svg_id, 
        x=300, 
        y=250, 
        text="SVG Animation MCP", 
        attributes={"fill": "#2c3e50", "font-size": 24, "font-family": "Arial, sans-serif"}
    )
    print(f"Added text with ID: {text_id}")
    
    # Add a complex path
    path_data = "M50,400 C100,300 200,300 250,400 S400,500 450,400"
    path_id = mcp.add_path(
        svg_id, 
        d=path_data, 
        attributes={"fill": "none", "stroke": "#8e44ad", "stroke-width": 3}
    )
    print(f"Added path with ID: {path_id}")
    
    # Add animations
    print("Adding animations...")
    
    # Animate circle radius
    anim1_id = mcp.animate_element(
        circle_id, 
        attribute="r", 
        from_value=75, 
        to_value=100, 
        duration=2.0, 
        repeat="indefinite"
    )
    print(f"Added radius animation with ID: {anim1_id}")
    
    # Animate rectangle position
    anim2_id = mcp.animate_element(
        rect1_id, 
        attribute="x", 
        from_value=50, 
        to_value=100, 
        duration=3.0, 
        repeat="indefinite"
    )
    print(f"Added position animation with ID: {anim2_id}")
    
    # Animate text color
    anim3_id = mcp.animate_element(
        text_id, 
        attribute="fill", 
        from_value="#2c3e50", 
        to_value="#8e44ad", 
        duration=4.0, 
        repeat="indefinite"
    )
    print(f"Added color animation with ID: {anim3_id}")
    
    # Send a test prompt
    mcp.send_prompt("Make the green rectangle larger")
    print("Sent test prompt")
    
    print("Test complete. The browser window should be open with the SVG elements and animations.")
    print("Press Ctrl+C to quit...")
    
    # Keep the script running to maintain the server
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Test script terminated by user.")

if __name__ == "__main__":
    main() 