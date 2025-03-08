"""
Utilities for SVG Animation MCP.

This module provides utility functions for working with SVG animations.
"""

import math
import json
import re


def validate_color(color):
    """
    Validate and normalize color values.
    
    Args:
        color: Color value (hex, rgb, or named color)
        
    Returns:
        Normalized color string
        
    Raises:
        ValueError: If the color is invalid
    """
    # Check if it's a valid hex color
    if color.startswith('#'):
        # Validate hex format (#RGB or #RRGGBB)
        if re.match(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$', color):
            return color.lower()
        raise ValueError(f"Invalid hex color format: {color}")
    
    # Check if it's a valid rgb color
    rgb_match = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return f"rgb({r}, {g}, {b})"
        raise ValueError(f"RGB values must be between 0 and 255: {color}")
    
    # Check if it's a valid rgba color
    rgba_match = re.match(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)', color)
    if rgba_match:
        r, g, b, a = rgba_match.groups()
        r, g, b = map(int, [r, g, b])
        a = float(a)
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0 <= a <= 1:
            return f"rgba({r}, {g}, {b}, {a})"
        raise ValueError(f"Invalid RGBA values: {color}")
    
    # List of valid CSS color names
    valid_css_colors = [
        "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black",
        "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse",
        "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
        "darkgoldenrod", "darkgray", "darkgreen", "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen",
        "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", "darkslategray",
        "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey",
        "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro", "ghostwhite",
        "gold", "goldenrod", "gray", "green", "greenyellow", "grey", "honeydew", "hotpink", "indianred",
        "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue",
        "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink",
        "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey", "lightsteelblue",
        "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue",
        "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen",
        "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin",
        "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid",
        "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff",
        "peru", "pink", "plum", "powderblue", "purple", "rebeccapurple", "red", "rosybrown", "royalblue",
        "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue",
        "slateblue", "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "teal",
        "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"
    ]
    
    # For named colors, check against valid CSS color names
    if color.lower() in valid_css_colors:
        return color
    
    raise ValueError(f"Invalid color name: {color}")


def validate_number(value, min_value=None, max_value=None, name="value"):
    """
    Validate a numeric value.
    
    Args:
        value: Numeric value to validate
        min_value: Optional minimum value
        max_value: Optional maximum value
        name: Name of the value for error messages
        
    Returns:
        The validated number
        
    Raises:
        ValueError: If the number is invalid
    """
    try:
        num = float(value)
        
        if min_value is not None and num < min_value:
            raise ValueError(f"{name} must be at least {min_value}")
        
        if max_value is not None and num > max_value:
            raise ValueError(f"{name} must be at most {max_value}")
            
        return num
    except (ValueError, TypeError):
        raise ValueError(f"Invalid number for {name}: {value}")


def rgb_to_hex(r, g, b):
    """
    Convert RGB color values to hexadecimal color string.
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        
    Returns:
        Hexadecimal color string (e.g. "#ff0000")
    """
    # Validate RGB values
    r = validate_number(r, 0, 255, "Red")
    g = validate_number(g, 0, 255, "Green")
    b = validate_number(b, 0, 255, "Blue")
    
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def hex_to_rgb(hex_color):
    """
    Convert hexadecimal color string to RGB values.
    
    Args:
        hex_color: Hexadecimal color string (e.g. "#ff0000")
        
    Returns:
        Tuple of (r, g, b) values
    """
    hex_color = hex_color.lstrip("#")
    
    # Handle shorthand hex format (#RGB)
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color format: #{hex_color}")
    
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_path_data(points):
    """
    Generate SVG path data from a list of points.
    
    Args:
        points: List of (x, y) coordinates
        
    Returns:
        SVG path data string
    """
    if not points:
        return ""
    
    path_data = f"M {points[0][0]} {points[0][1]}"
    for x, y in points[1:]:
        path_data += f" L {x} {y}"
    
    return path_data


def generate_polygon_points(cx, cy, radius, sides):
    """
    Generate points for a regular polygon.
    
    Args:
        cx: X-coordinate of the center
        cy: Y-coordinate of the center
        radius: Radius of the polygon
        sides: Number of sides
        
    Returns:
        List of (x, y) coordinates
    """
    if sides < 3:
        raise ValueError("Polygon must have at least 3 sides")
    
    points = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    
    return points


def generate_star_points(cx, cy, outer_radius, inner_radius, points):
    """
    Generate points for a star shape.
    
    Args:
        cx: X-coordinate of the center
        cy: Y-coordinate of the center
        outer_radius: Outer radius of the star
        inner_radius: Inner radius of the star
        points: Number of points
        
    Returns:
        List of (x, y) coordinates
    """
    if points < 2:
        raise ValueError("Star must have at least 2 points")
    
    result = []
    for i in range(points * 2):
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle = math.pi * i / points - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        result.append((x, y))
    
    return result


def interpolate_color(color1, color2, ratio):
    """
    Interpolate between two colors.
    
    Args:
        color1: First color (hex string)
        color2: Second color (hex string)
        ratio: Ratio of interpolation (0-1)
        
    Returns:
        Interpolated color (hex string)
    """
    # Validate the colors
    color1 = validate_color(color1)
    color2 = validate_color(color2)
    
    # If both colors are hex, interpolate them
    if color1.startswith('#') and color2.startswith('#'):
        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        return rgb_to_hex(r, g, b)
    
    # For other color formats, just return the first color for ratio < 0.5, second otherwise
    return color1 if ratio < 0.5 else color2


def bezier_curve_points(p0, p1, p2, p3, num_points=20):
    """
    Generate points along a cubic Bezier curve.
    
    Args:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y)
        p3: End point (x, y)
        num_points: Number of points to generate
        
    Returns:
        List of (x, y) coordinates
    """
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    
    return points


def serialize_animation_config(config):
    """
    Serialize animation configuration to JSON string.
    
    Args:
        config: Animation configuration dictionary
        
    Returns:
        JSON string
    """
    return json.dumps(config, indent=2)


def deserialize_animation_config(json_str):
    """
    Deserialize JSON string to animation configuration.
    
    Args:
        json_str: JSON string
        
    Returns:
        Animation configuration dictionary
    """
    return json.loads(json_str)


def escape_js_string(s):
    """
    Escape a string for use in JavaScript.
    
    Args:
        s: String to escape
        
    Returns:
        Escaped string
    """
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')


def validate_animation_duration(duration):
    """
    Validate animation duration.
    
    Args:
        duration: Animation duration in seconds
        
    Returns:
        Validated duration
        
    Raises:
        ValueError: If the duration is invalid
    """
    return validate_number(duration, 0.01, None, "Animation duration") 