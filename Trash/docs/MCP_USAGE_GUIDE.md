# SVG Animation MCP Usage Guide

This guide will help you run and interact with the SVG Animation MCP (Motion Control Platform) that you've created.

## Prerequisites

Before running the MCP, make sure you have the following installed:

- Python 3.6 or later
- Required Python packages (install using `pip install -r requirements.txt`)
- A modern web browser (Chrome is recommended)

## Basic Usage

### 1. Running the Basic Example

The simplest way to start using the MCP is to run the basic example:

```bash
python3 example_usage.py
```

This script demonstrates:
- Initializing the browser environment
- Creating an SVG canvas
- Adding basic shapes (rectangle, circle, text)
- Creating simple animations

The animation will run in your browser, and the script will keep running to maintain the connection. Press Ctrl+C to exit.

### 2. Advanced Animations

For more complex animations, run the advanced example:

```bash
python3 advanced_example.py
```

This demonstrates:
- Shape morphing (star to circle)
- Creating patterns of animated elements
- Using transformations and compound animations
- Advanced modules (if available)

### 3. AI-Generated Animations

To experience the AI-powered animation generation, run:

```bash
python3 ai_example.py
```

This example shows how to:
- Generate animations from natural language descriptions
- Use both basic and enhanced AI suggestion engines

## Creating Your Own Animations

To create your own animations, follow these steps:

### 1. Initialize the Environment

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment

# Initialize browser environment
init_browser_environment()

# Create MCP instance
mcp = MCP()
```

### 2. Create an SVG Canvas

```python
# Create a canvas with dimensions 800x600
svg = mcp.create_svg(width=800, height=600)
```

### 3. Add Shapes

```python
# Create a rectangle
rect = svg.add_rectangle(
    x=100, y=100,
    width=200, height=100,
    fill="blue"
)

# Create a circle
circle = svg.add_circle(
    cx=400, cy=200,
    r=50,
    fill="red"
)

# Create text
text = svg.add_text(
    x=400, y=50,
    text="My Animation",
    font_family="Arial",
    font_size=24,
    text_anchor="middle"
)
```

### 4. Animate Your Shapes

```python
# Animate an attribute (like radius for circles)
circle.animate(
    "r",  # attribute to animate
    from_value=50,
    to_value=80,
    duration=2,  # in seconds
    repeat_count="indefinite"  # or a number
)

# Animate a transformation (like movement)
rect.animate_transform(
    "translate",  # transform type
    from_value=(0, 0),
    to_value=(300, 0),
    duration=3,
    repeat_count="indefinite"
)

# Animate color
text.animate(
    "fill",
    from_value="black",
    to_value="purple",
    duration=4,
    repeat_count="indefinite"
)
```

### 5. Keep the Animation Running

```python
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Animation stopped")
```

## Using Advanced Features

### Shape Morphing

```python
from shape_morphing import morph_element

# Create two shapes with IDs
circle = svg.add_circle(cx=200, cy=200, r=50, fill="#ff5252", id="circle1")
square = svg.add_rectangle(x=350, y=150, width=100, height=100, fill="#4caf50", id="square1")

# Morph between them
morph_element("circle1", "square1", duration=2, mcp=mcp)
```

### Physics Engine

```python
from physics_engine import initialize_physics_animation

# Initialize physics simulation
engine = initialize_physics_animation(svg, mcp)

# Add shapes to the physics simulation
# ...

# Apply forces
engine.apply_explosion_force((400, 300), 1000, 200)

# Start the simulation
engine.start()
```

### Animation Sequences

```python
from animation_sequence import AnimationSequence

# Create a sequence
sequence = AnimationSequence(svg, mcp)

# Create staggered animations
elements = [circle1, circle2, circle3, circle4, circle5]
sequence.staggered_animation(
    elements=elements,
    attribute="opacity",
    from_value=0,
    to_value=1,
    duration=0.5,
    delay=0.1
)
```

## Troubleshooting

If you encounter issues:

1. **Browser doesn't open or connect**:
   - Make sure you've installed all dependencies from requirements.txt
   - Try running the script with administrator/sudo privileges
   - Check if your firewall is blocking the connection

2. **Animations don't appear**:
   - Check the browser console for JavaScript errors
   - Verify that elements have valid IDs and attributes
   - Ensure the browser tab remains open and active

3. **Script crashes or errors**:
   - Check error messages for clues about missing dependencies
   - Verify that all imported modules are available in your Python path
   - Make sure you're using a compatible Python version (3.6+)

## Running Tests

To ensure your MCP is working correctly:

```bash
# Run basic tests
python3 basic_test.py

# Run more comprehensive functional tests
python3 functional_test.py
```

For detailed testing options, refer to the README.md file.

## Support

If you encounter issues or have questions, please check:
- The README.md file for additional information
- The example scripts for usage patterns
- The test files for expected behavior 