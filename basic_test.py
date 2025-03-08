#!/usr/bin/env python3
"""
Basic test script for the SVG Animation MCP.

This script performs simple tests to check if the core modules
can be imported and basic functionality works.
"""

import os
import sys
import traceback

def run_basic_tests():
    """Run basic tests to verify the codebase works."""
    tests_passed = 0
    tests_failed = 0
    
    print("Running basic tests for SVG Animation MCP...")
    
    # Test 1: Import core modules
    print("\nTest 1: Import core modules")
    try:
        import svg_animation_mcp
        from svg_animation_mcp import MCP, MCPError
        import utils
        import browser_integration
        
        print("✅ Core modules imported successfully")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 2: Create MCP instance
    print("\nTest 2: Create MCP instance")
    try:
        from svg_animation_mcp import MCP
        mcp = MCP()
        print(f"✅ MCP instance created successfully: {mcp}")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Failed to create MCP instance: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 3: Test utility functions
    print("\nTest 3: Test utility functions")
    try:
        from utils import validate_number
        result = validate_number(10)
        assert result == 10, f"Expected 10, got {result}"
        
        from utils import escape_js_string
        result = escape_js_string('Test "string" with quotes')
        assert 'Test \\"string\\"' in result, f"Escaping didn't work as expected: {result}"
        
        print("✅ Utility functions work correctly")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Failed to test utility functions: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 4: Verify file structure
    print("\nTest 4: Verify file structure")
    required_files = [
        'svg_animation_mcp.py',
        'utils.py',
        'browser_integration.py',
        'ai_suggestions.py',
        'enhanced_ai_suggestions.py',
        'physics_engine.py',
        'shape_morphing.py',
        'animation_timing.py',
        'animation_sequence.py',
        'animation_settings_ui.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not missing_files:
        print("✅ All required files present")
        tests_passed += 1
    else:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        tests_failed += 1
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n✅ All basic tests passed! The codebase appears to be functional.")
        print("You can proceed with creating more detailed unit tests as needed.")
    else:
        print("\n❌ Some basic tests failed. Please fix the issues before proceeding.")
    
    return tests_failed == 0

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1) 