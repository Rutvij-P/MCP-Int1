#!/usr/bin/env python3
"""
Example of how to use the AI Suggestions functionality of the SVG Animation MCP.
"""

from src.mcp.svg_animation_mcp import MCP
from src.mcp.browser_integration import init_browser_environment
import time

# Try to import both AI suggestion modules
try:
    from ai_suggestions import generate_animation_from_text
    from enhanced_ai_suggestions import EnhancedAnimationSuggester
    AI_MODULES_AVAILABLE = True
except ImportError:
    AI_MODULES_AVAILABLE = False

def ai_suggestion_example():
    """
    Demonstrate how to use AI to generate animations from natural language descriptions.
    """
    if not AI_MODULES_AVAILABLE:
        print("Error: AI Suggestion modules not available.")
        print("Make sure ai_suggestions.py and enhanced_ai_suggestions.py are in your path.")
        return
    
    print("Initializing browser environment...")
    init_browser_environment()
    
    print("Creating MCP instance...")
    mcp = MCP()
    
    print("Creating SVG canvas...")
    svg = mcp.create_svg(width=800, height=600)
    
    # Add a background
    svg.add_rectangle(x=0, y=0, width=800, height=600, fill="#f8f9fa")
    
    # Add a title
    svg.add_text(
        x=400, y=50,
        text="AI-Generated SVG Animations",
        font_family="Arial, sans-serif",
        font_size=24,
        font_weight="bold",
        text_anchor="middle",
        fill="#333"
    )
    
    # Add description
    svg.add_text(
        x=400, y=80,
        text="Animations generated from natural language descriptions",
        font_family="Arial, sans-serif",
        font_size=16,
        text_anchor="middle",
        fill="#666"
    )
    
    # Example 1: Basic AI suggestion
    print("\nGenerating animation using basic AI suggester...")
    basic_prompt = "Create a red circle that pulses in the center of the screen"
    
    result = generate_animation_from_text(basic_prompt)
    if result["status"] == "success":
        print(f"✓ Successfully generated animation: {basic_prompt}")
    else:
        print(f"✗ Failed to generate animation: {result['error']}")
    
    # Wait a bit to see the first animation
    time.sleep(2)
    
    # Example 2: Enhanced AI suggestion (more complex)
    print("\nGenerating animation using enhanced AI suggester...")
    enhanced_suggester = EnhancedAnimationSuggester()
    
    enhanced_prompt = "Create a parallax effect with three layers of shapes moving at different speeds"
    success = enhanced_suggester.execute_suggestion(enhanced_prompt)
    
    if success:
        print(f"✓ Successfully generated complex animation: {enhanced_prompt}")
    else:
        print(f"✗ Failed to generate complex animation")
    
    print("\nAI-generated animations are now running in the browser!")
    print("Keep this script running to maintain the browser connection.")
    print("Press Ctrl+C to exit.")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting animation script.")

if __name__ == "__main__":
    ai_suggestion_example() 