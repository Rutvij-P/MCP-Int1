"""
AI-Powered Animation Suggestions for SVG Animation MCP.

This module provides utilities for generating SVG animations
from natural language descriptions using Large Language Models.
"""

import json
import re
from svg_animation_mcp import MCP, MCPError

class BaseAnimationSuggester:
    """
    Base class for animation suggestion functionality.
    
    Provides common methods for parsing descriptions and generating animations
    that can be extended by more specialized suggesters.
    """
    
    def __init__(self, mcp=None):
        """
        Initialize the base animation suggester.
        
        Args:
            mcp: Optional MCP instance to use (will create one if not provided)
        """
        self.mcp = mcp if mcp is not None else MCP()
    
    def _extract_shape_type(self, description):
        """
        Extract shape type from description.
        
        Args:
            description: Natural language description
            
        Returns:
            Extracted shape type or default
        """
        shapes_match = re.search(r'(a|an) (\w+) (that|which)', description, re.IGNORECASE)
        shape_type = shapes_match.group(2) if shapes_match else "rectangle"
        
        # Map common words to shape types
        shape_map = {
            "circle": "circle",
            "square": "rectangle",
            "rectangle": "rectangle",
            "box": "rectangle",
            "text": "text",
            "star": "path",  # will need special handling
            "line": "path"   # will need special handling
        }
        
        return shape_map.get(shape_type.lower(), "rectangle")
    
    def _extract_color(self, description):
        """
        Extract color from description.
        
        Args:
            description: Natural language description
            
        Returns:
            Extracted color or default
        """
        color_match = re.search(r'(\w+) colou?r', description, re.IGNORECASE)
        return color_match.group(1) if color_match else "blue"
    
    def _extract_animation_type(self, description):
        """
        Extract animation type from description.
        
        Args:
            description: Natural language description
            
        Returns:
            Extracted animation type or default
        """
        animation_patterns = {
            r'mov(e|ing)': "move",
            r'spin(ning)?|rotat(e|ing)': "spin",
            r'puls(e|ing)': "pulse",
            r'grow(ing)?': "pulse",
            r'bounc(e|ing)': "bounce",
            r'fad(e|ing)': "fade"
        }
        
        animation_type = "move"  # default
        for pattern, anim_type in animation_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                animation_type = anim_type
                break
                
        return animation_type
    
    def suggest_animation(self, description):
        """
        Suggest an animation based on a natural language description.
        
        Args:
            description: Natural language description of the desired animation
            
        Returns:
            Dictionary with code and explanation
        """
        try:
            code = self.parse_description(description)
            
            return {
                "code": code,
                "explanation": f"Generated animation code for: {description}"
            }
        except Exception as e:
            return {
                "error": str(e),
                "explanation": "Failed to generate animation code"
            }
    
    def execute_suggestion(self, description):
        """
        Generate and execute animation code from a description.
        
        Args:
            description: Natural language description of the desired animation
            
        Returns:
            True if successful, False otherwise
        """
        suggestion = self.suggest_animation(description)
        
        if "error" in suggestion:
            print(f"Error: {suggestion['error']}")
            return False
        
        try:
            # Create a clean namespace for execution
            exec_globals = {}
            exec(suggestion["code"], exec_globals)
            return True
        except Exception as e:
            print(f"Error executing animation code: {str(e)}")
            return False
    
    def parse_description(self, description):
        """
        Parse a natural language description and generate SVG animation code.
        
        This method should be implemented by subclasses.
        
        Args:
            description: Natural language description of the desired animation
            
        Returns:
            Executable Python code string
        """
        raise NotImplementedError("Subclasses must implement parse_description method")


