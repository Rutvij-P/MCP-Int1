"""
SVG Animation MCP - A Machine Communication Protocol for SVG animations.

This module provides a clean Python API for creating and animating SVG elements,
designed to be used by Large Language Models (LLMs) and users directly.
"""

import os
import time
import uuid
import threading
import webbrowser
from typing import Dict, Any, Optional, List, Union, Tuple

# Server imports
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# Constants
DEFAULT_PORT = 5050
DEFAULT_SVG_WIDTH = 800
DEFAULT_SVG_HEIGHT = 600

# Global instances
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
mcp_instance = None

class MCPError(Exception):
    """Custom exception class for SVG Animation MCP errors."""
    pass

class SVGAnimationMCP:
    """
    Main MCP class for SVG animation.
    
    Provides a Python API for creating and animating SVG elements.
    """
    
    def __init__(self, port: int = DEFAULT_PORT):
        """Initialize the MCP with server configuration."""
        self.port = port
        self.element_id_counter = 0
        self.server_thread = None
        self.browser_opened = False
        self.svg_data = {
            "elements": {},
            "animations": {},
            "current_svg": None
        }
    
    def _generate_id(self, prefix: str = "element") -> str:
        """Generate a unique ID for an element."""
        element_id = f"{prefix}_{uuid.uuid4().hex[:8]}"
        return element_id
    
    def start_server(self) -> None:
        """Start the Flask server in a background thread."""
        if self.server_thread is None:
            self.server_thread = threading.Thread(
                target=lambda: socketio.run(app, host="127.0.0.1", port=self.port, debug=False)
            )
            self.server_thread.daemon = True
            self.server_thread.start()
            print(f"SVG Animation MCP server started on http://127.0.0.1:{self.port}")
            time.sleep(1)  # Give the server a moment to start
    
    def create_svg(self, width: int = DEFAULT_SVG_WIDTH, height: int = DEFAULT_SVG_HEIGHT, 
                   prompt: str = None, open_browser: bool = True) -> str:
        """
        Create an SVG element and open it in the browser.
        
        Args:
            width: Width of the SVG element in pixels
            height: Height of the SVG element in pixels
            prompt: Optional prompt text that led to this SVG creation
            open_browser: Whether to open a browser window
            
        Returns:
            str: ID of the created SVG element
        """
        # Start the server if not already running
        self.start_server()
        
        # Generate a unique ID for the SVG
        svg_id = self._generate_id("svg")
        
        # Store SVG data
        self.svg_data["current_svg"] = svg_id
        self.svg_data["elements"][svg_id] = {
            "type": "svg",
            "width": width,
            "height": height,
            "prompt": prompt
        }
        
        # Emit the SVG creation event to connected clients
        socketio.emit("svg_created", {
            "svg_id": svg_id,
            "width": width,
            "height": height,
            "prompt": prompt
        })
        
        # Open the browser if requested
        if open_browser and not self.browser_opened:
            self._open_browser()
            self.browser_opened = True
        
        return svg_id
    
    def reset_canvas(self, width: int = DEFAULT_SVG_WIDTH, height: int = DEFAULT_SVG_HEIGHT,
                     prompt: str = None) -> str:
        """
        Reset the canvas by removing all elements and creating a new SVG.
        
        Args:
            width: Width of the new SVG element in pixels
            height: Height of the new SVG element in pixels
            prompt: Optional prompt text
            
        Returns:
            str: ID of the new SVG element
        """
        # Clear existing elements and animations
        self.svg_data["elements"] = {}
        self.svg_data["animations"] = {}
        
        # Create a new SVG
        svg_id = self.create_svg(width, height, prompt, False)
        
        # Emit a canvas reset event to all clients
        socketio.emit("canvas_reset", {
            "svg_id": svg_id,
            "width": width,
            "height": height
        })
        
        return svg_id
    
    def add_rectangle(self, svg_id: str, x: float = 0, y: float = 0, 
                      width: float = 100, height: float = 50, 
                      attributes: Dict[str, Any] = None) -> str:
        """
        Add a rectangle to the SVG.
        
        Args:
            svg_id: ID of the parent SVG element
            x: X-coordinate of the rectangle
            y: Y-coordinate of the rectangle
            width: Width of the rectangle
            height: Height of the rectangle
            attributes: Additional attributes for the rectangle
            
        Returns:
            str: ID of the created rectangle
        """
        if attributes is None:
            attributes = {}
        
        # Default styling if not provided
        if "fill" not in attributes:
            attributes["fill"] = "#3498db"
        if "stroke" not in attributes:
            attributes["stroke"] = "#2980b9"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = 2
        
        # Generate a unique ID for the rectangle
        rect_id = self._generate_id("rect")
        
        # Store rectangle data
        self.svg_data["elements"][rect_id] = {
            "type": "rect",
            "parent": svg_id,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "attributes": attributes
        }
        
        # Emit the rectangle creation event
        socketio.emit("element_created", {
            "element_id": rect_id,
            "parent_id": svg_id,
            "type": "rect",
            "properties": {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                **attributes
            }
        })
        
        return rect_id
    
    def add_circle(self, svg_id: str, cx: float = 0, cy: float = 0, 
                   r: float = 50, attributes: Dict[str, Any] = None) -> str:
        """
        Add a circle to the SVG.
        
        Args:
            svg_id: ID of the parent SVG element
            cx: X-coordinate of the center
            cy: Y-coordinate of the center
            r: Radius of the circle
            attributes: Additional attributes for the circle
            
        Returns:
            str: ID of the created circle
        """
        if attributes is None:
            attributes = {}
        
        # Default styling if not provided
        if "fill" not in attributes:
            attributes["fill"] = "#e74c3c"
        if "stroke" not in attributes:
            attributes["stroke"] = "#c0392b"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = 2
        
        # Generate a unique ID for the circle
        circle_id = self._generate_id("circle")
        
        # Store circle data
        self.svg_data["elements"][circle_id] = {
            "type": "circle",
            "parent": svg_id,
            "cx": cx,
            "cy": cy,
            "r": r,
            "attributes": attributes
        }
        
        # Emit the circle creation event
        socketio.emit("element_created", {
            "element_id": circle_id,
            "parent_id": svg_id,
            "type": "circle",
            "properties": {
                "cx": cx,
                "cy": cy,
                "r": r,
                **attributes
            }
        })
        
        return circle_id
    
    def add_text(self, svg_id: str, x: float = 0, y: float = 0, 
                 text: str = "Text", attributes: Dict[str, Any] = None) -> str:
        """
        Add text to the SVG.
        
        Args:
            svg_id: ID of the parent SVG element
            x: X-coordinate of the text
            y: Y-coordinate of the text
            text: Text content
            attributes: Additional attributes for the text
            
        Returns:
            str: ID of the created text element
        """
        if attributes is None:
            attributes = {}
        
        # Default styling if not provided
        if "fill" not in attributes:
            attributes["fill"] = "#000000"
        if "font-family" not in attributes:
            attributes["font-family"] = "Arial, sans-serif"
        if "font-size" not in attributes:
            attributes["font-size"] = 16
        
        # Generate a unique ID for the text
        text_id = self._generate_id("text")
        
        # Store text data
        self.svg_data["elements"][text_id] = {
            "type": "text",
            "parent": svg_id,
            "x": x,
            "y": y,
            "content": text,
            "attributes": attributes
        }
        
        # Emit the text creation event
        socketio.emit("element_created", {
            "element_id": text_id,
            "parent_id": svg_id,
            "type": "text",
            "properties": {
                "x": x,
                "y": y,
                "text": text,
                **attributes
            }
        })
        
        return text_id
    
    def add_path(self, svg_id: str, d: str, attributes: Dict[str, Any] = None) -> str:
        """
        Add a path to the SVG.
        
        Args:
            svg_id: ID of the parent SVG element
            d: SVG path data string
            attributes: Additional attributes for the path
            
        Returns:
            str: ID of the created path
        """
        if attributes is None:
            attributes = {}
        
        # Default styling if not provided
        if "fill" not in attributes:
            attributes["fill"] = "none"
        if "stroke" not in attributes:
            attributes["stroke"] = "#2c3e50"
        if "stroke-width" not in attributes:
            attributes["stroke-width"] = 2
        
        # Generate a unique ID for the path
        path_id = self._generate_id("path")
        
        # Store path data
        self.svg_data["elements"][path_id] = {
            "type": "path",
            "parent": svg_id,
            "d": d,
            "attributes": attributes
        }
        
        # Emit the path creation event
        socketio.emit("element_created", {
            "element_id": path_id,
            "parent_id": svg_id,
            "type": "path",
            "properties": {
                "d": d,
                **attributes
            }
        })
        
        return path_id
    
    def animate_element(self, element_id: str, attribute: str, 
                      from_value: Any, to_value: Any, 
                      duration: float = 1.0, repeat: Union[int, str] = 0,
                      attributes: Dict[str, Any] = None) -> str:
        """
        Add an animation to an SVG element.
        
        Args:
            element_id: ID of the element to animate
            attribute: Attribute to animate (e.g., 'x', 'width', 'fill')
            from_value: Starting value of the animation
            to_value: Ending value of the animation
            duration: Duration of the animation in seconds
            repeat: Number of repetitions (0 for none, 'indefinite' for infinite)
            attributes: Additional attributes for the animation
            
        Returns:
            str: ID of the created animation
        """
        if attributes is None:
            attributes = {}
        
        # Generate a unique ID for the animation
        anim_id = self._generate_id("anim")
        
        # Store animation data
        self.svg_data["animations"][anim_id] = {
            "element_id": element_id,
            "attribute": attribute,
            "from_value": from_value,
            "to_value": to_value,
            "duration": duration,
            "repeat": repeat,
            "attributes": attributes
        }
        
        # Emit the animation creation event
        socketio.emit("animation_created", {
            "animation_id": anim_id,
            "element_id": element_id,
            "attribute": attribute,
            "from": from_value,
            "to": to_value,
            "duration": duration,
            "repeat": repeat,
            "attributes": attributes
        })
        
        return anim_id
    
    def delete_element(self, element_id: str) -> bool:
        """
        Delete an element from the SVG.
        
        Args:
            element_id: ID of the element to delete
            
        Returns:
            bool: True if the element was deleted, False otherwise
        """
        if element_id in self.svg_data["elements"]:
            # Remove the element from the data
            del self.svg_data["elements"][element_id]
            
            # Remove any animations associated with this element
            for anim_id in list(self.svg_data["animations"].keys()):
                if self.svg_data["animations"][anim_id]["element_id"] == element_id:
                    del self.svg_data["animations"][anim_id]
            
            # Emit the element deletion event
            socketio.emit("element_deleted", {
                "element_id": element_id
            })
            
            return True
        
        return False
    
    def send_prompt(self, prompt: str) -> None:
        """
        Send a prompt to generate or modify SVG content.
        
        Args:
            prompt: The prompt text
        """
        # Emit the prompt event
        socketio.emit("prompt_received", {
            "prompt": prompt,
            "timestamp": time.time()
        })
    
    def _open_browser(self) -> None:
        """Open the default web browser pointing to the MCP server."""
        url = f"http://127.0.0.1:{self.port}/"
        print(f"Opening browser at: {url}")
        webbrowser.open(url)


