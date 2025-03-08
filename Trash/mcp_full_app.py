"""
Complete Flask Application for SVG Animation MCP.

This script demonstrates how to use the SVG Animation MCP library in a real web application.
It uses a real browser connection for all SVG manipulations.
"""

from flask import Flask, render_template, request, jsonify, url_for
import browser_connection  # Import our browser connection module first to monkey-patch
from svg_animation_mcp import MCP
import os
import json
import atexit
import signal
import sys
import time
import threading
import webbrowser

# Use a different port to avoid conflicts with AirPlay or other services
PORT = 5001

app = Flask(__name__)

# Register shutdown function to close the browser when the app exits
atexit.register(browser_connection.shutdown)

# Also handle SIGINT and SIGTERM to ensure browser is closed on Ctrl+C
def signal_handler(sig, frame):
    print("\nShutting down application...")
    browser_connection.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)

# Create a simple HTML template file
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>SVG Animation MCP Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
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
        
        h1, h2 {
            color: #333;
        }
        
        #svg-container {
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            height: 500px;
            position: relative;
        }
        
        .control-panel {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        
        button:hover {
            background-color: #45a049;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .status-indicator {
            padding: 10px;
            margin-top: 20px;
            background-color: #f9f9f9;
            border-radius: 4px;
            border-left: 4px solid #4CAF50;
        }
        
        .color-picker {
            margin-top: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .color-option {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid #ddd;
        }
        
        .color-option:hover {
            border-color: #333;
        }
        
        .color-option.selected {
            border-color: #000;
            box-shadow: 0 0 5px rgba(0,0,0,0.5);
        }
        
        .log-container {
            margin-top: 20px;
            height: 150px;
            overflow-y: auto;
            background-color: #333;
            color: #fff;
            padding: 10px;
            font-family: monospace;
            font-size: 12px;
            border-radius: 4px;
        }
        
        .log-entry {
            margin: 2px 0;
        }
        
        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
        }
        
        .tab {
            padding: 10px 15px;
            background-color: #ddd;
            border-radius: 4px 4px 0 0;
            cursor: pointer;
            border: 1px solid #ccc;
            border-bottom: none;
        }
        
        .tab.active {
            background-color: white;
            font-weight: bold;
        }
        
        .tab-content {
            display: none;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 0 4px 4px 4px;
        }
        
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SVG Animation MCP Demo</h1>
        
        <div class="tabs">
            <div class="tab active" data-tab="shapes">Shapes</div>
            <div class="tab" data-tab="animations">Animations</div>
            <div class="tab" data-tab="advanced">Advanced</div>
        </div>
        
        <div class="tab-content active" id="shapes-tab">
            <div class="control-panel">
                <button onclick="createShape('circle')">Add Circle</button>
                <button onclick="createShape('rectangle')">Add Rectangle</button>
                <button onclick="createShape('text')">Add Text</button>
                <button onclick="createShape('path')">Add Path</button>
                <button onclick="resetAnimations()" style="background-color: #f44336;">Reset All</button>
            </div>
            
            <div class="color-picker">
                <div class="form-group" style="width: 100%;">
                    <label>Shape Color:</label>
                </div>
                <div class="color-option selected" style="background-color: #3498db;" data-color="#3498db"></div>
                <div class="color-option" style="background-color: #e74c3c;" data-color="#e74c3c"></div>
                <div class="color-option" style="background-color: #2ecc71;" data-color="#2ecc71"></div>
                <div class="color-option" style="background-color: #f39c12;" data-color="#f39c12"></div>
                <div class="color-option" style="background-color: #9b59b6;" data-color="#9b59b6"></div>
                <div class="color-option" style="background-color: #1abc9c;" data-color="#1abc9c"></div>
                <div class="color-option" style="background-color: #34495e;" data-color="#34495e"></div>
            </div>
        </div>
        
        <div class="tab-content" id="animations-tab">
            <h2>Animation Controls</h2>
            <div class="form-group">
                <label for="animation-type">Animation Type:</label>
                <select id="animation-type">
                    <option value="translate">Move (Translate)</option>
                    <option value="rotate">Rotate</option>
                    <option value="scale">Scale</option>
                    <option value="color">Color Change</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="animation-duration">Duration (seconds):</label>
                <input type="number" id="animation-duration" value="2" min="0.1" step="0.1">
            </div>
            
            <div class="form-group">
                <label for="repeat-count">Repeat Count:</label>
                <select id="repeat-count">
                    <option value="indefinite">Indefinite</option>
                    <option value="1">1 time</option>
                    <option value="2">2 times</option>
                    <option value="3">3 times</option>
                    <option value="5">5 times</option>
                    <option value="10">10 times</option>
                </select>
            </div>
            
            <button onclick="applyAnimation()">Apply Animation</button>
            <button onclick="stopAnimation()" style="background-color: #f44336;">Stop Animation</button>
        </div>
        
        <div class="tab-content" id="advanced-tab">
            <h2>Advanced Controls</h2>
            <div class="form-group">
                <label for="custom-code">Custom JavaScript:</label>
                <textarea id="custom-code" rows="5" style="width: 100%; font-family: monospace; padding: 10px;">// Custom JavaScript to run in the browser</textarea>
            </div>
            <button onclick="executeCustomCode()">Execute</button>
            
            <div class="form-group" style="margin-top: 20px;">
                <label for="shape-attributes">Custom Shape Attributes:</label>
                <textarea id="shape-attributes" rows="3" style="width: 100%; font-family: monospace; padding: 10px;">{ "stroke-width": 3, "stroke-dasharray": "5,5" }</textarea>
            </div>
            <button onclick="applyCustomAttributes()">Apply to Current Shape</button>
        </div>
        
        <div id="svg-container">
            <!-- SVG will be inserted here -->
        </div>
        
        <div class="status-indicator">
            <div id="status">Ready. No shapes selected.</div>
        </div>
        
        <div class="log-container" id="log-container">
            <!-- Log entries will appear here -->
        </div>
    </div>
    
    <script>
        // Client-side JavaScript to communicate with our Flask API
        let selectedColor = "#3498db";
        
        // Initialize tabs
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                tab.classList.add('active');
                document.getElementById(tab.getAttribute('data-tab') + '-tab').classList.add('active');
            });
        });
        
        // Color picker
        document.querySelectorAll('.color-option').forEach(option => {
            option.addEventListener('click', () => {
                document.querySelectorAll('.color-option').forEach(o => o.classList.remove('selected'));
                option.classList.add('selected');
                selectedColor = option.getAttribute('data-color');
                log(`Selected color: ${selectedColor}`);
            });
        });
        
        function log(message) {
            const container = document.getElementById('log-container');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            container.appendChild(entry);
            container.scrollTop = container.scrollHeight;
        }
        
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
        
        function createShape(type) {
            fetch(`/create/${type}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    color: selectedColor
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    log(`Created ${type} with ID: ${data.id}`);
                    updateStatus(`Selected: ${type} (${data.id})`);
                } else {
                    log(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                log(`Error: ${error}`);
            });
        }
        
        function resetAnimations() {
            fetch('/reset', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                log('All animations reset');
                updateStatus('Ready. No shapes selected.');
            })
            .catch(error => {
                log(`Error: ${error}`);
            });
        }
        
        function applyAnimation() {
            const type = document.getElementById('animation-type').value;
            const duration = document.getElementById('animation-duration').value;
            const repeatCount = document.getElementById('repeat-count').value;
            
            fetch('/animate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: type,
                    duration: parseFloat(duration),
                    repeatCount: repeatCount
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    log(`Applied ${type} animation with duration ${duration}s`);
                } else {
                    log(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                log(`Error: ${error}`);
            });
        }
        
        function stopAnimation() {
            fetch('/stop-animation', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    log('Animation stopped');
                } else {
                    log(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                log(`Error: ${error}`);
            });
        }
        
        function executeCustomCode() {
            const code = document.getElementById('custom-code').value;
            
            fetch('/execute-js', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    log('Custom code executed successfully');
                    if (data.result) {
                        log(`Result: ${data.result}`);
                    }
                } else {
                    log(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                log(`Error: ${error}`);
            });
        }
        
        function applyCustomAttributes() {
            let attributes;
            try {
                attributes = JSON.parse(document.getElementById('shape-attributes').value);
            } catch (e) {
                log(`Error parsing JSON: ${e}`);
                return;
            }
            
            fetch('/set-attributes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    attributes: attributes
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    log('Custom attributes applied');
                } else {
                    log(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                log(`Error: ${error}`);
            });
        }
        
        // Initialize by creating the SVG
        fetch('/init', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                log(`SVG initialized with ID: ${data.id}`);
            } else {
                log(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            log(`Error: ${error}`);
        });
        
        // Log initial state
        log('SVG Animation MCP Demo loaded. Use the controls above to add shapes and animations.');
    </script>
</body>
</html>
""")

# Initialize MCP and SVG container
# Import and initialize browser_connection before initializing MCP
import browser_connection
browser_connection.initialize_browser()

# Now initialize MCP
mcp = MCP()
svg = None
current_element = None
elements = {}
animation_ids = {}

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/init', methods=['POST'])
def init():
    """Initialize the SVG container."""
    global svg, elements, animation_ids, current_element
    
    try:
        # If SVG was already initialized, clear it first
        if svg is not None:
            # Clear any existing state
            elements = {}
            animation_ids = {}
            current_element = None
        
        # Create a new SVG element with the proper container selector
        svg = mcp.create_svg(width=800, height=450, parent_selector="#svg-container")
        
        return jsonify({
            "status": "success", 
            "message": "SVG initialized", 
            "id": svg.id
        })
    except Exception as e:
        import traceback
        error_details = str(e) + "\n" + traceback.format_exc()
        print(f"Error initializing SVG: {error_details}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/create/<shape_type>', methods=['POST'])
def create_shape(shape_type):
    """Create a new shape in the SVG."""
    global svg, elements, current_element
    
    try:
        if svg is None:
            return jsonify({"status": "error", "message": "SVG not initialized"}), 400
        
        # Get color from request if available
        data = request.json or {}
        color = data.get('color', "#3498db")
        
        # Create different shapes based on the request
        if shape_type == 'circle':
            element = svg.add_circle(
                cx=200, cy=200, r=50,
                fill=color, stroke="#2980b9", stroke_width=2
            )
        elif shape_type == 'rectangle':
            element = svg.add_rectangle(
                x=300, y=150, width=150, height=100,
                fill=color, stroke="#2980b9", stroke_width=2
            )
        elif shape_type == 'text':
            element = svg.add_text(
                x=400, y=100, text="Hello SVG!",
                font_family="Arial", font_size=24, fill=color
            )
        elif shape_type == 'path':
            element = svg.add_path(
                d="M100,100 L200,100 L150,50 Z",
                fill=color, stroke="#2980b9", stroke_width=2
            )
        else:
            return jsonify({"status": "error", "message": f"Unknown shape type: {shape_type}"}), 400
            
        # Store the element in our global registry and set as current
        elements[element.id] = element
        current_element = element
        
        return jsonify({
            "status": "success",
            "message": f"Created {shape_type}",
            "id": element.id,
            "type": shape_type
        })
        
    except Exception as e:
        import traceback
        error_details = str(e) + "\n" + traceback.format_exc()
        print(f"Error creating {shape_type}: {error_details}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/animate', methods=['POST'])
def animate():
    """Apply an animation to the current element."""
    global current_element, animation_ids
    
    try:
        data = request.json
        element_id = data.get('id')
        animation_type = data.get('type', 'translate')
        duration = float(data.get('duration', 2.0))
        repeat_count = data.get('repeatCount', 'indefinite')
        
        # Make sure we have a selected element
        if element_id and element_id in elements:
            current_element = elements[element_id]
        elif current_element is None:
            return jsonify({"status": "error", "message": "No element selected"}), 400
        
        # Remove any existing animations for this element
        if current_element.id in animation_ids:
            try:
                current_element.remove_animation(animation_ids[current_element.id])
            except Exception as e:
                # Just log the error and continue
                print(f"Error removing animation: {str(e)}")
        
        animation_id = None
        
        if animation_type == 'translate':
            animation_id = current_element.animate_transform(
                transform_type="translate",
                from_value="0 0",
                to_value="100 50",
                duration=duration,
                repeat_count=repeat_count
            )
        elif animation_type == 'rotate':
            animation_id = current_element.animate_transform(
                transform_type="rotate",
                from_value="0 150 150",
                to_value="360 150 150",
                duration=duration,
                repeat_count=repeat_count
            )
        elif animation_type == 'scale':
            animation_id = current_element.animate_transform(
                transform_type="scale",
                from_value="1",
                to_value="1.5",
                duration=duration,
                repeat_count=repeat_count
            )
        elif animation_type == 'color':
            animation_id = current_element.animate(
                attribute="fill",
                from_value="#3498db",
                to_value="#e74c3c",
                duration=duration,
                repeat_count=repeat_count
            )
        else:
            return jsonify({"status": "error", "message": f"Unknown animation type: {animation_type}"}), 400
        
        if animation_id:
            animation_ids[current_element.id] = animation_id
        
        return jsonify({
            "status": "success",
            "message": f"{animation_type} animation applied",
            "animation_id": animation_id
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stop-animation', methods=['POST'])
def stop_animation():
    """Stop the animation on the current element."""
    global current_element, animation_ids
    
    try:
        data = request.json
        element_id = data.get('id')
        
        # Make sure we have a selected element
        if element_id and element_id in elements:
            current_element = elements[element_id]
        elif current_element is None:
            return jsonify({"status": "error", "message": "No element selected"}), 400
        
        # Check if this element has any animations
        if current_element.id in animation_ids:
            # Remove the animation
            try:
                current_element.remove_animation(animation_ids[current_element.id])
                del animation_ids[current_element.id]
                return jsonify({
                    "status": "success",
                    "message": "Animation stopped"
                })
            except Exception as e:
                return jsonify({"status": "error", "message": f"Error stopping animation: {str(e)}"}), 500
        else:
            # No animation to stop for this element
            return jsonify({
                "status": "success",
                "message": "No animation to stop"
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/execute-js', methods=['POST'])
def execute_js():
    """Execute custom JavaScript code."""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({"status": "error", "message": "No code provided"}), 400
            
        result = mcp.execute_js(code)
        
        return jsonify({
            "status": "success",
            "message": "JavaScript executed",
            "result": str(result) if result is not None else None
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set-attributes', methods=['POST'])
def set_attributes():
    """Set attributes on the current element."""
    global current_element
    
    try:
        data = request.json
        element_id = data.get('id')
        attributes = data.get('attributes', {})
        
        # Make sure we have a selected element
        if element_id and element_id in elements:
            current_element = elements[element_id]
        elif current_element is None:
            return jsonify({"status": "error", "message": "No element selected"}), 400
        
        # Set each attribute
        for attr, value in attributes.items():
            try:
                current_element.set_attribute(attr, value)
            except Exception as e:
                return jsonify({"status": "error", "message": f"Error setting attribute {attr}: {str(e)}"}), 500
        
        return jsonify({
            "status": "success",
            "message": "Attributes set successfully"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset all elements and animations."""
    global svg, elements, current_element, animation_ids
    
    try:
        # Remove all elements
        if svg:
            # Find all elements and remove them
            script = """
            (function() {
                var svgElement = document.getElementById('%s');
                if (svgElement) {
                    // Remove all child elements except defs
                    var children = Array.from(svgElement.childNodes);
                    for (var i = 0; i < children.length; i++) {
                        var child = children[i];
                        if (child.tagName && child.tagName.toLowerCase() !== 'defs') {
                            svgElement.removeChild(child);
                        }
                    }
                    return true;
                }
                return false;
            })();
            """ % svg.id
            
            execute_js(script)
        
        # Reset our state
        elements = {}
        current_element = None
        animation_ids = {}
        
        return jsonify({
            "status": "success",
            "message": "All elements and animations reset"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/remove', methods=['POST'])
def remove_element():
    """Remove the specified element from the SVG."""
    global elements
    
    try:
        data = request.json
        element_id = data.get('id')
        
        if not element_id:
            return jsonify({"status": "error", "message": "No element ID provided"}), 400
        
        # Find the element in our elements dictionary
        if element_id in elements:
            element = elements[element_id]
            
            # Use the shape's remove method if available
            if hasattr(element, 'remove'):
                element.remove()
                
            # Remove from our elements dictionary
            del elements[element_id]
            
            return jsonify({
                "status": "success",
                "message": f"Element {element_id} removed successfully"
            })
        else:
            return jsonify({"status": "error", "message": f"Element {element_id} not found"}), 404
            
    except Exception as e:
        import traceback
        error_details = str(e) + "\n" + traceback.format_exc()
        print(f"Error removing element: {error_details}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/select', methods=['POST'])
def select_element():
    """Select an element for manipulation."""
    global current_element, elements
    
    try:
        data = request.json or {}
        element_id = data.get('id')
        
        if element_id:
            # If an ID is provided, try to find that specific element
            if element_id in elements:
                current_element = elements[element_id]
                return jsonify({
                    "status": "success",
                    "message": f"Selected element with ID {element_id}",
                    "id": element_id
                })
            else:
                return jsonify({"status": "error", "message": f"Element with ID {element_id} not found"}), 404
        else:
            # No ID provided, so just get the last element created
            if not elements:
                return jsonify({"status": "error", "message": "No elements available to select"}), 400
                
            # Get the last element created (highest ID number)
            # This is a simple heuristic that works for our element ID format
            last_id = sorted(elements.keys(), key=lambda k: int(k.split('_')[-1]) if k.split('_')[-1].isdigit() else 0)[-1]
            current_element = elements[last_id]
            
            return jsonify({
                "status": "success",
                "message": f"Selected last created element",
                "id": last_id
            })
            
    except Exception as e:
        import traceback
        error_details = str(e) + "\n" + traceback.format_exc()
        print(f"Error selecting element: {error_details}")
        return jsonify({"status": "error", "message": str(e)}), 500

def open_browser():
    """Open the browser after a short delay."""
    time.sleep(1.5)  # Wait for Flask to start
    url = f"http://localhost:{PORT}"
    print(f"Opening browser at {url}")
    # Only open the main page, not the renderer
    webbrowser.open(url)

if __name__ == '__main__':
    print("Starting Flask app for SVG Animation MCP...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the Flask app with the new port
    app.run(debug=False, port=PORT)  # Set debug=False for production use 