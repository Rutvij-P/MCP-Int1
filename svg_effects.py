"""
SVG Visual Effects & Filters Module for SVG Animation MCP.

This module provides high-performance animations with advanced SVG visual effects,
inspired by Vercel's polished, professional look. It includes filters, gradients,
masks, and clip paths for creating sophisticated visual effects.
"""

from browser_integration import execute_js

class SVGFilters:
    """
    Provides methods for creating and applying SVG filter effects.
    
    Implements professional-grade filter effects similar to those used on
    Vercel's website, including drop shadows, blurs, and color effects.
    """
    
    def __init__(self, mcp):
        """
        Initialize the SVGFilters class.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.filter_id_counter = 0
        self.filter_map = {}
        
    def _generate_filter_id(self, prefix="filter"):
        """Generate a unique ID for a filter."""
        filter_id = f"{prefix}_{self.filter_id_counter}"
        self.filter_id_counter += 1
        return filter_id
        
    def create_drop_shadow(self, dx=2, dy=2, std_deviation=3, flood_opacity=0.3, flood_color="#000000"):
        """
        Create a subtle drop shadow filter similar to Vercel's style.
        
        Args:
            dx: Horizontal offset of the shadow
            dy: Vertical offset of the shadow
            std_deviation: Standard deviation for the Gaussian blur
            flood_opacity: Opacity of the shadow (0-1)
            flood_color: Color of the shadow
            
        Returns:
            Filter ID to be used with elements
        """
        filter_id = self._generate_filter_id("drop_shadow")
        
        # Ensure SVG has a defs element
        svg_id = self.mcp.element_map.get("svg", {}).get("id", "svg_0")
        defs_id = self._ensure_defs_element(svg_id)
        
        js_code = f"""
        (function() {{
            var defs = document.getElementById('{defs_id}');
            if (!defs) return null;
            
            var filter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
            filter.setAttribute('id', '{filter_id}');
            filter.setAttribute('x', '-50%');
            filter.setAttribute('y', '-50%');
            filter.setAttribute('width', '200%');
            filter.setAttribute('height', '200%');
            
            // Create feOffset
            var feOffset = document.createElementNS('http://www.w3.org/2000/svg', 'feOffset');
            feOffset.setAttribute('in', 'SourceAlpha');
            feOffset.setAttribute('dx', '{dx}');
            feOffset.setAttribute('dy', '{dy}');
            feOffset.setAttribute('result', 'offOut');
            filter.appendChild(feOffset);
            
            // Create feGaussianBlur
            var feBlur = document.createElementNS('http://www.w3.org/2000/svg', 'feGaussianBlur');
            feBlur.setAttribute('in', 'offOut');
            feBlur.setAttribute('stdDeviation', '{std_deviation}');
            feBlur.setAttribute('result', 'blurOut');
            filter.appendChild(feBlur);
            
            // Create feColorMatrix to adjust shadow color
            var feColorMatrix = document.createElementNS('http://www.w3.org/2000/svg', 'feColorMatrix');
            feColorMatrix.setAttribute('in', 'blurOut');
            feColorMatrix.setAttribute('type', 'matrix');
            feColorMatrix.setAttribute('values', '0 0 0 0 {parseInt(flood_color.slice(1,3),16)/255} 0 0 0 0 {parseInt(flood_color.slice(3,5),16)/255} 0 0 0 0 {parseInt(flood_color.slice(5,7),16)/255} 0 0 0 {flood_opacity} 0');
            feColorMatrix.setAttribute('result', 'shadowOut');
            filter.appendChild(feColorMatrix);
            
            // Create feBlend to composite with original
            var feBlend = document.createElementNS('http://www.w3.org/2000/svg', 'feBlend');
            feBlend.setAttribute('in', 'SourceGraphic');
            feBlend.setAttribute('in2', 'shadowOut');
            feBlend.setAttribute('mode', 'normal');
            filter.appendChild(feBlend);
            
            defs.appendChild(filter);
            return '{filter_id}';
        }})();
        """
        
        result = execute_js(js_code)
        if result:
            self.filter_map[filter_id] = {
                "type": "drop_shadow",
                "params": {
                    "dx": dx,
                    "dy": dy,
                    "std_deviation": std_deviation,
                    "flood_opacity": flood_opacity,
                    "flood_color": flood_color
                }
            }
            return filter_id
        return None
        
    def create_blur_effect(self, std_deviation=3):
        """
        Create a Gaussian blur filter for depth and focus effects.
        
        Args:
            std_deviation: Standard deviation for the Gaussian blur
            
        Returns:
            Filter ID to be used with elements
        """
        # Implementation details here
        
    def create_glow_effect(self, std_deviation=3, flood_color="#4287f5", flood_opacity=0.8):
        """
        Create a glow effect filter for highlights and emphasis.
        
        Args:
            std_deviation: Standard deviation for the Gaussian blur
            flood_color: Color of the glow
            flood_opacity: Opacity of the glow (0-1)
            
        Returns:
            Filter ID to be used with elements
        """
        # Implementation details here
        
    def create_color_matrix(self, matrix_type="saturate", value=2):
        """
        Create a color matrix filter for color manipulation.
        
        Args:
            matrix_type: Type of color matrix ('saturate', 'hueRotate', 'luminanceToAlpha', etc.)
            value: Value for the color matrix
            
        Returns:
            Filter ID to be used with elements
        """
        # Implementation details here
        
    def apply_filter(self, element, filter_id):
        """
        Apply a filter to an SVG element.
        
        Args:
            element: SVG element to apply the filter to
            filter_id: ID of the filter to apply
            
        Returns:
            True if successful, False otherwise
        """
        if not element or not hasattr(element, 'id'):
            print("Error: Invalid element provided")
            return False
        
        if not filter_id or filter_id not in self.filter_map:
            print(f"Error: Filter ID '{filter_id}' not found")
            return False
        
        js_code = f"""
        (function() {{
            var element = document.getElementById('{element.id}');
            if (!element) return false;
            
            element.setAttribute('filter', 'url(#{filter_id})');
            return true;
        }})();
        """
        
        try:
            result = execute_js(js_code)
            return result
        except Exception as e:
            print(f"Error applying filter: {str(e)}")
            return False

class SVGGradients:
    """
    Provides methods for creating and applying SVG gradients.
    
    Implements professional-grade gradient effects similar to those used on
    Vercel's website, including linear, radial, and animated gradients.
    """
    
    def __init__(self, mcp):
        """
        Initialize the SVGGradients class.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.gradient_id_counter = 0
        self.gradient_map = {}
        
    def _generate_gradient_id(self, prefix="gradient"):
        """Generate a unique ID for a gradient."""
        gradient_id = f"{prefix}_{self.gradient_id_counter}"
        self.gradient_id_counter += 1
        return gradient_id
        
    def create_linear_gradient(self, x1="0%", y1="0%", x2="100%", y2="0%", stops=None):
        """
        Create a linear gradient with Vercel's color schemes.
        
        Args:
            x1: Starting x-coordinate
            y1: Starting y-coordinate
            x2: Ending x-coordinate
            y2: Ending y-coordinate
            stops: List of dictionaries with 'offset', 'color', and 'opacity' keys
            
        Returns:
            Gradient ID to be used with elements
        """
        # Implementation details here
        
    def create_radial_gradient(self, cx="50%", cy="50%", r="50%", fx="50%", fy="50%", stops=None):
        """
        Create a radial gradient for spotlight effects.
        
        Args:
            cx: Center x-coordinate
            cy: Center y-coordinate
            r: Radius
            fx: Focal point x-coordinate
            fy: Focal point y-coordinate
            stops: List of dictionaries with 'offset', 'color', and 'opacity' keys
            
        Returns:
            Gradient ID to be used with elements
        """
        # Implementation details here
        
    def create_animated_gradient(self, gradient_type="linear", duration=5, repeat_count="indefinite", **kwargs):
        """
        Create an animated gradient for subtle movement.
        
        Args:
            gradient_type: Type of gradient ('linear' or 'radial')
            duration: Duration of the animation in seconds
            repeat_count: Number of times to repeat the animation
            **kwargs: Additional parameters for the gradient
            
        Returns:
            Gradient ID to be used with elements
        """
        # Implementation details here
        
    def apply_gradient(self, element, gradient_id):
        """
        Apply a gradient to an SVG element.
        
        Args:
            element: SVG element to apply the gradient to
            gradient_id: ID of the gradient to apply
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here

class SVGMasks:
    """
    Provides methods for creating and applying SVG masks and clip paths.
    
    Implements professional-grade masking effects similar to those used on
    Vercel's website, including reveal/hide effects and text masking.
    """
    
    def __init__(self, mcp):
        """
        Initialize the SVGMasks class.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.mask_id_counter = 0
        self.mask_map = {}
        
    def _generate_mask_id(self, prefix="mask"):
        """Generate a unique ID for a mask."""
        mask_id = f"{prefix}_{self.mask_id_counter}"
        self.mask_id_counter += 1
        return mask_id
        
    def create_reveal_mask(self, shape="rect", animation_type="wipe", duration=1, **kwargs):
        """
        Create a reveal/hide effect for dramatic entrances.
        
        Args:
            shape: Shape of the mask ('rect', 'circle', 'path')
            animation_type: Type of animation ('wipe', 'fade', 'zoom')
            duration: Duration of the animation in seconds
            **kwargs: Additional parameters for the mask
            
        Returns:
            Mask ID to be used with elements
        """
        # Implementation details here
        
    def create_text_mask(self, text, font_size=24, font_family="Arial", **kwargs):
        """
        Create a text mask for creative typography.
        
        Args:
            text: Text to use as a mask
            font_size: Font size
            font_family: Font family
            **kwargs: Additional parameters for the mask
            
        Returns:
            Mask ID to be used with elements
        """
        # Implementation details here
        
    def create_progressive_reveal(self, steps=5, duration=2, delay=0.1, **kwargs):
        """
        Create a progressive reveal effect (Vercel-style).
        
        Args:
            steps: Number of steps in the reveal
            duration: Duration of each step in seconds
            delay: Delay between steps in seconds
            **kwargs: Additional parameters for the mask
            
        Returns:
            Mask ID to be used with elements
        """
        # Implementation details here
        
    def apply_mask(self, element, mask_id):
        """
        Apply a mask to an SVG element.
        
        Args:
            element: SVG element to apply the mask to
            mask_id: ID of the mask to apply
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here

class SVGPerformance:
    """
    Provides methods for optimizing SVG animation performance.
    
    Implements best practices for high-performance SVG animations,
    including requestAnimationFrame, will-change hints, and batched updates.
    """
    
    def __init__(self, mcp):
        """
        Initialize the SVGPerformance class.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        
    def optimize_element(self, element, techniques=None):
        """
        Apply performance optimization techniques to an SVG element.
        
        Args:
            element: SVG element to optimize
            techniques: List of optimization techniques to apply
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here
        
    def setup_request_animation_frame(self):
        """
        Set up requestAnimationFrame for smooth animations.
        
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here
        
    def add_will_change_hint(self, element, properties=None):
        """
        Add will-change hints for browser rendering optimization.
        
        Args:
            element: SVG element to optimize
            properties: List of properties that will change
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here
        
    def setup_batched_updates(self):
        """
        Set up batched animation updates for efficiency.
        
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here
        
    def implement_visibility_culling(self, svg, viewport_margin=100):
        """
        Implement visibility culling for off-screen elements.
        
        Args:
            svg: SVG element
            viewport_margin: Margin around the viewport in pixels
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here

    def _has_browser_support(self, feature):
        """
        Check if the browser supports a specific feature.
        
        Args:
            feature: Feature to check ('will-change', 'filters', etc.)
            
        Returns:
            True if supported, False otherwise
        """
        js_code = f"""
        (function() {{
            switch('{feature}') {{
                case 'will-change':
                    return 'willChange' in document.documentElement.style;
                case 'filters':
                    return 'filter' in document.documentElement.style;
                case 'requestAnimationFrame':
                    return typeof window.requestAnimationFrame === 'function';
                default:
                    return false;
            }}
        }})();
        """
        
        try:
            return execute_js(js_code) or False
        except:
            return False

class SVGPresets:
    """
    Provides predefined visual effects inspired by Vercel's design.
    
    Implements ready-to-use effects for common UI elements,
    including card hover effects, background animations, and loading states.
    """
    
    def __init__(self, mcp):
        """
        Initialize the SVGPresets class.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.filters = SVGFilters(mcp)
        self.gradients = SVGGradients(mcp)
        self.masks = SVGMasks(mcp)
        
    def apply_card_hover_effect(self, element, effect_type="shadow", **kwargs):
        """
        Apply a Vercel-inspired card hover effect.
        
        Args:
            element: SVG element to apply the effect to
            effect_type: Type of effect ('shadow', 'scale', 'glow')
            **kwargs: Additional parameters for the effect
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here
        
    def create_subtle_background_animation(self, svg, effect_type="wave", **kwargs):
        """
        Create a subtle background animation.
        
        Args:
            svg: SVG element
            effect_type: Type of effect ('wave', 'pulse', 'drift')
            **kwargs: Additional parameters for the animation
            
        Returns:
            Animation object
        """
        # Implementation details here
        
    def create_loading_animation(self, svg, style="dots", **kwargs):
        """
        Create a loading state animation.
        
        Args:
            svg: SVG element
            style: Style of the loading animation ('dots', 'spinner', 'pulse')
            **kwargs: Additional parameters for the animation
            
        Returns:
            Animation object
        """
        # Implementation details here
        
    def create_focus_indicator(self, element, style="outline", **kwargs):
        """
        Create a focus/selection indicator.
        
        Args:
            element: SVG element to apply the indicator to
            style: Style of the indicator ('outline', 'glow', 'pulse')
            **kwargs: Additional parameters for the indicator
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation details here

