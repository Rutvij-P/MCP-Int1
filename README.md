# SVG Animation MCP

A Machine Communication Protocol (MCP) for creating and animating SVG elements in a web browser.

## Overview

The SVG Animation MCP provides a Python API for creating and animating SVG elements in a web browser. It is designed to be easily used by Large Language Models (LLMs) to generate SVG animations based on natural language descriptions.

The MCP integrates with BrowserTools MCP for JavaScript execution, enabling dynamic SVG manipulation directly from Python code.

## Features

### Core Features
- Create SVG elements with a simple, intuitive API
- Add shapes (rectangles, circles, paths, text) to SVG canvases
- Animate shapes with attributes and transformations
- Execute custom JavaScript for advanced animations
- Utilities for generating paths, polygons, stars, and more
- Seamless integration with BrowserTools MCP
- Robust error handling and validation
- Consistent API across all modules

### Advanced Features
- **AI-Powered Animation Suggestions**: Generate SVG animations from natural language descriptions
- **Enhanced AI Suggestions**: Vercel-level quality animation generation
- **Physics Engine**: Add realistic physics to SVG elements with collision detection, forces, and constraints
- **Shape Morphing**: Create smooth transitions between different SVG shapes
- **Interactive Settings UI**: Fine-tune animation parameters with a user-friendly interface
- **Animation Timing**: Control animation timing with ease-in, ease-out, and other timing functions
- **Animation Sequence**: Create complex animation sequences with precise timing

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/svg-animation-mcp.git
cd svg-animation-mcp

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment

# Initialize browser environment
init_browser_environment()

# Create MCP instance
mcp = MCP()

# Create SVG canvas
svg = mcp.create_svg(width=500, height=500)

# Add a rectangle
rect = svg.add_rectangle(x=10, y=10, width=100, height=100, fill='red')

# Animate the rectangle
rect.animate_transform('translate', from_value=(0, 0), to_value=(400, 0), duration=2)
```

### Error Handling

The MCP now includes robust error handling with custom exceptions:

```python
from svg_animation_mcp import MCP, MCPError
from browser_integration import init_browser_environment, BrowserIntegrationError

try:
    # Initialize browser environment
    if not init_browser_environment():
        raise RuntimeError("Failed to initialize browser environment")
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=500, height=500)
    
    # Add and animate a rectangle
    rect = svg.add_rectangle(x=10, y=10, width=100, height=100, fill='red')
    rect.animate_transform('translate', from_value=(0, 0), to_value=(400, 0), duration=2)
    
except MCPError as e:
    print(f"MCP Error: {e}")
