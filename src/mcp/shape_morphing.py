"""
Shape Morphing Module for SVG Animation MCP.

This module provides utilities for morphing between different SVG shapes,
enabling smooth transitions and animations.
"""

import re
import math
from browser_integration import execute_js

class PathParser:
    """
    Parser for SVG path data.
    
    Converts SVG path data strings to structured command lists for morphing.
    """
    
    def __init__(self, path_data=""):
        """
        Initialize the path parser with optional path data.
        
        Args:
            path_data: SVG path data string
        """
        self.path_data = path_data
        self.commands = []
        if path_data:
            self.parse()
    
    def parse(self, path_data=None):
        """
        Parse SVG path data into structured commands.
        
        Args:
            path_data: Optional path data to parse (uses stored path_data if None)
            
        Returns:
            List of parsed commands
        """
        if path_data is not None:
            self.path_data = path_data
        
        # Reset commands
        self.commands = []
        
        if not self.path_data:
            return self.commands
        
        # Regular expression to match SVG path commands
        command_pattern = r'([MLHVCSQTAZmlhvcsqtaz])([^MLHVCSQTAZmlhvcsqtaz]*)'
        matches = re.findall(command_pattern, self.path_data)
        
        for command_type, params in matches:
            # Parse parameters
            params = params.strip()
            # Extract numbers (including negative and decimal numbers)
            param_values = re.findall(r'[+-]?[0-9]*\.?[0-9]+', params)
            param_values = [float(val) for val in param_values]
            
            # Store command
            self.commands.append({
                'type': command_type,
                'params': param_values
            })
        
        return self.commands
    
    def to_path_data(self, commands=None):
        """
        Convert commands back to SVG path data string.
        
        Args:
            commands: List of commands (uses stored commands if None)
            
        Returns:
            SVG path data string
        """
        if commands is None:
            commands = self.commands
        
        path_data = ""
        
        for cmd in commands:
            path_data += cmd['type']
            
            # Join parameters with spaces
            params = cmd['params']
            if params:
                params_str = " ".join(str(round(p, 3)) for p in params)
                path_data += " " + params_str
        
        return path_data
    
    def normalize_commands(self, target_count=None):
        """
        Normalize commands to have consistent command types and point counts.
        
        This converts all commands to absolute coordinates and breaks down
        complex commands into simpler ones for easier morphing.
        
        Args:
            target_count: Optional target number of points
            
        Returns:
            Normalized commands
        """
        if not self.commands:
            return []
        
        normalized = []
        current_x, current_y = 0, 0
        
        for cmd in self.commands:
            cmd_type = cmd['type']
            params = cmd['params'].copy()
            
            # Convert relative commands to absolute
            if cmd_type.islower():
                cmd_type = cmd_type.upper()
                
                # Handle different command types
                if cmd_type == 'M' or cmd_type == 'L':
                    # Move or line to: pairs of coordinates
                    for i in range(0, len(params), 2):
                        params[i] += current_x
                        params[i+1] += current_y
                
                elif cmd_type == 'H':
                    # Horizontal line: single x-coordinate
                    for i in range(len(params)):
                        params[i] += current_x
                
                elif cmd_type == 'V':
                    # Vertical line: single y-coordinate
                    for i in range(len(params)):
                        params[i] += current_y
                
                elif cmd_type == 'C':
                    # Cubic bezier: three pairs of coordinates
                    for i in range(0, len(params), 6):
                        params[i] += current_x
                        params[i+1] += current_y
                        params[i+2] += current_x
                        params[i+3] += current_y
                        params[i+4] += current_x
                        params[i+5] += current_y
                
                elif cmd_type == 'S' or cmd_type == 'Q':
                    # Smooth cubic or quadratic bezier: two pairs of coordinates
                    for i in range(0, len(params), 4):
                        params[i] += current_x
                        params[i+1] += current_y
                        params[i+2] += current_x
                        params[i+3] += current_y
                
                elif cmd_type == 'T':
                    # Smooth quadratic continuation: one pair of coordinates
                    for i in range(0, len(params), 2):
                        params[i] += current_x
                        params[i+1] += current_y
                
                elif cmd_type == 'A':
                    # Arc: complex parameters, endpoints are relative
                    for i in range(0, len(params), 7):
                        params[i+5] += current_x
                        params[i+6] += current_y
            
            # Convert H and V to L commands for consistent morphing
            if cmd_type == 'H':
                for x in params:
                    normalized.append({
                        'type': 'L',
                        'params': [x, current_y]
                    })
                    current_x = x
            
            elif cmd_type == 'V':
                for y in params:
                    normalized.append({
                        'type': 'L',
                        'params': [current_x, y]
                    })
                    current_y = y
            
            # Handle other command types
            elif cmd_type == 'M':
                # Move command
                for i in range(0, len(params), 2):
                    x, y = params[i], params[i+1]
                    normalized.append({
                        'type': 'M',
                        'params': [x, y]
                    })
                    current_x, current_y = x, y
            
            elif cmd_type == 'L':
                # Line command
                for i in range(0, len(params), 2):
                    x, y = params[i], params[i+1]
                    normalized.append({
                        'type': 'L',
                        'params': [x, y]
                    })
                    current_x, current_y = x, y
            
            elif cmd_type == 'C':
                # Cubic bezier
                for i in range(0, len(params), 6):
                    x1, y1 = params[i], params[i+1]
                    x2, y2 = params[i+2], params[i+3]
                    x, y = params[i+4], params[i+5]
                    normalized.append({
                        'type': 'C',
                        'params': [x1, y1, x2, y2, x, y]
                    })
                    current_x, current_y = x, y
            
            elif cmd_type == 'Z':
                # Close path
                normalized.append({
                    'type': 'Z',
                    'params': []
                })
            
            # Add more conversions for other command types as needed
            # For simplicity, we're focusing on the most common commands
        
        # If a target count is specified, we need to add or remove points
        if target_count is not None and target_count > 0:
            # To be implemented: interpolation to achieve target point count
            pass
        
        return normalized


