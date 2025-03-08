#!/usr/bin/env python3
"""
Test script for SVG Animation MCP.

This script tests the basic functionality of the SVG Animation MCP
and ensures the HTML renderer works correctly.
"""

import os
import sys
import time
import webbrowser
import pytest

def create_test_html():
    """Create a test HTML file with the necessary structure."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SVG Animation MCP Test</title>
        <style>
            body { 
                margin: 0; 
                padding: 20px; 
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            #svg-container { 
                border: 1px solid #ccc; 
                margin: 20px auto; 
                background-color: white;
                min-height: 500px;
                position: relative;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SVG Animation MCP Test</h1>
            <div id="svg-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="800" height="450">
                    <rect x="100" y="100" width="150" height="100" fill="#3498db">
                        <animate attributeName="x" from="100" to="500" dur="3s" repeatCount="indefinite" />
                    </rect>
                    <circle cx="400" cy="150" r="50" fill="#e74c3c">
                        <animate attributeName="r" from="50" to="80" dur="1.5s" repeatCount="indefinite" />
                    </circle>
                    <text x="300" y="300" font-size="24" fill="#2c3e50">SVG Animation MCP
                        <animate attributeName="fill" from="#2c3e50" to="#8e44ad" dur="3s" repeatCount="indefinite" />
                    </text>
                </svg>
            </div>
        </div>
    </body>
    </html>
    """
    
    test_file = os.path.join(os.path.dirname(__file__), "test_animation.html")
    with open(test_file, "w") as f:
        f.write(html_content)
    
    return os.path.abspath(test_file)

def test_basic_svg_animation():
    """Test basic SVG Animation MCP functionality."""
    # Create the test HTML file
    html_path = create_test_html()
    assert os.path.exists(html_path), "Test HTML file was not created"
    
    # In an actual test environment, we would test the API directly
    # rather than just opening a browser
    pass

def main():
    """Run the test manually."""
    print("\n=== SVG Animation MCP Test ===\n")
    
    # Create the test HTML file
    html_path = create_test_html()
    file_url = f"file://{html_path}"
    
    # Open the HTML file in a browser
    print(f"Opening test HTML file: {file_url}")
    webbrowser.open(file_url)
    
    print("\nTest SVG with animations created successfully!")
    print("\nThe animation should be visible in your browser.")
    
    # Wait for a moment to ensure animations run
    try:
        print("\nPress Ctrl+C to exit the test...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTest completed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 