except BrowserIntegrationError as e:
    print(f"Browser Integration Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Advanced Examples

#### AI-Powered Animation Suggestions

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
from ai_suggestions import generate_animation_from_text

# Initialize browser environment
init_browser_environment()

# Generate animation from natural language description
result = generate_animation_from_text("Create a red circle that pulses in the center")
print(result["status"])  # 'success' or 'error'
```

#### Enhanced AI Suggestions

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
from enhanced_ai_suggestions import EnhancedAnimationSuggester

# Initialize browser environment
init_browser_environment()

# Create enhanced suggester
suggester = EnhancedAnimationSuggester()

# Generate and execute a sophisticated animation
success = suggester.execute_suggestion("Create a parallax effect with three layers of shapes moving at different speeds")
```

#### Physics Engine

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
from physics_engine import initialize_physics_animation

# Initialize browser environment
init_browser_environment()

# Create MCP instance
mcp = MCP()

# Create SVG canvas
svg = mcp.create_svg(width=800, height=600)

# Initialize physics simulation
engine = initialize_physics_animation(svg, mcp)

# Apply an explosion force at a specific point
engine.apply_explosion_force((400, 300), 1000, 200)

# Start the physics simulation
engine.start()
```

#### Shape Morphing

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
from shape_morphing import morph_element

# Initialize browser environment
init_browser_environment()

# Create MCP instance
mcp = MCP()

# Create SVG canvas
svg = mcp.create_svg(width=800, height=600)

# Create shapes
circle = svg.add_circle(cx=200, cy=200, r=50, fill="#ff5252", id="circle1")
square = svg.add_rectangle(x=350, y=150, width=100, height=100, fill="#4caf50", id="square1")

# Morph between shapes
morph_element("circle1", "square1", duration=2, mcp=mcp)
```

#### Animation Settings UI

```python
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
from animation_settings_ui import create_settings_ui, show_settings_ui

# Initialize browser environment
init_browser_environment()

# Create MCP instance
mcp = MCP()

# Create SVG canvas
svg = mcp.create_svg(width=800, height=600)

# Create and show the settings UI
ui = create_settings_ui(mcp)
show_settings_ui(ui)
```

### More Examples

See the `demo.py` and `advanced_demo.py` files for more examples of how to use the SVG Animation MCP.

## API Reference

### MCP Class

The `MCP` class is the main entry point for creating SVG animations.

```python
mcp = MCP()
```

#### Methods

- `create_svg(width=500, height=500, parent_selector="body")`: Create an SVG element in the browser
- `execute_js(code)`: Execute arbitrary JavaScript code in the browser

### SVG Class

The `SVG` class represents an SVG element in the browser.

```python
svg = mcp.create_svg(width=500, height=500)
```

#### Methods

- `add_rectangle(x=0, y=0, width=100, height=100, **kwargs)`: Add a rectangle to the SVG
- `add_circle(cx=0, cy=0, r=50, **kwargs)`: Add a circle to the SVG
- `add_path(d, **kwargs)`: Add a path to the SVG
- `add_text(x=0, y=0, text="", **kwargs)`: Add text to the SVG

### Shape Class

The `Shape` class is the base class for all SVG shapes, providing methods for animation and attribute manipulation.

```python
shape = svg.add_rectangle(x=10, y=10, width=100, height=100)
```

#### Methods

- `set_attribute(attribute, value)`: Set an attribute of the shape
- `animate(attribute, from_value, to_value, duration=1, repeat_count="indefinite", **kwargs)`: Animate an attribute of the shape
- `animate_transform(transform_type, from_value, to_value, duration=1, repeat_count="indefinite", **kwargs)`: Animate a transformation of the shape
- `remove_animation(animation_id=None)`: Remove an animation from the shape

### Utilities

The `utils` module provides utility functions for working with SVG animations.

```python
from utils import generate_star_points, generate_path_data, validate_color
```

#### Functions

- `validate_color(color)`: Validate and normalize color values
- `validate_number(value, min_value=None, max_value=None, name="value")`: Validate a numeric value
- `rgb_to_hex(r, g, b)`: Convert RGB color values to hexadecimal color string
- `hex_to_rgb(hex_color)`: Convert hexadecimal color string to RGB values
- `generate_path_data(points)`: Generate SVG path data from a list of points
- `generate_polygon_points(cx, cy, radius, sides)`: Generate points for a regular polygon
- `generate_star_points(cx, cy, outer_radius, inner_radius, points)`: Generate points for a star shape
- `interpolate_color(color1, color2, ratio)`: Interpolate between two colors
- `bezier_curve_points(p0, p1, p2, p3, num_points=20)`: Generate points along a cubic Bezier curve
- `serialize_animation_config(config)`: Serialize animation configuration to JSON string
- `deserialize_animation_config(json_str)`: Deserialize JSON string to animation configuration
- `escape_js_string(s)`: Escape a string for use in JavaScript
- `validate_animation_duration(duration)`: Validate animation duration

### Browser Integration

The `browser_integration` module provides utilities for interacting with the browser.

```python
from browser_integration import init_browser_environment, execute_js, is_browser_available
```

#### Functions

- `execute_js(code, throw_on_error=True)`: Execute JavaScript code in the browser
- `init_browser_environment()`: Initialize the browser environment for SVG animations
- `clear_svg_animations()`: Clear all SVG animations from the browser
- `is_browser_available()`: Check if a browser environment is available

### Advanced Modules

#### AI Suggestions

The `ai_suggestions` module provides utilities for generating SVG animations from natural language descriptions.

```python
from ai_suggestions import generate_animation_from_text, AnimationSuggester
```

#### Enhanced AI Suggestions

The `enhanced_ai_suggestions` module provides advanced natural language processing for generating sophisticated animations.

```python
from enhanced_ai_suggestions import EnhancedAnimationSuggester
```

#### Physics Engine

The `physics_engine` module provides a simple physics engine for adding realistic physical behaviors to SVG elements.

```python
from physics_engine import initialize_physics_animation
```

#### Shape Morphing

The `shape_morphing` module provides utilities for morphing between different SVG shapes.

```python
from shape_morphing import morph_element
```

#### Animation Timing

The `animation_timing` module provides utilities for controlling animation timing.

```python
from animation_timing import AnimationTiming, apply_vercel_entrance
```

#### Animation Sequence

The `animation_sequence` module provides utilities for creating complex animation sequences.

```python
from animation_sequence import AnimationSequence, vercel_staggered_fade_in
```

## Testing

The SVG Animation MCP includes a comprehensive test suite to ensure it meets production standards. The tests are organized into several categories:

### Unit Tests
- Tests for core MCP functionality
- Tests for SVG element creation
- Tests for animation capabilities
- Tests for utility functions
- Tests for browser integration

### Performance Tests
- Tests for SVG creation performance
- Tests for animation application performance
- Tests for memory usage efficiency
- Tests for complex animation chaining

### Browser End-to-End Tests
- Tests for SVG rendering in a real browser
- Tests for animation rendering and execution
- Tests for animation removal

### Simplified Test Scripts

For quick verification of production readiness, two simplified test scripts are provided:

- **basic_test.py**: Tests basic functionality like module imports and file structure
- **functional_test.py**: Tests core functionality including SVG creation, shape manipulation, and performance

To run these simplified tests:

```bash
# Run basic tests
python3 basic_test.py

# Run functional tests
python3 functional_test.py
```

These scripts provide a streamlined way to verify that the codebase is functioning correctly without the complexity of the full test suite.

### Running Tests

We provide a convenient test runner script to execute different test categories:

```bash
# Run unit tests (default)
python run_tests.py

# Run all tests (including browser tests)
python run_tests.py --all

# Run only performance tests
python run_tests.py --performance

# Run only browser tests
python run_tests.py --browser

# Run tests with coverage report
python run_tests.py --coverage

# Run tests with verbose output
python run_tests.py --verbose
```

### CI/CD Integration

The test suite is designed to be easily integrated into CI/CD pipelines. Environment variables control which tests are run:

- `BROWSER_TESTS=true`: Enables browser-based tests
- `FULL_BROWSER_TESTS=true`: Enables comprehensive browser tests

For headless environments, the browser tests automatically use headless mode.

## Error Handling

The MCP provides several custom exception classes for error handling:

- `MCPError`: Base exception class for SVG Animation MCP errors
- `BrowserIntegrationError`: Exception class for browser integration errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Directory Structure

The project is organized as follows:

- `src/mcp/`: Core MCP library files
  - `svg_animation_mcp.py`: Main MCP implementation
  - `browser_integration.py`: Browser communication layer
  - `utils.py`: Utility functions
  - `animation_*.py`: Animation-related modules
  - Other specialized modules

- `examples/`: Example usage and demos
  - `example_usage.py`: Basic usage examples
  - `demo.py`: Simple demonstration
  - `advanced_demo.py`: Advanced features demonstration
  - `advanced_example.py`: More complex examples
  - `ai_example.py`: AI-powered animation examples

- `tests/`: Test suite
  - Unit tests for all components
  - Integration tests
  - Performance tests
  - Browser end-to-end tests

- `docs/`: Documentation
  - `MCP_USAGE_GUIDE.md`: Detailed usage guide 