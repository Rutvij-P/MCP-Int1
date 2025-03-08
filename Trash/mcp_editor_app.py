"""
SVG Editor MCP - Interactive UI with Instant Visual Feedback

This application provides a web-based interface for creating and editing SVG elements
with immediate visual feedback and a user-friendly interface.
"""

from flask import Flask, render_template, request, jsonify, url_for, redirect
import browser_connection  # Import browser_connection first
import browser_integration  # Then import browser_integration
from svg_animation_mcp import MCP
import os
import json
import atexit
import signal
import sys
import webbrowser
import threading
import time

# Use a dedicated port for the editor
PORT = 5002

# Initialize browser integration before creating the Flask app
browser_integration.initialize()

app = Flask(__name__)

# Initialize MCP instance
mcp = MCP()

# Register shutdown function
atexit.register(browser_connection.shutdown)

# Handle signals for clean shutdown
def signal_handler(sig, frame):
    print("\nShutting down editor application...")
    browser_connection.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Ensure templates and static directories exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# SVG object to track the current state
svg = None

@app.route('/')
def index():
    """Render the main editor page."""
    return render_template('editor.html')

@app.route('/create_svg', methods=['POST'])
def create_svg():
    """Create a new SVG canvas with the specified dimensions."""
    global svg
    
    data = request.json
    width = data.get('width', 800)
    height = data.get('height', 600)
    
    # Create the SVG using MCP
    svg = mcp.create_svg(width=width, height=height, parent_selector="#svg-canvas")
    
    return jsonify({
        'status': 'success',
        'svg_id': svg.id,
        'width': width,
        'height': height
    })

