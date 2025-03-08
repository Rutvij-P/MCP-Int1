"""
Example of using the SVG Animation MCP library.

This script demonstrates how to create and animate SVG elements using the MCP library.
"""

from svg_animation_mcp import MCP
import time

def main():
    # Initialize the MCP
    mcp = MCP()
    
    # Create an SVG canvas - target the specific container instead of body
    svg = mcp.create_svg(width=600, height=400, parent_selector="#svg-container")
    print("SVG canvas created with ID:", svg.id)
    
    # Add a background rectangle
    background = svg.add_rectangle(
        x=0, y=0, 
        width=600, height=400, 
        fill="#f0f0f0", 
        stroke="#333333", 
        stroke_width=2
    )
    
    # Add a circle that will move horizontally
    circle = svg.add_circle(
        cx=100, cy=200, 
        r=40, 
        fill="#ff6600", 
        stroke="#333333", 
        stroke_width=2
    )
    
    # Add a rectangle that will change color
    rect = svg.add_rectangle(
        x=250, y=150, 
        width=100, height=100, 
        fill="#3366cc", 
        stroke="#333333", 
        stroke_width=2
    )
    
    # Add some text
    text = svg.add_text(
        x=300, y=50, 
        text="SVG Animation Demo", 
        font_family="Arial", 
        font_size=24, 
        text_anchor="middle", 
        fill="#333333"
    )
    
    # Add a path (a simple triangle)
    path = svg.add_path(
        d="M 450,300 L 500,200 L 550,300 Z", 
        fill="#33cc33", 
        stroke="#333333", 
        stroke_width=2
    )
    
    # Now let's add some animations
    
    # 1. Move the circle horizontally
    circle_anim = circle.animate_transform(
        transform_type="translate", 
        from_value="0 0", 
        to_value="400 0", 
        duration=3, 
        repeat_count="indefinite"
    )
    
    # 2. Change rectangle color
    rect_anim = rect.animate(
        attribute="fill", 
        from_value="#3366cc", 
        to_value="#cc3366", 
        duration=2, 
        repeat_count="indefinite"
    )
    
    # 3. Rotate the triangle
    path_anim = path.animate_transform(
        transform_type="rotate", 
        from_value="0 500 250", 
        to_value="360 500 250", 
        duration=4, 
        repeat_count="indefinite"
    )
    
    # 4. Scale the text
    text_anim = text.animate_transform(
        transform_type="scale", 
        from_value="1", 
        to_value="1.2", 
        duration=1.5, 
        repeat_count="indefinite"
    )
    
    print("Animations created with IDs:", circle_anim, rect_anim, path_anim, text_anim)
    
    # Let the animations run for 10 seconds
    print("Animations running for 10 seconds...")
    time.sleep(10)
    
    # Remove one animation (the circle's)
    print("Removing circle animation...")
    circle.remove_animation(circle_anim)
    
    # Change an attribute directly
    print("Changing rectangle attributes...")
    rect.set_attribute("stroke-width", 5)
    rect.set_attribute("stroke", "#ff0000")
    
    # Update text
    print("Updating text...")
    text.set_text("Animation Modified!")
    
    print("Example complete! The remaining animations will continue to run indefinitely.")

if __name__ == "__main__":
    main() 