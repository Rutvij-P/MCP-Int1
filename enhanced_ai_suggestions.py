"""
Enhanced AI Suggestions Module for SVG Animation MCP.

This module provides advanced natural language processing capabilities
for generating sophisticated SVG animations from text descriptions,
with Vercel-level quality and precision.
"""

import re
import json
from svg_animation_mcp import MCP, MCPError
from ai_suggestions import BaseAnimationSuggester
from animation_timing import AnimationTiming, apply_vercel_entrance, apply_vercel_exit
from animation_sequence import AnimationSequence, vercel_staggered_fade_in, vercel_content_reveal

class EnhancedAnimationSuggester(BaseAnimationSuggester):
    """
    Advanced class for generating sophisticated animations from natural language.
    
    Features improved pattern recognition, error correction, and integration
    with Vercel-style animation patterns.
    """
    
    def __init__(self, mcp=None):
        """
        Initialize the enhanced animation suggester.
        
        Args:
            mcp: Optional MCP instance to use (will create one if not provided)
        """
        super().__init__(mcp)
        self.animation_patterns = self._load_animation_patterns()
        self.vercel_templates = self._load_vercel_templates()
        self.error_corrector = ErrorCorrectionLayer()
        
    def _load_animation_patterns(self):
        """
        Load expanded set of animation patterns with sophisticated regex matching.
        
        Returns:
            Dictionary of animation patterns
        """
        # Return a dictionary with expanded patterns that can catch more nuanced descriptions
        return {
            # Basic movements with expanded synonyms
            "move": {
                "patterns": [
                    r'mov(e|es|ing)|translat(e|es|ing)|slide(s|ing)?|glide(s|ing)?',
                    r'(go|goes|going) (from|to)( the)?( right| left| top| bottom)?',
                    r'travel(s|ing)?|journey(s|ing)?|proceed(s|ing)?',
                    r'shift(s|ing)?|reposition(s|ing)?|relocat(e|es|ing)',
                ],
                "params": ["direction", "distance", "duration"],
                "template": "element.animate_transform('translate', from_value=(0, 0), to_value=({direction_vector}), duration={duration}, easing='easeOutExpo')"
            },
            
            # Rotation with expanded synonyms
            "rotate": {
                "patterns": [
                    r'rotat(e|es|ing)|spin(s|ning)?|turn(s|ing)?|revolv(e|es|ing)',
                    r'twist(s|ing)?|whirl(s|ing)?|circle(s|ing)?',
                    r'orbit(s|ing)?|gyrat(e|es|ing)|pivot(s|ing)?',
                ],
                "params": ["degrees", "duration", "direction"],
                "template": "element.animate_transform('rotate', from_value='0 {center_x} {center_y}', to_value='{degrees} {center_x} {center_y}', duration={duration}, easing='easeInOutCubic')"
            },
            
            # Scaling/pulsing with expanded synonyms
            "scale": {
                "patterns": [
                    r'(scale|scaling|scales|sized?|sizing|resiz(e|es|ing))',
                    r'grow(s|ing)?|expand(s|ing)?|enlarg(e|es|ing)',
                    r'shrink(s|ing)?|contract(s|ing)?|reduc(e|es|ing)',
                    r'puls(e|es|ing)|throb(s|bing)?|beat(s|ing)?',
                    r'(get|gets|getting) (bigger|larger|smaller)',
                ],
                "params": ["scale_factor", "duration", "repeat"],
                "template": "element.animate_transform('scale', from_value='1', to_value='{scale_factor}', duration={duration}, repeat_count='{repeat}', easing='easeInOutQuad')"
            },
            
            # Fading with expanded synonyms
            "fade": {
                "patterns": [
                    r'fad(e|es|ing) (in|out|away)',
                    r'(appear|appears|appearing|disappear|disappears|disappearing)',
                    r'(become|becomes|becoming) (visible|invisible|transparent|opaque)',
                    r'(show|shows|showing|hide|hides|hiding) gradually',
                    r'(increase|increases|increasing|decrease|decreases|decreasing) opacity',
                ],
                "params": ["direction", "duration"],
                "template": "element.animate('opacity', from_value={start_opacity}, to_value={end_opacity}, duration={duration}, easing='easeOutExpo')"
            },
            
            # Bouncing with expanded synonyms
            "bounce": {
                "patterns": [
                    r'bounc(e|es|ing)|jump(s|ing)?|hop(s|ping)?',
                    r'spring(s|ing)?|rebound(s|ing)?|ricochet(s|ing)?',
                    r'pogo(s|ing)?|oscillat(e|es|ing)|undulat(e|es|ing)',
                ],
                "params": ["height", "duration", "repeat"],
                "template": "element.animate('y', from_value={start_y}, to_value={end_y}, duration={duration}, repeat_count='{repeat}', values='{start_y};{mid_y};{end_y}', key_times='0;0.5;1', easing='easeOutBack')"
            },
            
            # Vercel-specific animations
            "vercel_entrance": {
                "patterns": [
                    r'vercel.?(style)? entrance',
                    r'subtle appear(ance)?',
                    r'professional (entrance|intro|appearance)',
                    r'elegant (appear|entrance|intro)',
                    r'modern (appear|entrance|intro)',
                ],
                "params": ["duration", "delay"],
                "template": "apply_vercel_entrance(element, duration={duration}, delay={delay})"
            },
            
            # More Vercel-specific animations
            "staggered_reveal": {
                "patterns": [
                    r'stagger(ed)? (reveal|entrance|appearance)',
                    r'sequence of (elements|items) (appearing|revealing)',
                    r'elements appear(ing)? one (by one|after another)',
                    r'cascade of (elements|items)',
                ],
                "params": ["elements", "delay", "stagger"],
                "template": "vercel_staggered_fade_in(mcp, {elements}, base_delay={delay}, stagger_amount={stagger})"
            },
        }
    
    def _load_vercel_templates(self):
        """
        Load Vercel-inspired animation templates.
        
        Returns:
            Dictionary of Vercel animation templates
        """
        return {
            "hero_entrance": {
                "description": "Vercel-style hero section entrance animation",
                "code": """
                    # Create container
                    container = svg.add_rectangle(x=50, y=50, width=700, height=400, rx=8, fill="#ffffff", stroke="#eaeaea", stroke_width=1, id="hero_container")
                    
                    # Create title
                    title = svg.add_text(x=400, y=150, text="{title_text}", font_size="32px", text_anchor="middle", fill="#000000", font_family="Arial", id="hero_title")
                    
                    # Create subtitle
                    subtitle = svg.add_text(x=400, y=200, text="{subtitle_text}", font_size="18px", text_anchor="middle", fill="#666666", font_family="Arial", id="hero_subtitle")
                    
                    # Create button
                    button = svg.add_rectangle(x=325, y=250, width=150, height=40, rx=4, fill="#0070f3", id="hero_button")
                    button_text = svg.add_text(x=400, y=275, text="{button_text}", font_size="16px", text_anchor="middle", fill="#ffffff", font_family="Arial", id="hero_button_text")
                    
                    # Create animation sequence
                    sequence = AnimationSequence(mcp)
                    
                    # Add container animation
                    sequence.add_attribute_animation(container, "opacity", 0, 1, duration=0.5, delay=0.1, easing="easeOutExpo")
                    sequence.add_transform_animation(container, "scale", "0.98", "1", duration=0.7, delay=0.1, easing="easeOutExpo")
                    
                    # Add content animations
                    sequence.add_attribute_animation(title, "opacity", 0, 1, duration=0.6, delay=0.3, easing="easeOutExpo")
                    sequence.add_transform_animation(title, "translate", "0 20", "0 0", duration=0.7, delay=0.3, easing="easeOutExpo")
                    
                    sequence.add_attribute_animation(subtitle, "opacity", 0, 1, duration=0.6, delay=0.4, easing="easeOutExpo")
                    sequence.add_transform_animation(subtitle, "translate", "0 20", "0 0", duration=0.7, delay=0.4, easing="easeOutExpo")
                    
                    sequence.add_attribute_animation(button, "opacity", 0, 1, duration=0.6, delay=0.5, easing="easeOutExpo")
                    sequence.add_attribute_animation(button_text, "opacity", 0, 1, duration=0.6, delay=0.5, easing="easeOutExpo")
                    sequence.add_transform_animation(button, "translate", "0 20", "0 0", duration=0.7, delay=0.5, easing="easeOutExpo")
                    sequence.add_transform_animation(button_text, "translate", "0 20", "0 0", duration=0.7, delay=0.5, easing="easeOutExpo")
                    
                    # Apply hover effect to button
                    apply_vercel_hover(button, scale=1.03, duration=0.2)
                    
                    # Play the sequence
                    sequence.play()
                """
            },
            
            "feature_grid": {
                "description": "Vercel-style feature grid with staggered reveal",
                "code": """
                    # Create feature items
                    features = []
                    feature_texts = {feature_texts}
                    
                    for i, text in enumerate(feature_texts):
                        row = i // 3
                        col = i % 3
                        x = 100 + col * 250
                        y = 100 + row * 150
                        
                        # Create feature container
                        container = svg.add_rectangle(x=x, y=y, width=200, height=100, rx=8, fill="#ffffff", stroke="#eaeaea", stroke_width=1, id=f"feature_{i}_container")
                        
                        # Create feature icon (circle as placeholder)
                        icon = svg.add_circle(cx=x+30, cy=y+30, r=15, fill="#0070f3", id=f"feature_{i}_icon")
                        
                        # Create feature title
                        title = svg.add_text(x=x+100, y=y+35, text=text, font_size="16px", text_anchor="middle", fill="#000000", font_family="Arial", id=f"feature_{i}_title")
                        
                        # Group items
                        features.append([container, icon, title])
                    
                    # Create staggered animation for each feature group
                    for i, feature_group in enumerate(features):
                        # Create sequence for this feature
                        sequence = AnimationSequence(mcp)
                        
                        # Add animations with staggered delay
                        delay = 0.1 + (i * 0.1)
                        
                        for item in feature_group:
                            # Set initial state
                            item.set_attribute("opacity", "0")
                            item.set_attribute("transform", "translate(0, 20)")
                            
                            # Add animations
                            sequence.add_attribute_animation(item, "opacity", 0, 1, duration=0.6, delay=delay, easing="easeOutExpo")
                            sequence.add_transform_animation(item, "translate", "0 20", "0 0", duration=0.7, delay=delay, easing="easeOutExpo")
                        
                        # Play the sequence
                        sequence.play()
                """
            },
            
            "data_visualization": {
                "description": "Vercel-style animated data visualization",
                "code": """
                    # Create chart background
                    chart_bg = svg.add_rectangle(x=100, y=100, width=600, height=300, rx=8, fill="#ffffff", stroke="#eaeaea", stroke_width=1, id="chart_bg")
                    
                    # Create chart title
                    chart_title = svg.add_text(x=400, y=80, text="{chart_title}", font_size="24px", text_anchor="middle", fill="#000000", font_family="Arial", id="chart_title")
                    
                    # Create data bars
                    data_values = {data_values}
                    max_value = max(data_values)
                    bars = []
                    labels = []
                    
                    for i, value in enumerate(data_values):
                        # Calculate bar height
                        bar_height = (value / max_value) * 250
                        
                        # Create bar
                        bar = svg.add_rectangle(
                            x=150 + i * 100, 
                            y=400 - bar_height, 
                            width=60, 
                            height=bar_height, 
                            fill="#0070f3", 
                            id=f"bar_{i}"
                        )
                        bars.append(bar)
                        
                        # Create label
                        label = svg.add_text(
                            x=180 + i * 100, 
                            y=420, 
                            text=str(value), 
                            font_size="14px", 
                            text_anchor="middle", 
                            fill="#666666", 
                            font_family="Arial", 
                            id=f"label_{i}"
                        )
                        labels.append(label)
                        
                        # Set initial state
                        bar.set_attribute("height", "0")
                        bar.set_attribute("y", "400")
                        label.set_attribute("opacity", "0")
                    
                    # Create animation sequence
                    sequence = AnimationSequence(mcp)
                    
                    # Add background and title animations
                    sequence.add_attribute_animation(chart_bg, "opacity", 0, 1, duration=0.5, delay=0.1, easing="easeOutExpo")
                    sequence.add_attribute_animation(chart_title, "opacity", 0, 1, duration=0.5, delay=0.2, easing="easeOutExpo")
                    
                    # Add staggered bar animations
                    for i, (bar, label) in enumerate(zip(bars, labels)):
                        delay = 0.3 + (i * 0.1)
                        bar_height = (data_values[i] / max_value) * 250
                        
                        # Animate bar height
                        sequence.add_attribute_animation(
                            bar, "height", 0, bar_height, 
                            duration=0.8, delay=delay, 
                            easing="easeOutExpo"
                        )
                        
                        # Animate bar position
                        sequence.add_attribute_animation(
                            bar, "y", 400, 400 - bar_height, 
                            duration=0.8, delay=delay, 
                            easing="easeOutExpo"
                        )
                        
                        # Animate label
                        sequence.add_attribute_animation(
                            label, "opacity", 0, 1, 
                            duration=0.5, delay=delay + 0.2, 
                            easing="easeOutExpo"
                        )
                    
                    # Play the sequence
                    sequence.play()
                """
            }
        }
    
    def parse_description(self, description):
        """
        Parse a natural language description with advanced pattern matching.
        
        Args:
            description: Natural language description of the desired animation
            
        Returns:
            Dictionary with parsed information
        """
        # Initialize result with defaults
        result = {
            "animation_type": "move",  # Default animation type
            "shape_type": "rectangle",  # Default shape type
            "color": "blue",           # Default color
            "duration": 1.0,           # Default duration
            "repeat": "indefinite",    # Default repeat
            "direction": "right",      # Default direction
            "params": {}               # Additional parameters
        }
        
        # Extract shape type
        shape_patterns = {
            "circle": r'(a|an)?\s*(circle|circular|round|sphere|disc|disk)',
            "rectangle": r'(a|an)?\s*(rect(angle)?|square|box|block|rectangular)',
            "path": r'(a|an)?\s*(path|curve|line|shape|custom shape)',
            "text": r'(a|an)?\s*(text|word|phrase|sentence|characters?)',
            "star": r'(a|an)?\s*(star|asterisk)',
            "polygon": r'(a|an)?\s*(polygon|triangle|pentagon|hexagon|octagon)',
        }
        
        for shape, pattern in shape_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                result["shape_type"] = shape
                break
        
        # Extract color
        color_match = re.search(r'(red|blue|green|yellow|orange|purple|pink|black|white|gray|grey|brown|cyan|magenta|teal|navy|olive|maroon|gold|silver|turquoise|violet|indigo|coral|crimson|lime|aqua|fuchsia|plum|tan|khaki|lavender|salmon|azure|beige|ivory|mint|rose)\s+(colou?r(ed)?|fill(ed)?)?', description, re.IGNORECASE)
        if color_match:
            result["color"] = color_match.group(1).lower()
        
        # Extract animation type
        for anim_type, data in self.animation_patterns.items():
            for pattern in data["patterns"]:
                if re.search(pattern, description, re.IGNORECASE):
                    result["animation_type"] = anim_type
                    break
            if result["animation_type"] == anim_type:
                break
        
        # Extract duration
        duration_match = re.search(r'(\d+(\.\d+)?)\s*(s(ec(ond)?s?)?|seconds?)', description, re.IGNORECASE)
        if duration_match:
            result["duration"] = float(duration_match.group(1))
        
        # Extract repeat
        if "once" in description.lower() or "single" in description.lower() or "one time" in description.lower():
            result["repeat"] = "1"
        elif "twice" in description.lower() or "two times" in description.lower():
            result["repeat"] = "2"
        elif "three times" in description.lower():
            result["repeat"] = "3"
        elif "indefinite" in description.lower() or "forever" in description.lower() or "continuously" in description.lower() or "loop" in description.lower():
            result["repeat"] = "indefinite"
        
        # Extract direction for movement
        direction_patterns = {
            "left": r'(to|towards?|from right to) (the )?left',
            "right": r'(to|towards?|from left to) (the )?right',
            "up": r'(to|towards?|from bottom to) (the )?(top|up)',
            "down": r'(to|towards?|from top to) (the )?(bottom|down)',
            "top-left": r'(to|towards?) (the )?(top|upper)[ -]left',
            "top-right": r'(to|towards?) (the )?(top|upper)[ -]right',
            "bottom-left": r'(to|towards?) (the )?(bottom|lower)[ -]left',
            "bottom-right": r'(to|towards?) (the )?(bottom|lower)[ -]right',
        }
        
        for direction, pattern in direction_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                result["direction"] = direction
                break
        
        # Extract text content if shape is text
        if result["shape_type"] == "text":
            text_match = re.search(r'saying ["\']([^"\']+)["\']|text ["\']([^"\']+)["\']|words? ["\']([^"\']+)["\']|phrase ["\']([^"\']+)["\']', description, re.IGNORECASE)
            if text_match:
                # Find the first non-None group
                text_content = next((g for g in text_match.groups() if g is not None), "Hello World")
                result["params"]["text"] = text_content
            else:
                result["params"]["text"] = "Hello World"  # Default text
        
        # Extract size information
        size_match = re.search(r'(\d+)(?:\s*px)?\s+(width|height|size|radius)', description, re.IGNORECASE)
        if size_match:
            size_value = int(size_match.group(1))
            size_type = size_match.group(2).lower()
            
            if size_type == "width":
                result["params"]["width"] = size_value
            elif size_type == "height":
                result["params"]["height"] = size_value
            elif size_type == "radius":
                result["params"]["radius"] = size_value
            else:  # generic size
                if result["shape_type"] == "circle":
                    result["params"]["radius"] = size_value
                else:
                    result["params"]["width"] = size_value
                    result["params"]["height"] = size_value
        
        # Check for Vercel-specific templates
        for template_name, template_data in self.vercel_templates.items():
            if template_name.lower() in description.lower() or template_data["description"].lower() in description.lower():
                result["template"] = template_name
                
                # Extract template-specific parameters
                if template_name == "hero_entrance":
                    # Extract title, subtitle, and button text
                    title_match = re.search(r'title ["\']([^"\']+)["\']', description, re.IGNORECASE)
                    result["params"]["title_text"] = title_match.group(1) if title_match else "Welcome to Our Platform"
                    
                    subtitle_match = re.search(r'subtitle ["\']([^"\']+)["\']', description, re.IGNORECASE)
                    result["params"]["subtitle_text"] = subtitle_match.group(1) if subtitle_match else "The next generation of web development"
                    
                    button_match = re.search(r'button ["\']([^"\']+)["\']', description, re.IGNORECASE)
                    result["params"]["button_text"] = button_match.group(1) if button_match else "Get Started"
                
                elif template_name == "feature_grid":
                    # Extract feature texts
                    feature_match = re.search(r'features ["\']([^"\']+)["\']', description, re.IGNORECASE)
                    if feature_match:
                        features = feature_match.group(1).split(',')
                        result["params"]["feature_texts"] = [f.strip() for f in features]
                    else:
                        result["params"]["feature_texts"] = ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5", "Feature 6"]
                
                elif template_name == "data_visualization":
                    # Extract chart title and data values
                    chart_title_match = re.search(r'chart title ["\']([^"\']+)["\']', description, re.IGNORECASE)
                    result["params"]["chart_title"] = chart_title_match.group(1) if chart_title_match else "Data Visualization"
                    
                    data_match = re.search(r'data values ["\']([^"\']+)["\']', description, re.IGNORECASE)
                    if data_match:
                        try:
                            data_str = data_match.group(1)
                            # Try to parse as comma-separated values
                            data_values = [float(x.strip()) for x in data_str.split(',')]
                            result["params"]["data_values"] = data_values
                        except:
                            result["params"]["data_values"] = [25, 40, 60, 35, 70]
                    else:
                        result["params"]["data_values"] = [25, 40, 60, 35, 70]
        
        return result
    
    def generate_code(self, parsed_info):
        """
        Generate code based on parsed information.
        
        Args:
            parsed_info: Dictionary with parsed animation information
            
        Returns:
            String of executable Python code
        """
        # Start with imports and setup
        code = """
# Animation generated from natural language description
from svg_animation_mcp import MCP
from browser_integration import init_browser_environment
from utils import generate_star_points, generate_path_data
from animation_timing import AnimationTiming, apply_vercel_entrance, apply_vercel_exit, apply_vercel_hover
from animation_sequence import AnimationSequence, vercel_staggered_fade_in, vercel_content_reveal

# Initialize browser environment
init_browser_environment()

# Initialize animation timing
AnimationTiming.initialize(MCP())

# Create MCP instance
mcp = MCP()

# Create SVG canvas
svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
"""
        
        # Check if we're using a Vercel template
        if "template" in parsed_info:
            template_name = parsed_info["template"]
            template_code = self.vercel_templates[template_name]["code"]
            
            # Replace template parameters
            for param_name, param_value in parsed_info["params"].items():
                if isinstance(param_value, list):
                    # Format lists properly
                    param_str = json.dumps(param_value)
                    template_code = template_code.replace(f"{{{param_name}}}", param_str)
                else:
                    template_code = template_code.replace(f"{{{param_name}}}", str(param_value))
            
            # Add the template code
            code += "\n# Using Vercel template: " + template_name + "\n"
            code += template_code
            
            return code
        
        # If not using a template, generate code based on parsed info
        shape_type = parsed_info["shape_type"]
        color = parsed_info["color"]
        animation_type = parsed_info["animation_type"]
        duration = parsed_info["duration"]
        repeat = parsed_info["repeat"]
        direction = parsed_info["direction"]
        params = parsed_info["params"]
        
        # Create the shape
        if shape_type == "circle":
            radius = params.get("radius", 50)
            code += f"""
# Create a {color} circle
circle = svg.add_circle(cx=400, cy=300, r={radius}, fill="{color}", id="animated_circle")
element = circle  # Reference for animation
"""
        
        elif shape_type == "rectangle":
            width = params.get("width", 100)
            height = params.get("height", 80)
            code += f"""
# Create a {color} rectangle
rect = svg.add_rectangle(x=350, y=260, width={width}, height={height}, fill="{color}", id="animated_rect")
element = rect  # Reference for animation
"""
        
        elif shape_type == "text":
            text = params.get("text", "Hello World")
            code += f"""
# Create {color} text
text = svg.add_text(x=400, y=300, text="{text}", fill="{color}", font_size="24px", text_anchor="middle", font_family="Arial", id="animated_text")
element = text  # Reference for animation
"""
        
        elif shape_type == "star":
            code += f"""
# Create a {color} star
star_points = generate_star_points(cx=400, cy=300, outer_radius=100, inner_radius=50, points=5)
star_path_data = generate_path_data(star_points) + " Z"  # Z closes the path
star = svg.add_path(d=star_path_data, fill="{color}", id="animated_star")
element = star  # Reference for animation
"""
        
        elif shape_type == "polygon":
            sides = params.get("sides", 6)
            code += f"""
# Create a {color} polygon
polygon_points = generate_polygon_points(cx=400, cy=300, radius=100, sides={sides})
polygon_path_data = generate_path_data(polygon_points) + " Z"  # Z closes the path
polygon = svg.add_path(d=polygon_path_data, fill="{color}", id="animated_polygon")
element = polygon  # Reference for animation
"""
        
        else:  # Default to path
            code += f"""
# Create a {color} path
path = svg.add_path(d="M350,250 L450,250 L400,350 Z", fill="{color}", id="animated_path")
element = path  # Reference for animation
"""
        
        # Add animation based on type
        if animation_type == "move":
            # Map direction to vector
            direction_vectors = {
                "left": "(-200, 0)",
                "right": "(200, 0)",
                "up": "(0, -200)",
                "down": "(0, 200)",
                "top-left": "(-200, -200)",
                "top-right": "(200, -200)",
                "bottom-left": "(-200, 200)",
                "bottom-right": "(200, 200)"
            }
            vector = direction_vectors.get(direction, "(200, 0)")
            
            code += f"""
# Create a movement animation
sequence = AnimationSequence(mcp)
sequence.add_transform_animation(element, "translate", from_value="0 0", to_value="{vector}", duration={duration}, easing="easeOutExpo", repeat_count="{repeat}")
sequence.play()
"""
        
        elif animation_type == "rotate":
            degrees = params.get("degrees", 360)
            center_x = 400  # Default x-center for rotation
            center_y = 300  # Default y-center for rotation
            
            code += f"""
# Create a rotation animation
sequence = AnimationSequence(mcp)
sequence.add_transform_animation(element, "rotate", from_value="0 {center_x} {center_y}", to_value="{degrees} {center_x} {center_y}", duration={duration}, easing="easeInOutCubic", repeat_count="{repeat}")
sequence.play()
"""
        
        elif animation_type == "scale":
            scale_factor = params.get("scale_factor", 1.5)
            
            code += f"""
# Create a scaling/pulsing animation
sequence = AnimationSequence(mcp)
sequence.add_transform_animation(element, "scale", from_value="1", to_value="{scale_factor}", duration={duration}, easing="easeInOutQuad", repeat_count="{repeat}")
sequence.play()
"""
        
        elif animation_type == "fade":
            if "in" in direction:
                start_opacity = 0
                end_opacity = 1
                # Set initial opacity
                code += "# Set initial opacity\nelement.set_attribute('opacity', '0')\n"
            else:  # fade out
                start_opacity = 1
                end_opacity = 0
            
            code += f"""
# Create a fade animation
sequence = AnimationSequence(mcp)
sequence.add_attribute_animation(element, "opacity", from_value={start_opacity}, to_value={end_opacity}, duration={duration}, easing="easeOutExpo", repeat_count="{repeat}")
sequence.play()
"""
        
        elif animation_type == "bounce":
            height = params.get("height", 50)
            start_y = 300  # Default y position
            mid_y = start_y - height  # Highest point
            end_y = start_y  # Back to original position
            
            code += f"""
# Create a bounce animation
sequence = AnimationSequence(mcp)
sequence.add_attribute_animation(
    element, "y", from_value={start_y}, to_value={end_y}, 
    duration={duration}, easing="easeOutBack", repeat_count="{repeat}",
    values="{start_y};{mid_y};{end_y}", key_times="0;0.5;1"
)
sequence.play()
"""
        
        elif animation_type == "vercel_entrance":
            delay = params.get("delay", 0)
            
            code += f"""
# Create a Vercel-style entrance animation
apply_vercel_entrance(element, duration={duration}, delay={delay})
"""
        
        elif animation_type == "staggered_reveal":
            # Staggered animations typically need multiple elements
            # For demonstration, we'll create multiple copies of the element
            stagger_amount = params.get("stagger", 0.05)
            base_delay = params.get("delay", 0)
            
            code += f"""
# Create multiple elements for staggered animation
elements = []
for i in range(5):
    # Create copies at different positions
    x_offset = i * 100
    if element.id.startswith('animated_circle'):
        copy = svg.add_circle(cx=200 + x_offset, cy=300, r={params.get('radius', 50)}, fill="{color}", id=f"staggered_{{i}}")
    elif element.id.startswith('animated_rect'):
        copy = svg.add_rectangle(x=150 + x_offset, y=260, width={params.get('width', 100)}, height={params.get('height', 80)}, fill="{color}", id=f"staggered_{{i}}")
    elif element.id.startswith('animated_text'):
        copy = svg.add_text(x=200 + x_offset, y=300, text="{params.get('text', 'Hello')}", fill="{color}", font_size="24px", text_anchor="middle", font_family="Arial", id=f"staggered_{{i}}")
    else:
        # For other shapes, create rectangles as a fallback
        copy = svg.add_rectangle(x=150 + x_offset, y=260, width=80, height=80, fill="{color}", id=f"staggered_{{i}}")
    
    elements.append(copy)

# Create staggered animation
vercel_staggered_fade_in(mcp, elements, base_delay={base_delay}, stagger_amount={stagger_amount})
"""
        
        else:
            # Default simple animation if type not recognized
            code += f"""
# Create a simple animation
element.animate("opacity", from_value=0.5, to_value=1, duration={duration}, repeat_count="{repeat}")
"""
        
        return code
    
    def suggest_animation(self, description):
        """
        Suggest an animation based on a natural language description.
        
        Args:
            description: Natural language description of the desired animation
            
        Returns:
            Dictionary with code and explanation
        """
        try:
            # Parse the description
            parsed_info = self.parse_description(description)
            
            # Validate and fix parsed information
            parsed_info = self.error_corrector.validate_animation_params(parsed_info)
            
            # Generate code
            code = self.generate_code(parsed_info)
            
            return {
                "code": code,
                "explanation": f"Generated Vercel-quality animation code for: {description}",
                "parsed_info": parsed_info
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


class ErrorCorrectionLayer:
    """
    Validate and fix common LLM-generated animation issues.
    
    This class checks for and corrects common errors in animation parameters
    to ensure the generated animations work correctly.
    """
    
    def validate_animation_params(self, params):
        """
        Validate and fix animation parameters if necessary.
        
        Args:
            params: Dictionary of animation parameters
            
        Returns:
            Validated and fixed parameters
        """
        # Make a copy to avoid modifying the original
        validated = params.copy()
        
        # Validate duration (must be positive)
        if validated["duration"] <= 0:
            validated["duration"] = 1.0
        
        # Validate color (must be a valid color name or hex)
        color = validated["color"]
        valid_colors = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink", 
            "black", "white", "gray", "grey", "brown", "cyan", "magenta",
            "teal", "navy", "olive", "maroon", "gold", "silver"
        ]
        
        if color not in valid_colors and not re.match(r'^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$', color):
            validated["color"] = "blue"  # Default to blue if invalid
        
        # Validate repeat count
        if validated["repeat"] not in ["indefinite", "1", "2", "3", "4", "5"]:
            validated["repeat"] = "indefinite"
        
        # Shape-specific validations
        if validated["shape_type"] == "circle":
            radius = validated["params"].get("radius", 50)
            if radius <= 0:
                validated["params"]["radius"] = 50
        
        elif validated["shape_type"] == "rectangle":
            width = validated["params"].get("width", 100)
            height = validated["params"].get("height", 80)
            if width <= 0:
                validated["params"]["width"] = 100
            if height <= 0:
                validated["params"]["height"] = 80
        
        return validated


def generate_animation_from_text(description):
    """
    Generate and execute an animation from a text description.
    
    This is the main entry point for the AI suggestion system.
    
    Args:
        description: Natural language description of the desired animation
        
    Returns:
        Dictionary with result information
    """
    suggester = EnhancedAnimationSuggester()
    success = suggester.execute_suggestion(description)
    
    if success:
        return {
            "status": "success",
            "message": f"Generated Vercel-quality animation from description: {description}"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to generate animation from description"
        } 