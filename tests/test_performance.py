"""
Performance tests for the MCP to ensure production readiness.
"""
import pytest
import time
from svg_animation_mcp import MCP

def test_svg_creation_performance(mcp, mock_browser):
    """Test the performance of creating SVG elements."""
    start_time = time.time()
    
    # Create an SVG canvas
    svg = mcp.create_svg(width=1000, height=1000)
    
    # Create a large number of elements
    num_elements = 100
    for i in range(num_elements):
        svg.add_circle(cx=i*10, cy=i*10, r=5, fill="red")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Performance threshold: creating 100 elements should take less than 1 second
    # in a mock environment (actual performance will be tested separately)
    assert execution_time < 1.0
    
    # Verify that all elements were created
    circle_ids = [key for key in mcp.element_map if key.startswith("circle_")]
    assert len(circle_ids) == num_elements

def test_animation_performance(mcp, mock_browser):
    """Test the performance of creating and applying animations."""
    svg = mcp.create_svg()
    
    # Create 20 rectangles
    rectangles = []
    for i in range(20):
        rect = svg.add_rectangle(x=i*50, y=100, width=40, height=40, fill=f"rgb({i*10}, 100, 150)")
        rectangles.append(rect)
    
    start_time = time.time()
    
    # Apply multiple animations to each rectangle
    for i, rect in enumerate(rectangles):
        rect.animate("x", from_value=i*50, to_value=i*50 + 100, duration=2, repeat_count="indefinite")
        rect.animate("y", from_value=100, to_value=200, duration=3, repeat_count="indefinite")
        rect.animate("fill", from_value=f"rgb({i*10}, 100, 150)", to_value="blue", duration=4, repeat_count="indefinite")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Performance threshold: applying 60 animations should take less than 1 second
    # in a mock environment
    assert execution_time < 1.0
    
    # Verify that all animations were created
    animation_ids = [key for key in mcp.element_map if key.startswith("anim_")]
    assert len(animation_ids) == 60  # 3 animations per rectangle × 20 rectangles

def test_memory_usage(mcp, mock_browser):
    """Test the memory efficiency of the MCP by creating many elements and animations."""
    svg = mcp.create_svg()
    
    # Create a large number of elements and store their IDs
    element_ids = []
    for i in range(50):
        circle = svg.add_circle(cx=i*10, cy=i*10, r=5, fill="red")
        element_ids.append(circle.id)
        
        # Add an animation to each circle
        anim = circle.animate("r", from_value=5, to_value=10, duration=1, repeat_count="indefinite")
        element_ids.append(anim)
    
    # Check that we haven't created duplicate IDs
    assert len(element_ids) == len(set(element_ids))
    
    # Check that all elements are tracked in the element map
    for element_id in element_ids:
        assert element_id in mcp.element_map

def test_complex_animation_chaining(mcp, mock_browser):
    """Test creating complex chained animations."""
    svg = mcp.create_svg()
    start_time = time.time()
    
    # Create a complex animation scenario
    for i in range(10):
        # Create a shape
        rect = svg.add_rectangle(x=i*100, y=100, width=80, height=80, fill=f"hsl({i*36}, 100%, 50%)")
        
        # Add multiple transforms
        rect.animate_transform("translate", from_value=f"{i*100} 100", to_value=f"{i*100} 300", 
                            duration=2, repeat_count="indefinite")
        rect.animate_transform("rotate", from_value=f"0 {i*100+40} 300", to_value=f"360 {i*100+40} 300", 
                            duration=3, repeat_count="indefinite")
        rect.animate_transform("scale", from_value="1", to_value="1.5", 
                            duration=4, repeat_count="indefinite")
        
        # Add attribute animations
        rect.animate("fill-opacity", from_value="1", to_value="0.5", 
                   duration=5, repeat_count="indefinite")
        rect.animate("stroke-width", from_value="0", to_value="5", 
                   duration=6, repeat_count="indefinite")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Performance threshold: this complex operation should complete in a reasonable time
    assert execution_time < 2.0
    
    # Verify the number of created animations
    animation_ids = [key for key in mcp.element_map if key.startswith("anim_")]
    assert len(animation_ids) == 50  # 5 animations per rectangle × 10 rectangles 