class ShapeMorpher:
    """
    Class for morphing between SVG shapes.
    
    Provides methods for creating smooth transitions between shapes.
    """
    
    def __init__(self, mcp):
        """
        Initialize the shape morpher.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.parser = PathParser()
    
    def create_morph_animation(self, from_element_id, to_element_id, duration=1, steps=30):
        """
        Create a morph animation between two SVG elements.
        
        Args:
            from_element_id: ID of the starting element
            to_element_id: ID of the target element
            duration: Duration of the animation in seconds
            steps: Number of intermediate steps
            
        Returns:
            ID of the created animation element
        """
        # Create a unique ID for the animation
        animation_id = f"morph_{from_element_id}_to_{to_element_id}"
        
        # Get element data using JavaScript
        js_code = f"""
        (function() {{
            var fromElement = document.getElementById('{from_element_id}');
            var toElement = document.getElementById('{to_element_id}');
            
            if (!fromElement || !toElement) {{
                return {{
                    success: false,
                    error: "Element not found"
                }};
            }}
            
            // Get element types
            var fromType = fromElement.tagName.toLowerCase();
            var toType = toElement.tagName.toLowerCase();
            
            // Extract attributes
            var fromAttrs = {{}};
            var toAttrs = {{}};
            
            // Copy attributes
            for (var i = 0; i < fromElement.attributes.length; i++) {{
                var attr = fromElement.attributes[i];
                if (attr.name !== 'id') {{
                    fromAttrs[attr.name] = attr.value;
                }}
            }}
            
            for (var i = 0; i < toElement.attributes.length; i++) {{
                var attr = toElement.attributes[i];
                if (attr.name !== 'id') {{
                    toAttrs[attr.name] = attr.value;
                }}
            }}
            
            return {{
                success: true,
                fromType: fromType,
                toType: toType,
                fromAttrs: fromAttrs,
                toAttrs: toAttrs
            }};
        }})();
        """
        
        # Execute JavaScript to get element data
        # In a real implementation, this would use the BrowserTools MCP
        # to execute the code and get the result
        
        # For now, we'll simulate a result
        element_data = {
            'success': True,
            'fromType': 'path',
            'toType': 'path',
            'fromAttrs': {
                'd': 'M10,10 L50,10 L50,50 L10,50 Z',  # Square
                'fill': 'red'
            },
            'toAttrs': {
                'd': 'M30,10 L50,30 L30,50 L10,30 Z',  # Diamond
                'fill': 'blue'
            }
        }
        
        # Check if elements were found
        if not element_data['success']:
            print(f"Error: {element_data.get('error', 'Unknown error')}")
            return None
        
        # Convert elements to paths if needed
        from_path = self._element_to_path_data(element_data['fromType'], element_data['fromAttrs'])
        to_path = self._element_to_path_data(element_data['toType'], element_data['toAttrs'])
        
        if not from_path or not to_path:
            print("Error: Could not convert elements to paths")
            return None
        
        # Parse path data
        from_commands = self.parser.parse(from_path)
        to_commands = self.parser.parse(to_path)
        
        # Normalize commands to have the same structure
        from_normalized = self.parser.normalize_commands()
        to_normalized = self.parser.normalize_commands()
        
        # Make sure both paths have the same number of commands
        self._equalize_command_counts(from_normalized, to_normalized)
        
        # Create SVG animation
        self._create_morph_animation_element(
            animation_id, 
            from_element_id, 
            from_normalized, 
            to_normalized, 
            duration,
            steps
        )
        
        return animation_id
    
    def _element_to_path_data(self, element_type, attrs):
        """
        Convert an SVG element to path data.
        
        Args:
            element_type: Type of the SVG element
            attrs: Element attributes
            
        Returns:
            Path data string or None if conversion failed
        """
        if element_type == 'path':
            return attrs.get('d', '')
        
        elif element_type == 'rect':
            # Convert rectangle to path
            x = float(attrs.get('x', 0))
            y = float(attrs.get('y', 0))
            width = float(attrs.get('width', 0))
            height = float(attrs.get('height', 0))
            rx = float(attrs.get('rx', 0))
            ry = float(attrs.get('ry', rx))
            
            if rx == 0 and ry == 0:
                # Simple rectangle
                return f"M{x},{y} h{width} v{height} h{-width} Z"
            else:
                # Rectangle with rounded corners
                return (
                    f"M{x+rx},{y} "
                    f"h{width-2*rx} "
                    f"a{rx},{ry} 0 0 1 {rx},{ry} "
                    f"v{height-2*ry} "
                    f"a{rx},{ry} 0 0 1 {-rx},{ry} "
                    f"h{-width+2*rx} "
                    f"a{rx},{ry} 0 0 1 {-rx},{-ry} "
                    f"v{-height+2*ry} "
                    f"a{rx},{ry} 0 0 1 {rx},{-ry} "
                    f"Z"
                )
        
        elif element_type == 'circle':
            # Convert circle to path
            cx = float(attrs.get('cx', 0))
            cy = float(attrs.get('cy', 0))
            r = float(attrs.get('r', 0))
            
            # Approximate circle with 4 bezier curves
            return (
                f"M{cx},{cy-r} "
                f"C{cx+r*0.55},{cy-r} {cx+r},{cy-r*0.55} {cx+r},{cy} "
                f"C{cx+r},{cy+r*0.55} {cx+r*0.55},{cy+r} {cx},{cy+r} "
                f"C{cx-r*0.55},{cy+r} {cx-r},{cy+r*0.55} {cx-r},{cy} "
                f"C{cx-r},{cy-r*0.55} {cx-r*0.55},{cy-r} {cx},{cy-r} "
                f"Z"
            )
        
        elif element_type == 'ellipse':
            # Convert ellipse to path
            cx = float(attrs.get('cx', 0))
            cy = float(attrs.get('cy', 0))
            rx = float(attrs.get('rx', 0))
            ry = float(attrs.get('ry', 0))
            
            # Approximate ellipse with 4 bezier curves
            return (
                f"M{cx},{cy-ry} "
                f"C{cx+rx*0.55},{cy-ry} {cx+rx},{cy-ry*0.55} {cx+rx},{cy} "
                f"C{cx+rx},{cy+ry*0.55} {cx+rx*0.55},{cy+ry} {cx},{cy+ry} "
                f"C{cx-rx*0.55},{cy+ry} {cx-rx},{cy+ry*0.55} {cx-rx},{cy} "
                f"C{cx-rx},{cy-ry*0.55} {cx-rx*0.55},{cy-ry} {cx},{cy-ry} "
                f"Z"
            )
        
        elif element_type == 'line':
            # Convert line to path
            x1 = float(attrs.get('x1', 0))
            y1 = float(attrs.get('y1', 0))
            x2 = float(attrs.get('x2', 0))
            y2 = float(attrs.get('y2', 0))
            
            return f"M{x1},{y1} L{x2},{y2}"
        
        elif element_type == 'polygon' or element_type == 'polyline':
            # Convert polygon/polyline to path
            points = attrs.get('points', '')
            if not points:
                return None
            
            # Parse points
            point_pairs = re.findall(r'([+-]?[0-9]*\.?[0-9]+)[,\s]([+-]?[0-9]*\.?[0-9]+)', points)
            if not point_pairs:
                return None
            
            # Create path data
            path_data = f"M{point_pairs[0][0]},{point_pairs[0][1]}"
            for x, y in point_pairs[1:]:
                path_data += f" L{x},{y}"
            
            if element_type == 'polygon':
                path_data += " Z"
            
            return path_data
        
        return None
    
    def _equalize_command_counts(self, from_commands, to_commands):
        """
        Make sure both command lists have the same number of commands.
        
        This adds interpolated commands if necessary.
        
        Args:
            from_commands: First list of commands
            to_commands: Second list of commands
        """
        if len(from_commands) == len(to_commands):
            return
        
        # For simplicity, we'll just duplicate the last command in the shorter list
        # In a real implementation, you'd want to interpolate points more intelligently
        if len(from_commands) < len(to_commands):
            last_cmd = from_commands[-1].copy() if from_commands else {'type': 'L', 'params': [0, 0]}
            while len(from_commands) < len(to_commands):
                from_commands.append(last_cmd.copy())
        else:
            last_cmd = to_commands[-1].copy() if to_commands else {'type': 'L', 'params': [0, 0]}
            while len(to_commands) < len(from_commands):
                to_commands.append(last_cmd.copy())
    
    def _create_morph_animation_element(self, animation_id, target_element_id, from_commands, to_commands, duration, steps):
        """
        Create an SVG animation element for the morph.
        
        Args:
            animation_id: ID for the animation element
            target_element_id: ID of the target element
            from_commands: Starting commands
            to_commands: Ending commands
            duration: Animation duration in seconds
            steps: Number of animation steps
        """
        # Generate intermediate paths
        paths = []
        
        for step in range(steps + 1):
            t = step / steps  # Interpolation factor (0 to 1)
            
            # Interpolate between commands
            interpolated = []
            
            for i in range(min(len(from_commands), len(to_commands))):
                from_cmd = from_commands[i]
                to_cmd = to_commands[i]
                
                # Use the command type from the target (end) command
                cmd_type = to_cmd['type']
                
                # Interpolate parameters
                params = []
                for j in range(min(len(from_cmd['params']), len(to_cmd['params']))):
                    from_param = from_cmd['params'][j]
                    to_param = to_cmd['params'][j]
                    
                    # Linear interpolation
                    interpolated_param = from_param + (to_param - from_param) * t
                    params.append(interpolated_param)
                
                interpolated.append({
                    'type': cmd_type,
                    'params': params
                })
            
            # Convert to path data
            path_data = self.parser.to_path_data(interpolated)
            paths.append(path_data)
        
        # Create a JavaScript animation using requestAnimationFrame
        js_code = f"""
        (function() {{
            var element = document.getElementById('{target_element_id}');
            if (!element) return;
            
            var paths = {paths};
            var duration = {duration * 1000}; // Convert to milliseconds
            var startTime = null;
            var animationId = '{animation_id}';
            
            // Store the original path if needed later
            element.setAttribute('data-original-path', element.getAttribute('d'));
            
            function animate(timestamp) {{
                if (!startTime) startTime = timestamp;
                var elapsed = timestamp - startTime;
                
                if (elapsed >= duration) {{
                    // Animation complete, set final path
                    element.setAttribute('d', paths[paths.length - 1]);
                    
                    // Store animation status
                    element.setAttribute('data-morphing', 'false');
                    return;
                }}
                
                // Calculate progress (0 to 1)
                var progress = elapsed / duration;
                
                // Find the appropriate path based on progress
                var index = Math.min(Math.floor(progress * paths.length), paths.length - 1);
                element.setAttribute('d', paths[index]);
                
                // Continue animation
                requestAnimationFrame(animate);
            }}
            
            // Mark element as morphing
            element.setAttribute('data-morphing', 'true');
            
            // Start animation
            var animFrameId = requestAnimationFrame(animate);
            
            // Store animation frame ID for potential cancellation
            window[animationId] = animFrameId;
        }})();
        """
        
        # Execute the JavaScript code
        execute_js(js_code)
    
    def stop_morph_animation(self, animation_id, target_element_id, reset=False):
        """
        Stop a morph animation.
        
        Args:
            animation_id: ID of the animation
            target_element_id: ID of the target element
            reset: If True, reset to original path
        """
        js_code = f"""
        (function() {{
            // Cancel animation frame
            if (window['{animation_id}']) {{
                cancelAnimationFrame(window['{animation_id}']);
                window['{animation_id}'] = null;
            }}
            
            var element = document.getElementById('{target_element_id}');
            if (!element) return;
            
            // Reset to original path if requested
            if ({str(reset).lower()}) {{
                var originalPath = element.getAttribute('data-original-path');
                if (originalPath) {{
                    element.setAttribute('d', originalPath);
                }}
            }}
            
            // Update status
            element.setAttribute('data-morphing', 'false');
        }})();
        """
        
        execute_js(js_code)
    
    def morph_between_shapes(self, shape1, shape2, morph_element_id=None, duration=1):
        """
        Create a morphing animation between two SVG shapes.
        
        Args:
            shape1: First SVG Shape object
            shape2: Second SVG Shape object
            morph_element_id: ID for the morphing element (created if None)
            duration: Animation duration in seconds
            
        Returns:
            ID of the morphing element
        """
        # If no morph element is provided, create one
        if morph_element_id is None:
            morph_element_id = f"morph_{shape1.id}_to_{shape2.id}"
            
            # Create a new path element for the morph
            js_code = f"""
            (function() {{
                var svg = document.getElementById('{shape1.id}').closest('svg');
                if (!svg) return null;
                
                var morphElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                morphElement.setAttribute('id', '{morph_element_id}');
                
                // Copy attributes from first shape
                var sourceElement = document.getElementById('{shape1.id}');
                for (var i = 0; i < sourceElement.attributes.length; i++) {{
                    var attr = sourceElement.attributes[i];
                    if (attr.name !== 'id' && attr.name !== 'd' && attr.name !== 'points') {{
                        morphElement.setAttribute(attr.name, attr.value);
                    }}
                }}
                
                svg.appendChild(morphElement);
                return morphElement.id;
            }})();
            """
            
            execute_js(js_code)
        
        # Create the morph animation
        animation_id = self.create_morph_animation(shape1.id, shape2.id, duration, steps=30)
        
        # Return the morph element ID
        return morph_element_id


def shape_to_path(shape):
    """
    Convert an SVG shape to a path.
    
    Args:
        shape: SVG Shape object
        
    Returns:
        Path data string
    """
    # Execute JavaScript to get the element type and attributes
    js_code = f"""
    (function() {{
        var element = document.getElementById('{shape.id}');
        if (!element) return null;
        
        var type = element.tagName.toLowerCase();
        var attrs = {{}};
        
        for (var i = 0; i < element.attributes.length; i++) {{
            var attr = element.attributes[i];
            attrs[attr.name] = attr.value;
        }}
        
        return {{type: type, attrs: attrs}};
    }})();
    """
    
    # In a real implementation, this would be executed via BrowserTools MCP
    # For now, we'll simulate a result based on the shape type
    result = {'type': 'unknown', 'attrs': {}}
    
    # Convert to path data based on the result
    morpher = ShapeMorpher(None)  # No MCP instance needed for this function
    path_data = morpher._element_to_path_data(result['type'], result['attrs'])
    
    return path_data


def morph_element(from_element_id, to_element_id, duration=1, mcp=None):
    """
    Create a morph animation between two SVG elements.
    
    Args:
        from_element_id: ID of the starting element
        to_element_id: ID of the target element
        duration: Duration of the animation in seconds
        mcp: Optional MCP instance
        
    Returns:
        ID of the animation
    """
    morpher = ShapeMorpher(mcp)
    return morpher.create_morph_animation(from_element_id, to_element_id, duration) 