class AnimationSuggester(BaseAnimationSuggester):
    """
    Class for suggesting animations based on natural language descriptions.
    
    Uses a templating approach to convert descriptions into executable Python code
    that creates SVG animations.
    """
    
    def __init__(self, mcp=None):
        """
        Initialize the AnimationSuggester.
        
        Args:
            mcp: Optional MCP instance to use (will create one if not provided)
        """
        super().__init__(mcp)
        self.animation_patterns = self._load_animation_patterns()
    
    def _load_animation_patterns(self):
        """Load predefined animation patterns."""
        return {
            "bounce": {
                "description": "Element bounces up and down repeatedly",
                "params": ["element", "height", "duration"],
                "code_template": "{element}.animate('y', from_value={element.y}, to_value={element.y + height}, "
                                 "duration={duration}, repeat_count='indefinite', "
                                 "values='{element.y};{element.y + height};{element.y}', key_times='0;0.5;1')"
            },
            "pulse": {
                "description": "Element grows and shrinks repeatedly",
                "params": ["element", "scale_factor", "duration"],
                "code_template": "{element}.animate_transform('scale', from_value=1, to_value={scale_factor}, "
                                "duration={duration}, repeat_count='indefinite')"
            },
            "spin": {
                "description": "Element rotates around its center",
                "params": ["element", "degrees", "duration"],
                "code_template": "{element}.animate_transform('rotate', "
                                "from_value='0 {element.cx} {element.cy}', "
                                "to_value='{degrees} {element.cx} {element.cy}', "
                                "duration={duration}, repeat_count='indefinite')"
            },
            "fade": {
                "description": "Element fades in or out",
                "params": ["element", "from_opacity", "to_opacity", "duration"],
                "code_template": "{element}.animate('opacity', from_value={from_opacity}, "
                                "to_value={to_opacity}, duration={duration})"
            },
            "move": {
                "description": "Element moves from one position to another",
                "params": ["element", "to_x", "to_y", "duration"],
                "code_template": "{element}.animate_transform('translate', from_value=(0, 0), "
                                "to_value=({to_x}, {to_y}), duration={duration})"
            }
        }
    
    def parse_description(self, description):
        """
        Parse a natural language description and generate SVG animation code.
        
        Args:
            description: Natural language description of the desired animation
            
        Returns:
            Executable Python code string
        """
        # Extract key information from description using base class methods
        shape_type = self._extract_shape_type(description)
        color = self._extract_color(description)
        animation_type = self._extract_animation_type(description)
        
        # Generate code based on extracted information
        code = f"# Animation generated from description: {description}\n"
        code += "from svg_animation_mcp import MCP\n"
        code += "from browser_integration import init_browser_environment\n"
        code += "from utils import generate_star_points, generate_path_data\n\n"
        code += "# Initialize browser environment\n"
        code += "init_browser_environment()\n\n"
        code += "# Create MCP instance\n"
        code += "mcp = MCP()\n\n"
        code += "# Create SVG canvas\n"
        code += "svg = mcp.create_svg(width=600, height=400, parent_selector=\"#animation-container\")\n\n"
        
        # Create shape based on type
        if shape_type == "circle":
            code += f"# Create a {color} circle\n"
            code += f"circle = svg.add_circle(cx=300, cy=200, r=50, fill=\"{color}\")\n\n"
            element_var = "circle"
        elif shape_type == "rectangle":
            code += f"# Create a {color} rectangle\n"
            code += f"rect = svg.add_rectangle(x=200, y=150, width=100, height=80, fill=\"{color}\")\n\n"
            element_var = "rect"
        elif shape_type == "text":
            text_match = re.search(r'text saying "([^"]+)"', description, re.IGNORECASE)
            text = text_match.group(1) if text_match else "Hello World"
            code += f"# Create {color} text\n"
            code += f"text = svg.add_text(x=300, y=200, text=\"{text}\", fill=\"{color}\", font_size=\"24px\", text_anchor=\"middle\")\n\n"
            element_var = "text"
        elif shape_type == "path" and "star" in description.lower():
            code += f"# Create a {color} star\n"
            code += "# Generate star points\n"
            code += "star_points = generate_star_points(cx=300, cy=200, outer_radius=100, inner_radius=50, points=5)\n"
            code += "star_path_data = generate_path_data(star_points) + \" Z\"  # Z closes the path\n\n"
            code += f"star = svg.add_path(d=star_path_data, fill=\"{color}\")\n\n"
            element_var = "star"
        
        # Apply animation based on type
        if animation_type == "move":
            match = re.search(r'(left|right|up|down)', description, re.IGNORECASE)
            direction = match.group(1).lower() if match else "right"
            
            direction_map = {
                "left": "(-200, 0)",
                "right": "(200, 0)",
                "up": "(0, -200)",
                "down": "(0, 200)"
            }
            
            to_value = direction_map.get(direction, "(200, 0)")
            code += f"# Make the {shape_type} move {direction}\n"
            code += f"{element_var}.animate_transform(\"translate\", from_value=(0, 0), to_value={to_value}, duration=2, repeat_count=\"indefinite\")\n"
        
        elif animation_type == "spin":
            code += f"# Make the {shape_type} spin\n"
            if shape_type == "circle":
                code += f"{element_var}.animate_transform(\"rotate\", from_value=\"0 300 200\", to_value=\"360 300 200\", duration=3, repeat_count=\"indefinite\")\n"
            elif shape_type == "rectangle":
                code += f"{element_var}.animate_transform(\"rotate\", from_value=\"0 250 190\", to_value=\"360 250 190\", duration=3, repeat_count=\"indefinite\")\n"
            elif shape_type == "path":
                code += f"{element_var}.animate_transform(\"rotate\", from_value=\"0 300 200\", to_value=\"360 300 200\", duration=3, repeat_count=\"indefinite\")\n"
            else:
                code += f"{element_var}.animate_transform(\"rotate\", from_value=\"0 300 200\", to_value=\"360 300 200\", duration=3, repeat_count=\"indefinite\")\n"
        
        elif animation_type == "pulse":
            code += f"# Make the {shape_type} pulse\n"
            if shape_type == "circle":
                code += f"{element_var}.animate(\"r\", from_value=50, to_value=80, duration=1, repeat_count=\"indefinite\")\n"
            else:
                code += f"{element_var}.animate_transform(\"scale\", from_value=\"1 1\", to_value=\"1.5 1.5\", duration=1, repeat_count=\"indefinite\")\n"
        
        elif animation_type == "bounce":
            code += f"# Make the {shape_type} bounce\n"
            if shape_type == "circle":
                code += f"{element_var}.animate(\"cy\", from_value=200, to_value=350, duration=1, repeat_count=\"indefinite\", values=\"200;350;200\", key_times=\"0;0.5;1\")\n"
            elif shape_type == "rectangle":
                code += f"{element_var}.animate(\"y\", from_value=150, to_value=300, duration=1, repeat_count=\"indefinite\", values=\"150;300;150\", key_times=\"0;0.5;1\")\n"
            else:
                code += f"{element_var}.animate_transform(\"translate\", from_value=\"0 0\", to_value=\"0 150\", duration=1, repeat_count=\"indefinite\", values=\"0 0;0 150;0 0\", key_times=\"0;0.5;1\")\n"
        
        elif animation_type == "fade":
            fade_type = "in" if "in" in description.lower() else "out"
            if fade_type == "in":
                code += f"# Make the {shape_type} fade in\n"
                code += f"{element_var}.set_attribute(\"opacity\", \"0\")\n"
                code += f"{element_var}.animate(\"opacity\", from_value=0, to_value=1, duration=2)\n"
            else:
                code += f"# Make the {shape_type} fade out\n"
                code += f"{element_var}.animate(\"opacity\", from_value=1, to_value=0, duration=2)\n"
        
        return code


def generate_animation_from_text(description):
    """
    Generate and execute an animation from a text description.
    
    Args:
        description: Natural language description of the desired animation
        
    Returns:
        Dictionary with results of animation generation
    """
    suggester = AnimationSuggester()
    success = suggester.execute_suggestion(description)
    
    if success:
        return {
            "status": "success",
            "message": f"Successfully generated animation for: {description}"
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to generate animation for: {description}"
        } 