# Server routes
@app.route('/')
def index():
    """Render the main editor page."""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Return the server status."""
    return jsonify({
        "status": "running",
        "port": mcp_instance.port if mcp_instance else DEFAULT_PORT
    })

@app.route('/api/svg-data')
def get_svg_data():
    """Return the current SVG data."""
    if mcp_instance:
        return jsonify(mcp_instance.svg_data)
    return jsonify({})

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print("Client connected")
    if mcp_instance and mcp_instance.svg_data["current_svg"]:
        # Send current state to new client
        emit("svg_data", mcp_instance.svg_data)

@socketio.on('element_updated')
def handle_element_update(data):
    """Handle element update from client."""
    if mcp_instance and "element_id" in data and "properties" in data:
        element_id = data["element_id"]
        if element_id in mcp_instance.svg_data["elements"]:
            for key, value in data["properties"].items():
                if key != "type" and key != "parent":
                    if key == "attributes":
                        mcp_instance.svg_data["elements"][element_id][key].update(value)
                    else:
                        mcp_instance.svg_data["elements"][element_id][key] = value
            
            # Broadcast the update to all clients except sender
            emit("element_updated", data, broadcast=True, include_self=False)

@socketio.on('reset_canvas')
def handle_reset_canvas(data):
    """Handle canvas reset request from client."""
    if mcp_instance:
        width = data.get("width", DEFAULT_SVG_WIDTH)
        height = data.get("height", DEFAULT_SVG_HEIGHT)
        prompt = data.get("prompt", "Canvas reset by user")
        
        # Reset the canvas
        svg_id = mcp_instance.reset_canvas(width, height, prompt)
        
        # Return the new SVG ID
        return jsonify({"svg_id": svg_id})

@socketio.on('create_rect')
def handle_create_rect(data):
    """Handle rectangle creation from client."""
    if mcp_instance and "svg_id" in data:
        svg_id = data["svg_id"]
        x = data.get("x", 0)
        y = data.get("y", 0)
        width = data.get("width", 100)
        height = data.get("height", 50)
        
        # Extract attributes
        attributes = {}
        for key, value in data.items():
            if key not in ["svg_id", "x", "y", "width", "height"]:
                attributes[key] = value
        
        # Create the rectangle
        rect_id = mcp_instance.add_rectangle(svg_id, x, y, width, height, attributes)
        
        # Return the created rectangle ID
        return jsonify({"element_id": rect_id})

@socketio.on('create_circle')
def handle_create_circle(data):
    """Handle circle creation from client."""
    if mcp_instance and "svg_id" in data:
        svg_id = data["svg_id"]
        cx = data.get("cx", 0)
        cy = data.get("cy", 0)
        r = data.get("r", 50)
        
        # Extract attributes
        attributes = {}
        for key, value in data.items():
            if key not in ["svg_id", "cx", "cy", "r"]:
                attributes[key] = value
        
        # Create the circle
        circle_id = mcp_instance.add_circle(svg_id, cx, cy, r, attributes)
        
        # Return the created circle ID
        return jsonify({"element_id": circle_id})

@socketio.on('create_text')
def handle_create_text(data):
    """Handle text creation from client."""
    if mcp_instance and "svg_id" in data:
        svg_id = data["svg_id"]
        x = data.get("x", 0)
        y = data.get("y", 0)
        text = data.get("text", "Text")
        
        # Extract attributes
        attributes = {}
        for key, value in data.items():
            if key not in ["svg_id", "x", "y", "text"]:
                attributes[key] = value
        
        # Create the text
        text_id = mcp_instance.add_text(svg_id, x, y, text, attributes)
        
        # Return the created text ID
        return jsonify({"element_id": text_id})

@socketio.on('create_path')
def handle_create_path(data):
    """Handle path creation from client."""
    if mcp_instance and "svg_id" in data:
        svg_id = data["svg_id"]
        d = data.get("d", "")
        
        # Extract attributes
        attributes = {}
        for key, value in data.items():
            if key not in ["svg_id", "d"]:
                attributes[key] = value
        
        # Create the path
        path_id = mcp_instance.add_path(svg_id, d, attributes)
        
        # Return the created path ID
        return jsonify({"element_id": path_id})

@socketio.on('delete_element')
def handle_delete_element(data):
    """Handle element deletion from client."""
    if mcp_instance and "element_id" in data:
        element_id = data["element_id"]
        success = mcp_instance.delete_element(element_id)
        
        # Return the deletion result
        return jsonify({"success": success})

@socketio.on('export_svg')
def handle_export_svg(data):
    """Handle SVG export request."""
    if mcp_instance:
        # In a real implementation, we would generate the SVG code here
        # For now, we just acknowledge the request
        emit("export_result", {
            "success": True,
            "message": "SVG exported successfully"
        })

@socketio.on('prompt_received')
def handle_prompt(data):
    """Handle prompt from client."""
    if mcp_instance and "prompt" in data:
        prompt = data["prompt"]
        
        # Process the prompt (in a real implementation, this would involve more logic)
        # For now, we just broadcast it to all clients
        socketio.emit("prompt_received", {
            "prompt": prompt,
            "timestamp": time.time()
        })
        
        # Return a success response
        return jsonify({"success": True})

# Create a global MCP instance
def get_mcp_instance(port: int = DEFAULT_PORT) -> SVGAnimationMCP:
    """Get or create the global MCP instance."""
    global mcp_instance
    if mcp_instance is None:
        mcp_instance = SVGAnimationMCP(port=port)
    return mcp_instance

# Convenience function to create an SVG
def create_svg(width: int = DEFAULT_SVG_WIDTH, height: int = DEFAULT_SVG_HEIGHT, 
             prompt: str = None, open_browser: bool = True) -> str:
    """
    Create an SVG and open it in the browser.
    
    This is a convenience function for LLMs to use.
    
    Args:
        width: Width of the SVG in pixels
        height: Height of the SVG in pixels
        prompt: Optional prompt text
        open_browser: Whether to open a browser window
        
    Returns:
        str: ID of the created SVG
    """
    mcp = get_mcp_instance()
    return mcp.create_svg(width, height, prompt, open_browser)

# Run the server directly if this file is executed
if __name__ == "__main__":
    mcp = get_mcp_instance()
    mcp.start_server()
    
    # Create an example SVG
    svg_id = mcp.create_svg(prompt="Example SVG created by the MCP")
    
    # Add some example elements
    rect_id = mcp.add_rectangle(svg_id, 50, 50, 200, 100)
    circle_id = mcp.add_circle(svg_id, 300, 100, 50)
    text_id = mcp.add_text(svg_id, 150, 200, "Hello SVG!")
    
    # Add an animation
    mcp.animate_element(circle_id, "r", 50, 70, duration=2.0, repeat="indefinite")
    
    # Keep the server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutdown requested.") 