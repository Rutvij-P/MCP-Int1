#!/usr/bin/env python3
"""
Advanced example of how to use the SVG Animation MCP with more complex animations.
"""

from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
import utils
import time
import math

# Import advanced modules
try:
    from animation_timing import AnimationTiming
    from animation_sequence import AnimationSequence
    from physics_engine import initialize_physics_animation
    from shape_morphing import morph_element
    ADVANCED_MODULES_AVAILABLE = True
except ImportError:
    ADVANCED_MODULES_AVAILABLE = False

def create_star_animation(mcp, svg):
    """Create a morphing star animation."""
    # Generate star points
    star_points = utils.generate_star_points(cx=300, cy=200, outer_radius=80, inner_radius=40, points=5)
    
    # Convert points to SVG path data
    star_path_data = utils.generate_path_data(star_points)
    
    # Create star shape
    star = svg.add_path(
        d=star_path_data,
        fill="gold",
        stroke="orange",
        stroke_width=2,
        id="star"
    )
    
    # Create circle for morphing
    circle_path_data = "M300,120 A80,80 0 1,1 299,120 Z"  # Circle path
    
    # Add animation to morph between star and circle
    star.animate(
        "d",
        from_value=star_path_data,
        to_value=circle_path_data,
        duration=2,
        repeat_count="indefinite"
    )
    
    # Also animate the fill color
    star.animate(
        "fill",
        from_value="gold",
        to_value="orange",
        duration=2,
        repeat_count="indefinite"
    )
    
    # Add rotation transform
    star.animate_transform(
        "rotate",
        from_value="0 300 200",
        to_value="360 300 200",
        duration=10,
        repeat_count="indefinite"
    )
    
    return star

def create_pattern_animation(mcp, svg):
    """Create a pattern of animated circles."""
    circles = []
    
    # Create a grid of circles
    for i in range(5):
        for j in range(5):
            # Calculate position
            cx = 100 + i * 100
            cy = 100 + j * 100
            
            # Create circle
            circle = svg.add_circle(
                cx=cx,
                cy=cy,
                r=20,
                fill=f"hsl({(i+j)*36}, 100%, 50%)",
                stroke="white",
                stroke_width=1
            )
            
            # Add pulsing animation with delay based on position
            delay = (i + j) * 0.2
            
            # Using additionalAttributes for delay
            circle.animate(
                "r",
                from_value=20,
                to_value=40,
                duration=2,
                repeat_count="indefinite",
                begin=f"{delay}s"
            )
            
            circles.append(circle)
    
    return circles

def advanced_example():
    """
    Demonstrate advanced MCP features for SVG animation.
    """
    print("Initializing browser environment...")
    init_browser_environment()
    
    print("Creating MCP instance...")
    mcp = MCP()
    
    print("Creating SVG canvas...")
    svg = mcp.create_svg(width=700, height=600, parent_selector="body")
    
    # Add a background rectangle
    bg = svg.add_rectangle(
        x=0, y=0,
        width=700, height=600,
        fill="#f0f0f0"
    )
    
    print("Creating star animation...")
    star = create_star_animation(mcp, svg)
    
    print("Creating pattern animation...")
    circles = create_pattern_animation(mcp, svg)
    
    # Add title text
    title = svg.add_text(
        x=350, y=50,
        text="Advanced SVG Animation Demo",
        font_family="Arial, sans-serif",
        font_size=24,
        text_anchor="middle",
        font_weight="bold",
        fill="#333"
    )
    
    # Add special effects with custom JavaScript
    if ADVANCED_MODULES_AVAILABLE:
        print("Initializing advanced modules...")
        
        # Create a sequence of animations
        sequence = AnimationSequence(svg, mcp)
        
        # Use sequence to create staggered fade-in animation
        sequence.staggered_animation(
            elements=circles,
            attribute="opacity",
            from_value=0.3,
            to_value=1,
            duration=0.5,
            delay=0.1
        )
        
        # Physics simulation would go here if enabled
        # physics = initialize_physics_animation(svg, mcp)
        # physics.start()
    
    print("\nAdvanced animation is now running in the browser!")
    print("Keep this script running to maintain the browser connection.")
    print("Press Ctrl+C to exit.")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting animation script.")

if __name__ == "__main__":
    advanced_example() 