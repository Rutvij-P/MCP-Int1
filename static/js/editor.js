/**
 * SVG Animation Editor - Frontend JavaScript
 * 
 * This script handles the interaction between the frontend and the server,
 * as well as the SVG manipulation and animation features.
 */

// Initialize the Vue application when the DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Create the Vue application
    new Vue({
        el: '#app',
        data: {
            socket: null,
            draw: null,
            currentSvgId: null,
            elements: {},
            animations: [],
            selectedElement: null,
            currentTool: 'select',
            promptText: '',
            promptHistory: [],
            codeEditor: null,
            currentStatus: 'Ready',
            toastMessage: '',
            toastVisible: false,
            toastTimeout: null
        },
        methods: {
            initSocket() {
                // Initialize Socket.IO connection
                this.socket = io();
                
                // Set up event listeners for Socket.IO events
                this.socket.on('connect', () => {
                    console.log('Connected to server');
                    this.showToast('Connected to server');
                });
                
                this.socket.on('svg_created', data => {
                    console.log('SVG created:', data);
                    this.currentSvgId = data.svg_id;
                    this.initSVG(data.width, data.height);
                    if (data.prompt) {
                        this.addToPromptHistory(data.prompt);
                    }
                });
                
                this.socket.on('element_created', data => {
                    console.log('Element created:', data);
                    this.createElement(data);
                });
                
                this.socket.on('element_updated', data => {
                    console.log('Element updated:', data);
                    this.updateElementFromServer(data);
                });
                
                this.socket.on('animation_created', data => {
                    console.log('Animation created:', data);
                    this.createAnimation(data);
                });
                
                this.socket.on('prompt_received', data => {
                    console.log('Prompt received:', data);
                    this.addToPromptHistory(data.prompt);
                });
                
                this.socket.on('svg_data', data => {
                    console.log('Initial SVG data received:', data);
                    this.loadSVGData(data);
                });
                
                this.socket.on('export_result', data => {
                    console.log('Export result:', data);
                    if (data.success) {
                        this.showToast('SVG exported successfully');
                    } else {
                        this.showToast('Error exporting SVG: ' + data.message);
                    }
                });
                
                this.socket.on('canvas_reset', data => {
                    console.log('Canvas reset by server');
                    this.resetCanvasLocally(data.width || DEFAULT_SVG_WIDTH, data.height || DEFAULT_SVG_HEIGHT);
                });
            },
            
            resetCanvas() {
                if (!this.socket) return;
                
                // Confirm with the user before resetting
                if (confirm('Are you sure you want to reset the canvas? All elements will be removed.')) {
                    // Send reset request to the server
                    this.socket.emit('reset_canvas', {
                        width: DEFAULT_SVG_WIDTH,
                        height: DEFAULT_SVG_HEIGHT
                    });
                    
                    // Reset locally
                    this.resetCanvasLocally(DEFAULT_SVG_WIDTH, DEFAULT_SVG_HEIGHT);
                    
                    // Show a confirmation message
                    this.showToast('Canvas has been reset');
                }
            },
            
            resetCanvasLocally(width, height) {
                // Clear all elements and animations
                this.elements = {};
                this.animations = [];
                this.selectedElement = null;
                
                // Reinitialize the SVG
                this.initSVG(width, height);
                
                // Update the code editor
                this.updateCodeEditor();
            },
            
            initSVG(width, height) {
                // Clear any existing SVG
                const container = document.getElementById('svg-canvas');
                container.innerHTML = '';
                
                // Create a new SVG.js drawing
                this.draw = SVG().addTo('#svg-canvas').size(width, height);
                
                // Update the code editor
                this.updateCodeEditor();
                
                // Set current status
                this.currentStatus = 'Canvas ready';
            },
            
            createElement(data) {
                if (!this.draw) return;
                
                const { element_id, parent_id, type, properties } = data;
                let element;
                
                // Create the element based on its type
                switch (type) {
                    case 'rect':
                        element = this.draw.rect(properties.width, properties.height)
                            .move(properties.x, properties.y);
                        break;
                    case 'circle':
                        element = this.draw.circle(properties.r * 2)
                            .center(properties.cx, properties.cy);
                        break;
                    case 'text':
                        element = this.draw.text(properties.text)
                            .move(properties.x, properties.y);
                        break;
                    case 'path':
                        element = this.draw.path(properties.d);
                        break;
                    default:
                        console.error('Unknown element type:', type);
                        return;
                }
                
                // Apply styles and other properties
                if (properties.fill) element.fill(properties.fill);
                if (properties.stroke) element.stroke(properties.stroke);
                if (properties['stroke-width']) element.stroke({ width: properties['stroke-width'] });
                
                // Store the element for future reference
                this.elements[element_id] = {
                    id: element_id,
                    type: type,
                    element: element,
                    properties: { ...properties }
                };
                
                // Make the element clickable for selection
                element.click(this.selectElementHandler(element_id));
                
                // Update the code editor
                this.updateCodeEditor();
            },
            
            selectElementHandler(elementId) {
                return () => {
                    this.selectElement(elementId);
                };
            },
            
            selectElement(elementId) {
                // Deselect previously selected element
                if (this.selectedElement && this.elements[this.selectedElement.id]) {
                    const prevElement = this.elements[this.selectedElement.id].element;
                    prevElement.stroke({ width: this.selectedElement['stroke-width'] || 1 });
                }
                
                // Select the new element
                if (this.elements[elementId]) {
                    const element = this.elements[elementId];
                    const props = element.properties;
                    
                    // Highlight the selected element
                    element.element.stroke({ width: (props['stroke-width'] || 1) + 2 });
                    
                    // Set the selected element for property editing
                    this.selectedElement = {
                        id: elementId,
                        type: element.type,
                        ...props
                    };
                } else {
                    this.selectedElement = null;
                }
            },
            
            updateElement() {
                if (!this.selectedElement || !this.elements[this.selectedElement.id]) return;
                
                const elementId = this.selectedElement.id;
                const element = this.elements[elementId].element;
                const type = this.selectedElement.type;
                
                // Update the element based on its type
                switch (type) {
                    case 'rect':
                        element.move(this.selectedElement.x, this.selectedElement.y)
                            .size(this.selectedElement.width, this.selectedElement.height);
                        break;
                    case 'circle':
                        element.radius(this.selectedElement.r)
                            .center(this.selectedElement.cx, this.selectedElement.cy);
                        break;
                    case 'text':
                        element.text(this.selectedElement.text)
                            .move(this.selectedElement.x, this.selectedElement.y)
                            .font({ size: this.selectedElement['font-size'] });
                        break;
                }
                
                // Update styles
                element.fill(this.selectedElement.fill)
                    .stroke({
                        color: this.selectedElement.stroke,
                        width: this.selectedElement['stroke-width']
                    });
                
                // Update stored properties
                this.elements[elementId].properties = { ...this.selectedElement };
                
                // Emit the update to the server
                this.socket.emit('element_updated', {
                    element_id: elementId,
                    properties: { ...this.selectedElement }
                });
                
                // Update the code editor
                this.updateCodeEditor();
            },
            
            updateElementFromServer(data) {
                const { element_id, properties } = data;
                if (!this.elements[element_id]) return;
                
                const element = this.elements[element_id].element;
                const type = this.elements[element_id].type;
                
                // Update the element based on its type
                switch (type) {
                    case 'rect':
                        if (properties.x !== undefined && properties.y !== undefined) {
                            element.move(properties.x, properties.y);
                        }
                        if (properties.width !== undefined && properties.height !== undefined) {
                            element.size(properties.width, properties.height);
                        }
                        break;
                    case 'circle':
                        if (properties.r !== undefined) {
                            element.radius(properties.r);
                        }
                        if (properties.cx !== undefined && properties.cy !== undefined) {
                            element.center(properties.cx, properties.cy);
                        }
                        break;
                    case 'text':
                        if (properties.text !== undefined) {
                            element.text(properties.text);
                        }
                        if (properties.x !== undefined && properties.y !== undefined) {
                            element.move(properties.x, properties.y);
                        }
                        if (properties['font-size'] !== undefined) {
                            element.font({ size: properties['font-size'] });
                        }
                        break;
                }
                
                // Update styles
                if (properties.fill !== undefined) {
                    element.fill(properties.fill);
                }
                if (properties.stroke !== undefined || properties['stroke-width'] !== undefined) {
                    element.stroke({
                        color: properties.stroke,
                        width: properties['stroke-width']
                    });
                }
                
                // Update stored properties
                Object.assign(this.elements[element_id].properties, properties);
                
                // Update the selected element if it's the one being updated
                if (this.selectedElement && this.selectedElement.id === element_id) {
                    Object.assign(this.selectedElement, properties);
                }
                
                // Update the code editor
                this.updateCodeEditor();
            },
            
            createAnimation(data) {
                const { animation_id, element_id, attribute, from, to, duration, repeat } = data;
                if (!this.elements[element_id]) return;
                
                const element = this.elements[element_id].element;
                
                // Create the animation based on the attribute
                let animation;
                switch (attribute) {
                    case 'r':
                        animation = element.animate(duration * 1000, repeat === 'indefinite' ? -1 : repeat).radius(to);
                        break;
                    case 'cx':
                    case 'cy':
                        // For now, we'll just animate the center for circles
                        if (this.elements[element_id].type === 'circle') {
                            animation = element.animate(duration * 1000, repeat === 'indefinite' ? -1 : repeat).center(
                                attribute === 'cx' ? to : element.cx(),
                                attribute === 'cy' ? to : element.cy()
                            );
                        }
                        break;
                    case 'fill':
                        animation = element.animate(duration * 1000, repeat === 'indefinite' ? -1 : repeat).fill(to);
                        break;
                    // Add more attribute cases as needed
                    case 'x':
                    case 'y':
                        if (this.elements[element_id].type === 'rect' || this.elements[element_id].type === 'text') {
                            const currentX = this.elements[element_id].properties.x;
                            const currentY = this.elements[element_id].properties.y;
                            animation = element.animate(duration * 1000, repeat === 'indefinite' ? -1 : repeat).move(
                                attribute === 'x' ? to : currentX,
                                attribute === 'y' ? to : currentY
                            );
                        }
                        break;
                    case 'width':
                    case 'height':
                        if (this.elements[element_id].type === 'rect') {
                            const currentWidth = this.elements[element_id].properties.width;
                            const currentHeight = this.elements[element_id].properties.height;
                            animation = element.animate(duration * 1000, repeat === 'indefinite' ? -1 : repeat).size(
                                attribute === 'width' ? to : currentWidth,
                                attribute === 'height' ? to : currentHeight
                            );
                        }
                        break;
                }
                
                // Store the animation for future reference
                if (animation) {
                    this.animations.push({
                        id: animation_id,
                        element_id: element_id,
                        attribute: attribute,
                        animation: animation,
                        duration: duration,
                        repeat: repeat
                    });
                }
                
                // Update the code editor
                this.updateCodeEditor();
            },
            
            selectTool(tool) {
                this.currentTool = tool;
                this.currentStatus = `Tool: ${tool}`;
                
                // If user selected a shape tool, prepare for creation
                if (tool !== 'select') {
                    // Implement drawing logic for shape creation
                    this.setupDrawingEvents(tool);
                } else {
                    // Remove drawing event listeners
                    this.removeDrawingEvents();
                }
            },
            
            setupDrawingEvents(tool) {
                // First, remove any existing event listeners
                this.removeDrawingEvents();
                
                // Get the canvas container
                const container = document.getElementById('svg-canvas');
                
                if (!this.draw) return;
                
                // Add event listeners based on the selected tool
                switch (tool) {
                    case 'rectangle':
                        // Setup rectangle drawing
                        this.draw.on('mousedown', this.handleRectangleStart.bind(this));
                        break;
                    case 'circle':
                        // Setup circle drawing
                        this.draw.on('mousedown', this.handleCircleStart.bind(this));
                        break;
                    case 'text':
                        // Setup text creation
                        this.draw.on('click', this.handleTextCreate.bind(this));
                        break;
                    case 'path':
                        // Setup path drawing
                        this.draw.on('mousedown', this.handlePathStart.bind(this));
                        break;
                }
            },
            
            removeDrawingEvents() {
                if (!this.draw) return;
                
                // Remove all event listeners
                this.draw.off('mousedown');
                this.draw.off('mousemove');
                this.draw.off('mouseup');
                this.draw.off('click');
            },
            
            handleRectangleStart(event) {
                if (!this.currentSvgId) return;
                
                const startX = event.clientX - this.draw.node.getBoundingClientRect().left;
                const startY = event.clientY - this.draw.node.getBoundingClientRect().top;
                
                // Create a temporary rectangle
                const rect = this.draw.rect(1, 1).move(startX, startY).fill('#3498db').stroke('#2980b9');
                
                // Setup mousemove handler
                const moveHandler = (e) => {
                    const currentX = e.clientX - this.draw.node.getBoundingClientRect().left;
                    const currentY = e.clientY - this.draw.node.getBoundingClientRect().top;
                    
                    const width = Math.abs(currentX - startX);
                    const height = Math.abs(currentY - startY);
                    const x = Math.min(startX, currentX);
                    const y = Math.min(startY, currentY);
                    
                    rect.size(width, height).move(x, y);
                };
                
                // Setup mouseup handler
                const upHandler = () => {
                    // Remove the temporary handlers
                    this.draw.off('mousemove', moveHandler);
                    this.draw.off('mouseup', upHandler);
                    
                    // Get the final rectangle properties
                    const x = parseFloat(rect.x());
                    const y = parseFloat(rect.y());
                    const width = parseFloat(rect.width());
                    const height = parseFloat(rect.height());
                    
                    // Remove the temporary rectangle
                    rect.remove();
                    
                    // Only create if it has some size
                    if (width > 5 && height > 5) {
                        // Create a real rectangle through the server
                        this.socket.emit('create_rect', {
                            svg_id: this.currentSvgId,
                            x: x,
                            y: y,
                            width: width,
                            height: height,
                            fill: '#3498db',
                            stroke: '#2980b9',
                            'stroke-width': 2
                        });
                    }
                };
                
                // Add the temporary handlers
                this.draw.on('mousemove', moveHandler);
                this.draw.on('mouseup', upHandler);
            },
            
            handleCircleStart(event) {
                if (!this.currentSvgId) return;
                
                const centerX = event.clientX - this.draw.node.getBoundingClientRect().left;
                const centerY = event.clientY - this.draw.node.getBoundingClientRect().top;
                
                // Create a temporary circle
                const circle = this.draw.circle(1).center(centerX, centerY).fill('#e74c3c').stroke('#c0392b');
                
                // Setup mousemove handler
                const moveHandler = (e) => {
                    const currentX = e.clientX - this.draw.node.getBoundingClientRect().left;
                    const currentY = e.clientY - this.draw.node.getBoundingClientRect().top;
                    
                    const radius = Math.sqrt(
                        Math.pow(currentX - centerX, 2) + 
                        Math.pow(currentY - centerY, 2)
                    );
                    
                    circle.radius(radius);
                };
                
                // Setup mouseup handler
                const upHandler = () => {
                    // Remove the temporary handlers
                    this.draw.off('mousemove', moveHandler);
                    this.draw.off('mouseup', upHandler);
                    
                    // Get the final circle properties
                    const radius = parseFloat(circle.radius());
                    
                    // Remove the temporary circle
                    circle.remove();
                    
                    // Only create if it has some size
                    if (radius > 5) {
                        // Create a real circle through the server
                        this.socket.emit('create_circle', {
                            svg_id: this.currentSvgId,
                            cx: centerX,
                            cy: centerY,
                            r: radius,
                            fill: '#e74c3c',
                            stroke: '#c0392b',
                            'stroke-width': 2
                        });
                    }
                };
                
                // Add the temporary handlers
                this.draw.on('mousemove', moveHandler);
                this.draw.on('mouseup', upHandler);
            },
            
            handleTextCreate(event) {
                if (!this.currentSvgId) return;
                
                const x = event.clientX - this.draw.node.getBoundingClientRect().left;
                const y = event.clientY - this.draw.node.getBoundingClientRect().top;
                
                // Ask for text content
                const text = prompt('Enter text:', 'Hello SVG!');
                
                if (text) {
                    // Create text through the server
                    this.socket.emit('create_text', {
                        svg_id: this.currentSvgId,
                        x: x,
                        y: y,
                        text: text,
                        fill: '#000000',
                        'font-size': 16,
                        'font-family': 'Arial, sans-serif'
                    });
                }
            },
            
            handlePathStart(event) {
                if (!this.currentSvgId) return;
                
                const startX = event.clientX - this.draw.node.getBoundingClientRect().left;
                const startY = event.clientY - this.draw.node.getBoundingClientRect().top;
                
                // Start path data
                let pathData = `M${startX},${startY}`;
                
                // Create a temporary path
                const path = this.draw.path(pathData).fill('none').stroke({ color: '#2c3e50', width: 2 });
                
                // Setup mousemove handler
                const moveHandler = (e) => {
                    const currentX = e.clientX - this.draw.node.getBoundingClientRect().left;
                    const currentY = e.clientY - this.draw.node.getBoundingClientRect().top;
                    
                    // Update path data
                    pathData += ` L${currentX},${currentY}`;
                    path.plot(pathData);
                };
                
                // Setup mouseup handler
                const upHandler = () => {
                    // Remove the temporary handlers
                    this.draw.off('mousemove', moveHandler);
                    this.draw.off('mouseup', upHandler);
                    
                    // Remove the temporary path
                    path.remove();
                    
                    // Create a real path through the server
                    this.socket.emit('create_path', {
                        svg_id: this.currentSvgId,
                        d: pathData,
                        fill: 'none',
                        stroke: '#2c3e50',
                        'stroke-width': 2
                    });
                };
                
                // Add the temporary handlers
                this.draw.on('mousemove', moveHandler);
                this.draw.on('mouseup', upHandler);
            },
            
            sendPrompt() {
                if (!this.promptText.trim()) return;
                
                // Send the prompt to the server
                this.socket.emit('prompt_received', {
                    prompt: this.promptText,
                    timestamp: new Date().toISOString()
                });
                
                // Add to history locally
                this.addToPromptHistory(this.promptText);
                
                // Clear the prompt text
                this.promptText = '';
            },
            
            addToPromptHistory(text) {
                const timestamp = new Date().toLocaleTimeString();
                this.promptHistory.unshift({
                    text: text,
                    timestamp: timestamp
                });
                
                // Limit history to latest 10 items
                if (this.promptHistory.length > 10) {
                    this.promptHistory.pop();
                }
            },
            
            exportSVG() {
                if (!this.draw) return;
                
                // Get the SVG code
                const svgCode = this.draw.svg();
                
                // Create a blob and download link
                const blob = new Blob([svgCode], { type: 'image/svg+xml' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'animation.svg';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                // Notify the server about the export
                this.socket.emit('export_svg', {
                    svg_id: this.currentSvgId
                });
                
                this.showToast('SVG exported successfully');
            },
            
            copySVGCode() {
                if (!this.draw) return;
                
                // Get the SVG code
                const svgCode = this.draw.svg();
                
                // Copy to clipboard
                navigator.clipboard.writeText(svgCode)
                    .then(() => {
                        this.showToast('SVG code copied to clipboard');
                    })
                    .catch(err => {
                        console.error('Failed to copy:', err);
                        this.showToast('Failed to copy SVG code');
                    });
            },
            
            updateCodeEditor() {
                if (!this.codeEditor || !this.draw) return;
                
                // Get the SVG code and update the editor
                const svgCode = this.draw.svg();
                this.codeEditor.setValue(svgCode);
            },
            
            initCodeEditor() {
                // Initialize CodeMirror
                this.codeEditor = CodeMirror(document.getElementById('code-editor'), {
                    mode: 'xml',
                    theme: 'default',
                    lineNumbers: true,
                    readOnly: true
                });
            },
            
            loadSVGData(data) {
                if (!data || !data.elements || !data.current_svg) return;
                
                this.currentSvgId = data.current_svg;
                const svgData = data.elements[data.current_svg];
                
                if (svgData) {
                    // Initialize the SVG
                    this.initSVG(svgData.width, svgData.height);
                    
                    // Create all elements
                    for (const [id, element] of Object.entries(data.elements)) {
                        if (id !== data.current_svg && element.parent === data.current_svg) {
                            // Create element based on its type
                            const elementData = {
                                element_id: id,
                                parent_id: element.parent,
                                type: element.type,
                                properties: { ...element }
                            };
                            
                            // Remove non-property fields
                            delete elementData.properties.parent;
                            delete elementData.properties.type;
                            
                            // Add the element to the SVG
                            this.createElement(elementData);
                        }
                    }
                    
                    // Create all animations
                    for (const [id, animation] of Object.entries(data.animations)) {
                        const animationData = {
                            animation_id: id,
                            ...animation
                        };
                        this.createAnimation(animationData);
                    }
                }
            },
            
            showToast(message) {
                // Clear any existing toast timeout
                if (this.toastTimeout) {
                    clearTimeout(this.toastTimeout);
                }
                
                // Show the toast with the new message
                this.toastMessage = message;
                this.toastVisible = true;
                
                // Hide the toast after 3 seconds
                this.toastTimeout = setTimeout(() => {
                    this.toastVisible = false;
                }, 3000);
            }
        },
        mounted() {
            // Initialize Socket.IO connection
            this.initSocket();
            
            // Initialize CodeMirror editor
            this.initCodeEditor();
            
            // Event listener for keyboard shortcuts
            document.addEventListener('keydown', e => {
                // Delete key to remove selected element
                if (e.key === 'Delete' && this.selectedElement) {
                    // Implementation of element deletion
                    this.socket.emit('delete_element', {
                        element_id: this.selectedElement.id
                    });
                    
                    // Remove the element locally
                    if (this.elements[this.selectedElement.id]) {
                        this.elements[this.selectedElement.id].element.remove();
                        delete this.elements[this.selectedElement.id];
                        this.selectedElement = null;
                        
                        // Update the code editor
                        this.updateCodeEditor();
                    }
                }
            });
        }
    });
}); 