class SVGEffects:
    """
    Main class for SVG visual effects and filters.
    
    Provides access to all SVG effect classes and utilities.
    """
    
    def __init__(self, mcp):
        """
        Initialize the SVGEffects class.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.filters = SVGFilters(mcp)
        self.gradients = SVGGradients(mcp)
        self.masks = SVGMasks(mcp)
        self.performance = SVGPerformance(mcp)
        self.presets = SVGPresets(mcp)
        
    def _ensure_defs_element(self, svg_id):
        """
        Ensure the SVG has a defs element for storing definitions.
        
        Args:
            svg_id: ID of the SVG element
            
        Returns:
            ID of the defs element
        """
        js_code = f"""
        (function() {{
            var svg = document.getElementById('{svg_id}');
            if (!svg) return null;
            
            var defs = svg.querySelector('defs');
            if (!defs) {{
                defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
                defs.setAttribute('id', '{svg_id}_defs');
                svg.prepend(defs);
            }}
            return defs.id;
        }})();
        """
        return execute_js(js_code)
        
    def create_animated_effect(self, element, effect_type, animation_params=None):
        """
        Create an animated effect using the animation system.
        
        Args:
            element: SVG element to animate
            effect_type: Type of effect ('filter', 'gradient', 'mask')
            animation_params: Parameters for the animation
            
        Returns:
            Animation sequence object
        """
        from animation_sequence import AnimationSequence
        
        if not animation_params:
            animation_params = {}
        
        sequence = AnimationSequence(self.mcp)
        
        if effect_type == 'filter':
            # Create filter animation
            filter_id = self.filters.create_glow_effect(**animation_params.get('filter_params', {}))
            self.filters.apply_filter(element, filter_id)
            
            # Animate filter properties
            if 'animation' in animation_params:
                for param in animation_params['animation']:
                    sequence.add_attribute_animation(
                        element, 
                        param['attribute'],
                        param['from_value'],
                        param['to_value'],
                        param.get('duration', 1),
                        param.get('delay', 0),
                        param.get('easing', 'easeInOutCubic')
                    )
        
        # Similar implementations for gradient and mask
        
        return sequence
    
    def cleanup_unused_filters(self):
        """
        Remove unused filters from the SVG.
        
        Returns:
            Number of filters removed
        """
        js_code = """
        (function() {
            var filters = document.querySelectorAll('filter');
            var count = 0;
            
            for (var i = 0; i < filters.length; i++) {
                var filter = filters[i];
                var filterId = filter.id;
                
                // Check if any element uses this filter
                var elements = document.querySelectorAll('[filter="url(#' + filterId + ')"]');
                if (elements.length === 0) {
                    // No elements use this filter, so remove it
                    filter.parentNode.removeChild(filter);
                    count++;
                }
            }
            
            return count;
        })();
        """
        
        try:
            result = execute_js(js_code)
            # Update the filter_map to remove deleted filters
            return result
        except Exception as e:
            print(f"Error cleaning up filters: {str(e)}")
            return 0

    def integrate_with_ai_suggestions(self, suggester):
        """
        Integrate SVG effects with the Enhanced AI Suggestions module.
        
        Args:
            suggester: EnhancedAnimationSuggester instance
            
        Returns:
            True if successful, False otherwise
        """
        if not hasattr(suggester, 'effects'):
            suggester.effects = self
        return True

    def cleanup_all_unused_resources(self):
        """
        Clean up all unused filters, gradients, and masks.
        
        Returns:
            Dictionary with counts of removed resources
        """
        results = {
            'filters': self.cleanup_unused_filters(),
            'gradients': 0,  # Implement similar methods for gradients
            'masks': 0       # Implement similar methods for masks
        }
        return results

    def apply_combined_effects(self, element, effects_config):
        """
        Apply multiple effects to an element in sequence.
        
        Args:
            element: SVG element to apply effects to
            effects_config: Dictionary with effect configurations in the format:
                {
                    "filters": [
                        {"type": "drop_shadow", "params": {...}},
                        {"type": "glow", "params": {...}}
                    ],
                    "gradients": [
                        {"type": "linear", "params": {...}}
                    ],
                    "masks": [
                        {"type": "reveal", "params": {...}}
                    ],
                    "animations": [
                        {"type": "filter_animation", "params": {...}},
                        {"type": "mask_animation", "params": {...}}
                    ],
                    "performance": {
                        "techniques": ["will_change", "batched_updates"]
                    }
                }
            
        Returns:
            Dictionary with IDs of applied effects and animation sequences
        """
        if not element or not hasattr(element, 'id'):
            print("Error: Invalid element provided")
            return None
        
        results = {
            "filters": [],
            "gradients": [],
            "masks": [],
            "animations": [],
            "performance": False
        }
        
        # Apply performance optimizations first if specified
        if "performance" in effects_config:
            perf_config = effects_config["performance"]
            techniques = perf_config.get("techniques", [])
            if techniques:
                success = self.performance.optimize_element(element, techniques)
                results["performance"] = success
        
        # Apply filters
        if "filters" in effects_config:
            for filter_config in effects_config["filters"]:
                filter_type = filter_config.get("type")
                params = filter_config.get("params", {})
                
                filter_id = None
                if filter_type == "drop_shadow":
                    filter_id = self.filters.create_drop_shadow(**params)
                elif filter_type == "blur":
                    filter_id = self.filters.create_blur_effect(**params)
                elif filter_type == "glow":
                    filter_id = self.filters.create_glow_effect(**params)
                elif filter_type == "color_matrix":
                    filter_id = self.filters.create_color_matrix(**params)
                
                if filter_id:
                    self.filters.apply_filter(element, filter_id)
                    results["filters"].append(filter_id)
        
        # Apply gradients
        if "gradients" in effects_config:
            for gradient_config in effects_config["gradients"]:
                gradient_type = gradient_config.get("type")
                params = gradient_config.get("params", {})
                
                gradient_id = None
                if gradient_type == "linear":
                    gradient_id = self.gradients.create_linear_gradient(**params)
                elif gradient_type == "radial":
                    gradient_id = self.gradients.create_radial_gradient(**params)
                elif gradient_type == "animated":
                    gradient_id = self.gradients.create_animated_gradient(**params)
                
                if gradient_id:
                    self.gradients.apply_gradient(element, gradient_id)
                    results["gradients"].append(gradient_id)
        
        # Apply masks
        if "masks" in effects_config:
            for mask_config in effects_config["masks"]:
                mask_type = mask_config.get("type")
                params = mask_config.get("params", {})
                
                mask_id = None
                if mask_type == "reveal":
                    mask_id = self.masks.create_reveal_mask(**params)
                elif mask_type == "text":
                    mask_id = self.masks.create_text_mask(**params)
                elif mask_type == "progressive":
                    mask_id = self.masks.create_progressive_reveal(**params)
                
                if mask_id:
                    self.masks.apply_mask(element, mask_id)
                    results["masks"].append(mask_id)
        
        # Apply animations last
        if "animations" in effects_config:
            from animation_sequence import AnimationSequence
            
            # Create a master sequence to coordinate all animations
            master_sequence = AnimationSequence(self.mcp)
            
            for anim_config in effects_config["animations"]:
                anim_type = anim_config.get("type")
                params = anim_config.get("params", {})
                
                if anim_type == "filter_animation":
                    # Animate filter properties
                    for filter_id in results["filters"]:
                        if "attribute" in params and "values" in params:
                            # Find the filter element
                            js_code = f"""
                            (function() {{
                                var filter = document.getElementById('{filter_id}');
                                if (!filter) return null;
                                
                                // Find the specific filter effect element (feGaussianBlur, feOffset, etc.)
                                var effect = filter.querySelector('{params.get("effect_type", "feGaussianBlur")}');
                                if (!effect) return null;
                                
                                return effect.id || '{filter_id}_effect';
                            }})();
                            """
                            
                            try:
                                effect_id = execute_js(js_code)
                                if effect_id:
                                    # Create an animation element for the filter effect
                                    from_value = params.get("from_value")
                                    to_value = params.get("to_value")
                                    duration = params.get("duration", 1)
                                    delay = params.get("delay", 0)
                                    easing = params.get("easing", "easeInOutCubic")
                                    
                                    # Add animation to the sequence
                                    master_sequence.add_attribute_animation(
                                        {"id": effect_id},  # Create a pseudo-element with just an ID
                                        params["attribute"],
                                        from_value,
                                        to_value,
                                        duration,
                                        delay,
                                        easing
                                    )
                            except Exception as e:
                                print(f"Error creating filter animation: {str(e)}")
                
                elif anim_type == "mask_animation":
                    # Similar implementation for mask animations
                    pass
                
                elif anim_type == "element_animation":
                    # Direct animation of the element's properties
                    if "attribute" in params:
                        master_sequence.add_attribute_animation(
                            element,
                            params["attribute"],
                            params.get("from_value", 0),
                            params.get("to_value", 1),
                            params.get("duration", 1),
                            params.get("delay", 0),
                            params.get("easing", "easeInOutCubic")
                        )
                    elif "transform_type" in params:
                        master_sequence.add_transform_animation(
                            element,
                            params["transform_type"],
                            params.get("from_value", "0"),
                            params.get("to_value", "1"),
                            params.get("duration", 1),
                            params.get("delay", 0),
                            params.get("easing", "easeInOutCubic")
                        )
            
            # Store the sequence and automatically play it if specified
            results["animations"].append(master_sequence)
            if effects_config.get("auto_play", True):
                master_sequence.play()
        
        return results
