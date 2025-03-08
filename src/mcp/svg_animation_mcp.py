"""
SVG Animation MCP - A Machine Communication Protocol for SVG animations.

This module provides a Python API for creating and animating SVG elements
in a web browser, designed to be easily used by Large Language Models (LLMs).
It integrates with BrowserTools MCP for JavaScript execution.
"""

from browser_integration import execute_js, BrowserIntegrationError
from utils import validate_color, validate_number, escape_js_string, validate_animation_duration

class MCPError(Exception):
    """Custom exception class for SVG Animation MCP errors."""
    pass

class MCP:
    """
    Main MCP class for SVG animation.
    
    Manages unique element IDs and provides methods to create SVG elements.
    """
    
    def __init__(self):
        """Initialize the MCP with an ID counter and element map."""
        self.element_id_counter = 0
        self.element_map = {}
    
    def _generate_id(self, prefix="element"):
        """Generate a unique ID for an element."""
        element_id = f"{prefix}_{self.element_id_counter}"
        self.element_id_counter += 1
        return element_id
    
    def create_svg(self, width=500, height=500, parent_selector="body"):
        """
        Create an SVG element in the browser.
        
        Args:
            width: Width of the SVG in pixels
            height: Height of the SVG in pixels
            parent_selector: CSS selector for the parent element
            
        Returns:
            SVG object for further manipulation
            
        Raises:
            MCPError: If the SVG element cannot be created
        """
        try:
            svg_id = self._generate_id("svg")
            js_code = f"""
            var {svg_id} = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            {svg_id}.setAttribute('id', '{svg_id}');
            {svg_id}.setAttribute('width', '{width}');
            {svg_id}.setAttribute('height', '{height}');
            {svg_id}.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            document.querySelector('{parent_selector}').appendChild({svg_id});
            """
            execute_js(js_code)
            
            svg_obj = SVG(self, svg_id)
            self.element_map[svg_id] = svg_obj
            return svg_obj
        except Exception as e:
            raise MCPError(f"Failed to create SVG element: {str(e)}")
    
    def execute_js(self, code):
        """
        Execute arbitrary JavaScript code in the browser.
        
        Args:
            code: JavaScript code to execute
            
        Raises:
            MCPError: If JavaScript execution fails
        """
        try:
            execute_js(code)
        except Exception as e:
            raise MCPError(f"JavaScript execution failed: {str(e)}")


class SVG:
    """
    SVG class for managing an SVG element.
    
    Provides methods to add shapes and other SVG elements.
    """
    
    def __init__(self, mcp, id):
        """
        Initialize an SVG object.
        
        Args:
            mcp: Parent MCP instance
            id: Unique ID of the SVG element
        """
        self.mcp = mcp
        self.id = id
    
    def add_rectangle(self, x=0, y=0, width=100, height=100, **kwargs):
        """
        Add a rectangle to the SVG.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            width: Width of the rectangle
            height: Height of the rectangle
            **kwargs: Additional attributes (fill, stroke, etc.)
            
        Returns:
            Rectangle object for further manipulation
        """
        rect_id = self.mcp._generate_id("rect")
        
        js_code = f"""
        var {rect_id} = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        {rect_id}.setAttribute('id', '{rect_id}');
        {rect_id}.setAttribute('x', '{x}');
        {rect_id}.setAttribute('y', '{y}');
        {rect_id}.setAttribute('width', '{width}');
        {rect_id}.setAttribute('height', '{height}');
        """
        
        for attr, value in kwargs.items():
            js_code += f"{rect_id}.setAttribute('{attr}', '{value}');"
        
        js_code += f"document.getElementById('{self.id}').appendChild({rect_id});"
        execute_js(js_code)
        
        rect_obj = Rectangle(self.mcp, rect_id)
        self.mcp.element_map[rect_id] = rect_obj
        return rect_obj
    
    def add_circle(self, cx=0, cy=0, r=50, **kwargs):
        """
        Add a circle to the SVG.
        
        Args:
            cx: X-coordinate of the center
            cy: Y-coordinate of the center
            r: Radius
            **kwargs: Additional attributes (fill, stroke, etc.)
            
        Returns:
            Circle object for further manipulation
        """
        circle_id = self.mcp._generate_id("circle")
        
        js_code = f"""
        var {circle_id} = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        {circle_id}.setAttribute('id', '{circle_id}');
        {circle_id}.setAttribute('cx', '{cx}');
        {circle_id}.setAttribute('cy', '{cy}');
        {circle_id}.setAttribute('r', '{r}');
        """
        
        for attr, value in kwargs.items():
            js_code += f"{circle_id}.setAttribute('{attr}', '{value}');"
        
        js_code += f"document.getElementById('{self.id}').appendChild({circle_id});"
        execute_js(js_code)
        
        circle_obj = Circle(self.mcp, circle_id)
        self.mcp.element_map[circle_id] = circle_obj
        return circle_obj
    
    def add_path(self, d, **kwargs):
        """
        Add a path to the SVG.
        
        Args:
            d: Path data string
            **kwargs: Additional attributes (fill, stroke, etc.)
            
        Returns:
            Path object for further manipulation
        """
        path_id = self.mcp._generate_id("path")
        
        js_code = f"""
        var {path_id} = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        {path_id}.setAttribute('id', '{path_id}');
        {path_id}.setAttribute('d', '{d}');
        """
        
        for attr, value in kwargs.items():
            js_code += f"{path_id}.setAttribute('{attr}', '{value}');"
        
        js_code += f"document.getElementById('{self.id}').appendChild({path_id});"
        execute_js(js_code)
        
        path_obj = Path(self.mcp, path_id)
        self.mcp.element_map[path_id] = path_obj
        return path_obj

    def add_text(self, x=0, y=0, text="", **kwargs):
        """
        Add text to the SVG.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            text: Text content
            **kwargs: Additional attributes (font-size, fill, etc.)
            
        Returns:
            Text object for further manipulation
        """
        text_id = self.mcp._generate_id("text")
        
        js_code = f"""
        var {text_id} = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        {text_id}.setAttribute('id', '{text_id}');
        {text_id}.setAttribute('x', '{x}');
        {text_id}.setAttribute('y', '{y}');
        {text_id}.textContent = '{text}';
        """
        
        for attr, value in kwargs.items():
            js_code += f"{text_id}.setAttribute('{attr}', '{value}');"
        
        js_code += f"document.getElementById('{self.id}').appendChild({text_id});"
        execute_js(js_code)
        
        text_obj = Text(self.mcp, text_id)
        self.mcp.element_map[text_id] = text_obj
        return text_obj


