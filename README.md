# SVG Animation MCP

A Machine Communication Protocol (MCP) for creating and animating SVG elements with real-time editing and feedback.

## Overview

The SVG Animation MCP provides a clean interface for LLMs (Large Language Models) and users to create, edit, and animate SVG elements in a web browser. It offers real-time visual feedback, interactive editing, and easy export of SVG code.

## Features

- **SVG Creation**: Create and manipulate basic SVG shapes (rectangles, circles, paths, text)
- **Live Editing**: Interactive property editing with immediate visual feedback
- **Animation Support**: Add animations to SVG elements with timeline visualization
- **Prompt Interface**: Generate or modify SVGs using natural language prompts
- **Code Viewing**: See the SVG code with syntax highlighting and export options
- **Modular Architecture**: Extensible design for adding new features and animations

## Requirements

- Python 3.6+
- Flask and Flask-SocketIO
- Modern web browser with JavaScript enabled

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/svg-animation-mcp.git
   cd svg-animation-mcp
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Starting the MCP Server

Run the MCP server by executing:

```python
python svg_animation_mcp.py
```

This will start the server and open a browser window displaying the SVG editor interface.

### Using as an MCP in LLM Workflows

Import the MCP module in your Python code:

```python
from svg_animation_mcp import create_svg, get_mcp_instance

# Create an SVG with a prompt
svg_id = create_svg(width=800, height=600, prompt="Create a simple scene with a house and a tree")

# Get the MCP instance for more advanced operations
mcp = get_mcp_instance()

# Add shapes
rect_id = mcp.add_rectangle(svg_id, 50, 50, 200, 100, {"fill": "#3498db"})
circle_id = mcp.add_circle(svg_id, 300, 100, 50, {"fill": "#e74c3c"})
text_id = mcp.add_text(svg_id, 150, 200, "Hello SVG!")

# Add animations
mcp.animate_element(circle_id, "r", 50, 70, duration=2.0, repeat="indefinite")

# Send additional prompts
mcp.send_prompt("Make the rectangle green")
```

### Browser Interface

The browser interface includes:

- **Canvas Area**: Displays the SVG with interactive elements
- **Shape Tools**: Tools for creating and selecting shapes
- **Properties Panel**: Edit properties of selected elements
- **Prompt Section**: Enter natural language prompts
- **Code Viewer**: See and export the SVG code
- **Timeline**: Visualize and edit animations

## Architecture

The SVG Animation MCP is built with a clean client-server architecture:

- **Server-side**: Flask application with Socket.IO for real-time communication
- **Client-side**: Modern web interface using Vue.js and SVG.js
- **Communication**: WebSocket-based protocol for seamless updates

## Extension and Customization

You can extend the MCP by:

1. Adding new shape types in both frontend and backend
2. Creating new animation types
3. Implementing additional prompt processing capabilities
4. Expanding the UI with new features

## Troubleshooting

If you encounter issues:

- Ensure all dependencies are installed correctly
- Check that no other application is using the same port
- Verify your browser supports the latest JavaScript features
- Check the browser console for error messages

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 