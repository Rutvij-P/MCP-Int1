#!/usr/bin/env python3
"""
Functional test script for the SVG Animation MCP.

This script tests the actual functionality of the MCP codebase
using a direct approach without complex mocking.
"""

import os
import sys
import traceback
import time

def run_functional_tests():
    """Run functional tests to verify the MCP works as expected."""
    tests_passed = 0
    tests_failed = 0
    
    print("Running functional tests for SVG Animation MCP...")
    
    # Test 1: Create MCP instance and SVG element
    print("\nTest 1: Create MCP instance and SVG element")
    try:
        from svg_animation_mcp import MCP
        
        # Create MCP instance
        mcp = MCP()
        
        # Create SVG element
        svg = mcp.create_svg(width=800, height=600)
        
        # Verify SVG creation
        assert svg is not None, "SVG element was not created"
        assert svg.id.startswith("svg_"), f"Invalid SVG ID: {svg.id}"
        assert svg.id in mcp.element_map, f"SVG element not found in element map: {svg.id}"
        
        print("✅ MCP instance and SVG element created successfully")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Failed to create MCP instance and SVG element: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 2: Create and modify shapes
    print("\nTest 2: Create and modify shapes")
    try:
        from svg_animation_mcp import MCP
        
        mcp = MCP()
        svg = mcp.create_svg()
        
        # Create shapes
        rect = svg.add_rectangle(x=10, y=20, width=100, height=50, fill="blue")
        circle = svg.add_circle(cx=200, cy=100, r=30, fill="red")
        path = svg.add_path(d="M10,10 L50,10 L50,50 L10,50 Z", fill="none", stroke="green")
        text = svg.add_text(x=300, y=50, text="Hello SVG", font_family="Arial", font_size=16)
        
        # Verify shapes were created
        assert rect is not None, "Rectangle was not created"
        assert circle is not None, "Circle was not created"
        assert path is not None, "Path was not created"
        assert text is not None, "Text was not created"
        
        # Verify shapes are in element map
        assert rect.id in mcp.element_map, f"Rectangle not found in element map: {rect.id}"
        assert circle.id in mcp.element_map, f"Circle not found in element map: {circle.id}"
        assert path.id in mcp.element_map, f"Path not found in element map: {path.id}"
        assert text.id in mcp.element_map, f"Text not found in element map: {text.id}"
        
        # Modify shapes
        rect.set_attribute("fill", "purple")
        circle.set_attribute("r", 40)
        text.set_text("Modified Text")
        
        print("✅ Shapes created and modified successfully")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Failed to create and modify shapes: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 3: Test utility functions
    print("\nTest 3: Test utility functions")
    try:
        from utils import (
            validate_color, validate_number, escape_js_string,
            generate_path_data, generate_polygon_points, generate_star_points
        )
        
        # Test color validation
        color = validate_color("red")
        assert color == "red", f"Expected 'red', got '{color}'"
        
        # Test number validation
        num = validate_number(10.5)
        assert num == 10.5, f"Expected 10.5, got {num}"
        
        # Test string escaping
        escaped = escape_js_string('Test "string" with quotes')
        assert 'Test \\"string\\"' in escaped, f"Escaping didn't work as expected: {escaped}"
        
        # Test path generation if available
        if 'generate_path_data' in globals():
            points = [(0, 0), (10, 0), (10, 10), (0, 10)]
            path_data = generate_path_data(points)
            assert "M0,0" in path_data, f"Path data doesn't start correctly: {path_data}"
        
        print("✅ Utility functions work correctly")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Failed to test utility functions: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 4: Advanced modules imports
    print("\nTest 4: Advanced modules imports")
    try:
        # Import advanced modules
        import animation_timing
        import animation_sequence
        import physics_engine
        import shape_morphing
        import ai_suggestions
        import enhanced_ai_suggestions
        
        print("✅ Advanced modules imported successfully")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Failed to import advanced modules: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 5: Performance test
    print("\nTest 5: Performance test (creating 100 elements)")
    try:
        from svg_animation_mcp import MCP
        
        mcp = MCP()
        svg = mcp.create_svg()
        
        start_time = time.time()
        
        # Create 100 circles
        for i in range(100):
            svg.add_circle(cx=i*5, cy=i*3, r=5, fill=f"rgb({i}, 100, 150)")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Created 100 elements in {duration:.4f} seconds")
        assert duration < 10, f"Performance test took too long: {duration:.4f} seconds"
        
        print("✅ Performance test passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Failed performance test: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n✅ All functional tests passed! The MCP codebase appears to be production-ready.")
        print("You can now proceed with integration and deployment steps.")
    else:
        print("\n❌ Some functional tests failed. Please fix the issues before proceeding.")
    
    return tests_failed == 0

if __name__ == "__main__":
    success = run_functional_tests()
    sys.exit(0 if success else 1) 