class Shape:
    """
    Base class for SVG shapes.
    
    Provides methods for animation and attribute manipulation.
    """
    
    def __init__(self, mcp, id):
        """
        Initialize a Shape object.
        
        Args:
            mcp: Parent MCP instance
            id: Unique ID of the shape element
        """
        self.mcp = mcp
        self.id = id
    
    def set_attribute(self, attribute, value):
        """
        Set an attribute of the shape.
        
        Args:
            attribute: Name of the attribute
            value: Value of the attribute
            
        Raises:
            MCPError: If the attribute cannot be set
        """
        try:
            # Special handling for certain attributes
            if attribute.lower() in ('fill', 'stroke'):
                value = validate_color(value)
            
            # Format value for JavaScript
            if isinstance(value, str):
                js_value = f"'{escape_js_string(value)}'"
            elif isinstance(value, (int, float)):
                js_value = str(value)
            elif isinstance(value, bool):
                js_value = 'true' if value else 'false'
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
            
            js_code = f"""
            (function() {{
                var element = document.getElementById('{self.id}');
                if (element) {{
                    element.setAttribute('{attribute}', {js_value});
                    return true;
                }}
                return false;
            }})();
            """
            result = execute_js(js_code)
            
            if result is False:
                raise MCPError(f"Element with ID '{self.id}' not found")
                
        except (ValueError, BrowserIntegrationError) as e:
            raise MCPError(f"Failed to set attribute '{attribute}': {str(e)}")
    
    def animate(self, attribute, from_value, to_value, duration=1, repeat_count="indefinite", **kwargs):
        """
        Animate an attribute of the shape.
        
        Args:
            attribute: Name of the attribute
            from_value: Starting value
            to_value: Ending value
            duration: Duration in seconds
            repeat_count: Number of repetitions or "indefinite"
            **kwargs: Additional animation attributes
            
        Returns:
            Animation ID for reference
            
        Raises:
            MCPError: If the animation cannot be created
        """
        try:
            # Validate duration
            duration = validate_animation_duration(duration)
            
            # Special handling for color attributes
            if attribute.lower() in ('fill', 'stroke'):
                from_value = validate_color(from_value)
                to_value = validate_color(to_value)
            
            # Generate unique animation ID
            animation_id = self.mcp._generate_id(f"anim_{attribute}")
            
            # Format values for JavaScript
            if isinstance(from_value, str):
                from_js = f"'{escape_js_string(from_value)}'"
            else:
                from_js = str(from_value)
                
            if isinstance(to_value, str):
                to_js = f"'{escape_js_string(to_value)}'"
            else:
                to_js = str(to_value)
            
            # Build animation element
            js_code = f"""
            (function() {{
                var element = document.getElementById('{self.id}');
                if (!element) return false;
                
                var animation = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
                animation.setAttribute('id', '{animation_id}');
                animation.setAttribute('attributeName', '{attribute}');
                animation.setAttribute('from', {from_js});
                animation.setAttribute('to', {to_js});
                animation.setAttribute('dur', '{duration}s');
                animation.setAttribute('repeatCount', '{repeat_count}');
            """
            
            # Add additional attributes
            for attr, value in kwargs.items():
                if isinstance(value, str):
                    js_code += f"animation.setAttribute('{attr}', '{escape_js_string(value)}');\n"
                else:
                    js_code += f"animation.setAttribute('{attr}', {value});\n"
            
            js_code += """
                element.appendChild(animation);
                return animation.id;
            }})();
            """
            
            result = execute_js(js_code)
            
            if not result:
                raise MCPError(f"Failed to create animation for element with ID '{self.id}'")
                
            return result
            
        except (ValueError, BrowserIntegrationError) as e:
            raise MCPError(f"Failed to animate attribute '{attribute}': {str(e)}")
    
    def animate_transform(self, transform_type, from_value, to_value, duration=1, repeat_count="indefinite", **kwargs):
        """
        Animate a transformation of the shape.
        
        Args:
            transform_type: Type of transformation (translate, rotate, scale, etc.)
            from_value: Starting value
            to_value: Ending value
            duration: Duration in seconds
            repeat_count: Number of repetitions or "indefinite"
            **kwargs: Additional animation attributes
            
        Returns:
            Animation ID for reference
            
        Raises:
            MCPError: If the animation cannot be created
        """
        try:
            # Validate duration
            duration = validate_animation_duration(duration)
            
            # Validate transform type
            valid_transforms = ['translate', 'scale', 'rotate', 'skewX', 'skewY']
            if transform_type not in valid_transforms:
                raise ValueError(f"Invalid transform type: {transform_type}. Must be one of {valid_transforms}")
            
            # Generate unique animation ID
            animation_id = self.mcp._generate_id(f"anim_{transform_type}")
            
            # Format values for JavaScript
            if isinstance(from_value, tuple):
                from_js = f"'{from_value[0]} {from_value[1]}'"
            elif isinstance(from_value, str):
                from_js = f"'{escape_js_string(from_value)}'"
            else:
                from_js = f"'{from_value}'"
                
            if isinstance(to_value, tuple):
                to_js = f"'{to_value[0]} {to_value[1]}'"
            elif isinstance(to_value, str):
                to_js = f"'{escape_js_string(to_value)}'"
            else:
                to_js = f"'{to_value}'"
            
            # Build animation element
            js_code = f"""
            (function() {{
                var element = document.getElementById('{self.id}');
                if (!element) return false;
                
                var animation = document.createElementNS('http://www.w3.org/2000/svg', 'animateTransform');
                animation.setAttribute('id', '{animation_id}');
                animation.setAttribute('attributeName', 'transform');
                animation.setAttribute('type', '{transform_type}');
                animation.setAttribute('from', {from_js});
                animation.setAttribute('to', {to_js});
                animation.setAttribute('dur', '{duration}s');
                animation.setAttribute('repeatCount', '{repeat_count}');
            """
            
            # Add additional attributes
            for attr, value in kwargs.items():
                if isinstance(value, str):
                    js_code += f"animation.setAttribute('{attr}', '{escape_js_string(value)}');\n"
                else:
                    js_code += f"animation.setAttribute('{attr}', {value});\n"
            
            js_code += """
                element.appendChild(animation);
                return animation.id;
            }})();
            """
            
            result = execute_js(js_code)
            
            if not result:
                raise MCPError(f"Failed to create transform animation for element with ID '{self.id}'")
                
            return result
            
        except (ValueError, BrowserIntegrationError) as e:
            raise MCPError(f"Failed to animate transform '{transform_type}': {str(e)}")
    
    def remove_animation(self, animation_id=None):
        """
        Remove an animation from the shape.
        
        Args:
            animation_id: ID of the animation to remove, or None to remove all animations
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            MCPError: If the animation cannot be removed
        """
        try:
            if animation_id:
                js_code = f"""
                (function() {{
                    var animation = document.getElementById('{animation_id}');
                    if (animation && animation.parentNode) {{
                        animation.parentNode.removeChild(animation);
                        return true;
                    }}
                    return false;
                }})();
                """
            else:
                js_code = f"""
                (function() {{
                    var element = document.getElementById('{self.id}');
                    if (!element) return false;
                    
                    var animations = element.getElementsByTagName('animate');
                    while (animations.length > 0) {{
                        animations[0].parentNode.removeChild(animations[0]);
                    }}
                    
                    var transformAnimations = element.getElementsByTagName('animateTransform');
                    while (transformAnimations.length > 0) {{
                        transformAnimations[0].parentNode.removeChild(transformAnimations[0]);
                    }}
                    
                    return true;
                }})();
                """
            
            result = execute_js(js_code)
            
            if result is False:
                if animation_id:
                    raise MCPError(f"Animation with ID '{animation_id}' not found")
                else:
                    raise MCPError(f"Element with ID '{self.id}' not found")
                    
            return True
            
        except BrowserIntegrationError as e:
            raise MCPError(f"Failed to remove animation: {str(e)}")


class Rectangle(Shape):
    """Rectangle shape for SVG."""
    pass


class Circle(Shape):
    """Circle shape for SVG."""
    pass


class Path(Shape):
    """Path shape for SVG."""
    pass


class Text(Shape):
    """Text element for SVG."""
    def set_text(self, text):
        """
        Set the text content.
        
        Args:
            text: New text content
        """
        js_code = f"document.getElementById('{self.id}').textContent = '{text}';"
        execute_js(js_code) 