@app.route('/add_shape', methods=['POST'])
def add_shape():
    """Add a shape to the SVG."""
    global svg
    
    if not svg:
        return jsonify({'status': 'error', 'message': 'No SVG canvas created yet'})
    
    data = request.json
    shape_type = data.get('type')
    properties = data.get('properties', {})
    
    try:
        # Create the shape based on type
        if shape_type == 'rectangle':
            shape = svg.add_rectangle(
                x=properties.get('x', 0),
                y=properties.get('y', 0),
                width=properties.get('width', 100),
                height=properties.get('height', 100),
                fill=properties.get('fill', '#3498db'),
                stroke=properties.get('stroke', '#2980b9'),
                stroke_width=properties.get('stroke_width', 2)
            )
        elif shape_type == 'circle':
            shape = svg.add_circle(
                cx=properties.get('cx', 100),
                cy=properties.get('cy', 100),
                r=properties.get('r', 50),
                fill=properties.get('fill', '#e74c3c'),
                stroke=properties.get('stroke', '#c0392b'),
                stroke_width=properties.get('stroke_width', 2)
            )
        elif shape_type == 'text':
            shape = svg.add_text(
                x=properties.get('x', 100),
                y=properties.get('y', 100),
                text=properties.get('text', 'SVG Text'),
                font_family=properties.get('font_family', 'Arial'),
                font_size=properties.get('font_size', 24),
                fill=properties.get('fill', '#2c3e50')
            )
        else:
            return jsonify({'status': 'error', 'message': f'Unsupported shape type: {shape_type}'})
        
        return jsonify({
            'status': 'success',
            'shape_id': shape.id,
            'type': shape_type
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/update_shape', methods=['POST'])
def update_shape():
    """Update properties of an existing shape."""
    data = request.json
    shape_id = data.get('shape_id')
    properties = data.get('properties', {})
    
    try:
        # Use JavaScript to update the shape directly for instant feedback
        for attr, value in properties.items():
            js_code = f"""
            (function() {{
                var element = document.getElementById('{shape_id}');
                if (element) {{
                    element.setAttribute('{attr}', '{value}');
                    return true;
                }}
                return false;
            }})();
            """
            result = browser_connection.execute_js(js_code)
            
            if not result:
                return jsonify({'status': 'error', 'message': f'Element with ID {shape_id} not found'})
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_svg_code', methods=['GET'])
def get_svg_code():
    """Get the current SVG code."""
    try:
        js_code = """
        (function() {
            var svgElement = document.querySelector('#svg-canvas svg');
            if (svgElement) {
                return svgElement.outerHTML;
            }
            return '';
        })();
        """
        svg_code = browser_connection.execute_js(js_code)
        
        return jsonify({'status': 'success', 'svg_code': svg_code})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def open_browser():
    """Open a browser window after a short delay."""
    time.sleep(1.5)
    url = f"http://localhost:{PORT}/"
    print(f"Opening browser at: {url}")
    webbrowser.open(url)

if __name__ == '__main__':
    # Create the editor HTML template
    with open('templates/editor.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG Editor MCP</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/editor.css') }}">
    <style>
        /* Basic styles for the editor */
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            overflow: hidden;
        }
        
        .svg-editor-container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        .toolbar {
            background-color: #2c3e50;
            color: white;
            padding: 10px;
            display: flex;
            align-items: center;
        }
        
        .tool-button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            margin-right: 10px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .tool-button:hover {
            background-color: #2980b9;
        }
        
        .workspace {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        .canvas-container {
            flex: 1;
            background-color: white;
            overflow: auto;
            position: relative;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1) inset;
        }
        
        #svg-canvas {
            min-width: 800px;
            min-height: 600px;
            background-color: white;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            margin: 20px;
            overflow: visible;
        }
        
        .properties-panel {
            width: 300px;
            background-color: #ecf0f1;
            padding: 15px;
            overflow-y: auto;
            box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
        }
        
        .property-group {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #ddd;
        }
        
        .property-group h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        
        .property-row {
            display: flex;
            margin-bottom: 8px;
            align-items: center;
        }
        
        .property-label {
            width: 100px;
            font-size: 14px;
            color: #333;
        }
        
        .property-input {
            flex: 1;
            padding: 6px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        
        .status-bar {
            background-color: #34495e;
            color: white;
            padding: 5px 10px;
            font-size: 12px;
            display: flex;
            justify-content: space-between;
        }
        
        .color-input {
            width: 80px;
            padding: 0;
            height: 28px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="svg-editor-container">
        <!-- Main toolbar -->
        <div class="toolbar">
            <h2 style="margin-right: 20px;">SVG Editor</h2>
            <button class="tool-button" id="new-svg-btn">New Canvas</button>
            <button class="tool-button" id="rectangle-btn">Rectangle</button>
            <button class="tool-button" id="circle-btn">Circle</button>
            <button class="tool-button" id="text-btn">Text</button>
            <button class="tool-button" id="view-code-btn">View SVG Code</button>
        </div>
        
        <!-- Main workspace area -->
        <div class="workspace">
            <!-- SVG canvas with instant preview -->
            <div class="canvas-container">
                <div id="svg-canvas"></div>
            </div>
            
            <!-- Properties panel -->
            <div class="properties-panel">
                <div id="canvas-properties" class="property-group">
                    <h3>Canvas Properties</h3>
                    <div class="property-row">
                        <label class="property-label">Width:</label>
                        <input type="number" id="canvas-width" class="property-input" value="800">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Height:</label>
                        <input type="number" id="canvas-height" class="property-input" value="600">
                    </div>
                    <div class="property-row">
                        <button id="apply-canvas-btn" class="tool-button">Apply</button>
                    </div>
                </div>
                
                <div id="shape-properties" class="property-group" style="display: none;">
                    <h3>Shape Properties</h3>
                    <div id="shape-properties-container">
                        <!-- Dynamic shape properties will appear here -->
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Status bar -->
        <div class="status-bar">
            <div id="position-info">Position: 0, 0</div>
            <div id="shape-info">No selection</div>
        </div>
    </div>
    
    <!-- SVG Code Modal -->
    <div id="code-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000;">
        <div style="position: relative; width: 80%; height: 80%; margin: 5% auto; background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 20px rgba(0,0,0,0.3);">
            <button id="close-modal-btn" style="position: absolute; top: 10px; right: 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; padding: 5px 10px; cursor: pointer;">Close</button>
            <h3>SVG Code</h3>
            <pre id="svg-code-display" style="width: 100%; height: 85%; overflow: auto; background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd; white-space: pre-wrap;"></pre>
        </div>
    </div>
    
    <script>
        // Global variables
        let currentSvgId = null;
        let selectedShapeId = null;
        let currentTool = null;
        
        // DOM elements
        const svgCanvas = document.getElementById('svg-canvas');
        const canvasWidth = document.getElementById('canvas-width');
        const canvasHeight = document.getElementById('canvas-height');
        const applyCanvasBtn = document.getElementById('apply-canvas-btn');
        const newSvgBtn = document.getElementById('new-svg-btn');
        const rectangleBtn = document.getElementById('rectangle-btn');
        const circleBtn = document.getElementById('circle-btn');
        const textBtn = document.getElementById('text-btn');
        const viewCodeBtn = document.getElementById('view-code-btn');
        const codeModal = document.getElementById('code-modal');
        const closeModalBtn = document.getElementById('close-modal-btn');
        const svgCodeDisplay = document.getElementById('svg-code-display');
        const shapePropertiesPanel = document.getElementById('shape-properties');
        const shapePropertiesContainer = document.getElementById('shape-properties-container');
        const positionInfo = document.getElementById('position-info');
        const shapeInfo = document.getElementById('shape-info');
        
        // Initialize the SVG canvas
        function createSvgCanvas() {
            const width = parseInt(canvasWidth.value);
            const height = parseInt(canvasHeight.value);
            
            fetch('/create_svg', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    width: width,
                    height: height
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('SVG canvas created:', data);
                currentSvgId = data.svg_id;
                
                // Update canvas size
                svgCanvas.style.width = width + 'px';
                svgCanvas.style.height = height + 'px';
            })
            .catch((error) => {
                console.error('Error creating SVG canvas:', error);
            });
        }
        
        // Add a shape to the canvas
        function addShape(type, properties) {
            fetch('/add_shape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: type,
                    properties: properties
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(`${type} added:`, data);
                if (data.status === 'success') {
                    selectedShapeId = data.shape_id;
                    showShapeProperties(type, selectedShapeId, properties);
                    shapeInfo.textContent = `Selected: ${type} (${data.shape_id})`;
                }
            })
            .catch((error) => {
                console.error(`Error adding ${type}:`, error);
            });
        }
        
        // Update a shape's properties
        function updateShape(shapeId, properties) {
            fetch('/update_shape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    shape_id: shapeId,
                    properties: properties
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Shape updated:', data);
            })
            .catch((error) => {
                console.error('Error updating shape:', error);
            });
        }
        
        // Show shape properties in the panel
        function showShapeProperties(type, shapeId, properties) {
            // Clear existing properties
            shapePropertiesContainer.innerHTML = '';
            
            // Create property inputs based on shape type
            let propertyInputs = '';
            
            if (type === 'rectangle') {
                propertyInputs = `
                    <div class="property-row">
                        <label class="property-label">X:</label>
                        <input type="number" id="prop-x" class="property-input" value="${properties.x || 0}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Y:</label>
                        <input type="number" id="prop-y" class="property-input" value="${properties.y || 0}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Width:</label>
                        <input type="number" id="prop-width" class="property-input" value="${properties.width || 100}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Height:</label>
                        <input type="number" id="prop-height" class="property-input" value="${properties.height || 100}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Fill:</label>
                        <input type="color" id="prop-fill" class="property-input color-input" value="${properties.fill || '#3498db'}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Stroke:</label>
                        <input type="color" id="prop-stroke" class="property-input color-input" value="${properties.stroke || '#2980b9'}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Stroke Width:</label>
                        <input type="number" id="prop-stroke-width" class="property-input" value="${properties.stroke_width || 2}">
                    </div>
                `;
            } else if (type === 'circle') {
                propertyInputs = `
                    <div class="property-row">
                        <label class="property-label">Center X:</label>
                        <input type="number" id="prop-cx" class="property-input" value="${properties.cx || 100}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Center Y:</label>
                        <input type="number" id="prop-cy" class="property-input" value="${properties.cy || 100}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Radius:</label>
                        <input type="number" id="prop-r" class="property-input" value="${properties.r || 50}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Fill:</label>
                        <input type="color" id="prop-fill" class="property-input color-input" value="${properties.fill || '#e74c3c'}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Stroke:</label>
                        <input type="color" id="prop-stroke" class="property-input color-input" value="${properties.stroke || '#c0392b'}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Stroke Width:</label>
                        <input type="number" id="prop-stroke-width" class="property-input" value="${properties.stroke_width || 2}">
                    </div>
                `;
            } else if (type === 'text') {
                propertyInputs = `
                    <div class="property-row">
                        <label class="property-label">X:</label>
                        <input type="number" id="prop-x" class="property-input" value="${properties.x || 100}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Y:</label>
                        <input type="number" id="prop-y" class="property-input" value="${properties.y || 100}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Text:</label>
                        <input type="text" id="prop-text" class="property-input" value="${properties.text || 'SVG Text'}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Font Family:</label>
                        <select id="prop-font-family" class="property-input">
                            <option value="Arial" ${(properties.font_family || 'Arial') === 'Arial' ? 'selected' : ''}>Arial</option>
                            <option value="Helvetica" ${(properties.font_family || 'Arial') === 'Helvetica' ? 'selected' : ''}>Helvetica</option>
                            <option value="Times New Roman" ${(properties.font_family || 'Arial') === 'Times New Roman' ? 'selected' : ''}>Times New Roman</option>
                            <option value="Courier New" ${(properties.font_family || 'Arial') === 'Courier New' ? 'selected' : ''}>Courier New</option>
                        </select>
                    </div>
                    <div class="property-row">
                        <label class="property-label">Font Size:</label>
                        <input type="number" id="prop-font-size" class="property-input" value="${properties.font_size || 24}">
                    </div>
                    <div class="property-row">
                        <label class="property-label">Fill:</label>
                        <input type="color" id="prop-fill" class="property-input color-input" value="${properties.fill || '#2c3e50'}">
                    </div>
                `;
            }
            
            // Add apply button
            propertyInputs += `
                <div class="property-row" style="margin-top: 15px;">
                    <button id="apply-properties-btn" class="tool-button">Apply Changes</button>
                </div>
            `;
            
            // Set content and show the panel
            shapePropertiesContainer.innerHTML = propertyInputs;
            shapePropertiesPanel.style.display = 'block';
            
            // Add event listener to the apply button
            document.getElementById('apply-properties-btn').addEventListener('click', () => {
                const updatedProperties = {};
                
                // Get updated properties based on shape type
                if (type === 'rectangle') {
                    updatedProperties.x = document.getElementById('prop-x').value;
                    updatedProperties.y = document.getElementById('prop-y').value;
                    updatedProperties.width = document.getElementById('prop-width').value;
                    updatedProperties.height = document.getElementById('prop-height').value;
                    updatedProperties.fill = document.getElementById('prop-fill').value;
                    updatedProperties.stroke = document.getElementById('prop-stroke').value;
                    updatedProperties.stroke_width = document.getElementById('prop-stroke-width').value;
                } else if (type === 'circle') {
                    updatedProperties.cx = document.getElementById('prop-cx').value;
                    updatedProperties.cy = document.getElementById('prop-cy').value;
                    updatedProperties.r = document.getElementById('prop-r').value;
                    updatedProperties.fill = document.getElementById('prop-fill').value;
                    updatedProperties.stroke = document.getElementById('prop-stroke').value;
                    updatedProperties.stroke_width = document.getElementById('prop-stroke-width').value;
                } else if (type === 'text') {
                    updatedProperties.x = document.getElementById('prop-x').value;
                    updatedProperties.y = document.getElementById('prop-y').value;
                    updatedProperties.text = document.getElementById('prop-text').value;
                    updatedProperties.font_family = document.getElementById('prop-font-family').value;
                    updatedProperties.font_size = document.getElementById('prop-font-size').value;
                    updatedProperties.fill = document.getElementById('prop-fill').value;
                }
                
                // Update the shape
                updateShape(shapeId, updatedProperties);
            });
        }
        
        // Show SVG code in modal
        function showSvgCode() {
            fetch('/get_svg_code')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        svgCodeDisplay.textContent = data.svg_code;
                        codeModal.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error fetching SVG code:', error);
                });
        }
        
        // Event Listeners
        document.addEventListener('DOMContentLoaded', () => {
            // Create initial SVG canvas
            createSvgCanvas();
            
            // Canvas property changes
            applyCanvasBtn.addEventListener('click', createSvgCanvas);
            
            // Tool buttons
            newSvgBtn.addEventListener('click', createSvgCanvas);
            
            rectangleBtn.addEventListener('click', () => {
                currentTool = 'rectangle';
                addShape('rectangle', {
                    x: 100,
                    y: 100,
                    width: 150,
                    height: 100,
                    fill: '#3498db',
                    stroke: '#2980b9',
                    stroke_width: 2
                });
            });
            
            circleBtn.addEventListener('click', () => {
                currentTool = 'circle';
                addShape('circle', {
                    cx: 200,
                    cy: 200,
                    r: 50,
                    fill: '#e74c3c',
                    stroke: '#c0392b',
                    stroke_width: 2
                });
            });
            
            textBtn.addEventListener('click', () => {
                currentTool = 'text';
                addShape('text', {
                    x: 150,
                    y: 150,
                    text: 'SVG Text',
                    font_family: 'Arial',
                    font_size: 24,
                    fill: '#2c3e50'
                });
            });
            
            // View code button
            viewCodeBtn.addEventListener('click', showSvgCode);
            closeModalBtn.addEventListener('click', () => {
                codeModal.style.display = 'none';
            });
            
            // Mouse position tracking
            svgCanvas.addEventListener('mousemove', (e) => {
                const rect = svgCanvas.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                positionInfo.textContent = `Position: ${x}, ${y}`;
            });
            
            // Close modal when clicking outside
            window.addEventListener('click', (e) => {
                if (e.target === codeModal) {
                    codeModal.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>""")
    
    # Create stylesheet
    with open('static/css/editor.css', 'w') as f:
        f.write("""/* Additional styles for the editor will go here */""")
    
    # Start the browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=PORT, debug=False) 