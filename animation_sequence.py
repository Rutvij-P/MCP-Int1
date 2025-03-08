"""
Animation Sequence Module for SVG Animation MCP.

This module provides tools for creating precisely timed sequences of animations
similar to those found on Vercel's website, with perfect timing and coordination.
"""

from browser_integration import execute_js
from animation_timing import AnimationTiming, AnimationDelay

class AnimationSequence:
    """
    Create and manage sequences of animations with precise timing.
    
    Allows for the creation of sophisticated, coordinated animation sequences
    with staggered timing, synchronized events, and perfect coordination.
    """
    
    def __init__(self, mcp):
        """
        Initialize an animation sequence.
        
        Args:
            mcp: MCP instance
        """
        self.mcp = mcp
        self.animations = []
        self.sequence_id = f"sequence_{int(hash(self)) % 10000}"
        self.is_playing = False
        self._initialize_timing()
    
    def _initialize_timing(self):
        """Initialize animation timing in the browser."""
        AnimationTiming.initialize(self.mcp)
    
    def add(self, element, animation_type, params, delay=0, easing=None, duration=None):
        """
        Add an animation to the sequence.
        
        Args:
            element: SVG element to animate
            animation_type: Type of animation ('attribute', 'transform', or 'custom')
            params: Dictionary of animation parameters
            delay: Delay before this animation starts (in seconds)
            easing: Optional easing function name
            duration: Optional duration override (in seconds)
            
        Returns:
            Self for method chaining
        """
        # Process duration if provided
        if duration is not None:
            params['duration'] = duration
        
        # Add animation to the sequence
        self.animations.append({
            "element": element,
            "element_id": element.id,
            "type": animation_type,
            "params": params,
            "delay": delay,
            "easing": easing
        })
        
        return self
    
    def add_attribute_animation(self, element, attribute, from_value, to_value, 
                               duration=1, delay=0, easing=None, **kwargs):
        """
        Add an attribute animation to the sequence.
        
        Args:
            element: SVG element to animate
            attribute: Attribute to animate
            from_value: Starting value
            to_value: Ending value
            duration: Animation duration (in seconds)
            delay: Delay before this animation starts (in seconds)
            easing: Optional easing function name
            **kwargs: Additional animation parameters
            
        Returns:
            Self for method chaining
        """
        params = {
            "attribute": attribute,
            "from_value": from_value,
            "to_value": to_value,
            "duration": duration,
            **kwargs
        }
        
        return self.add(element, 'attribute', params, delay, easing)
    
    def add_transform_animation(self, element, transform_type, from_value, to_value, 
                               duration=1, delay=0, easing=None, **kwargs):
        """
        Add a transform animation to the sequence.
        
        Args:
            element: SVG element to animate
            transform_type: Type of transform ('translate', 'scale', 'rotate', etc.)
            from_value: Starting value
            to_value: Ending value
            duration: Animation duration (in seconds)
            delay: Delay before this animation starts (in seconds)
            easing: Optional easing function name
            **kwargs: Additional animation parameters
            
        Returns:
            Self for method chaining
        """
        params = {
            "transform_type": transform_type,
            "from_value": from_value,
            "to_value": to_value,
            "duration": duration,
            **kwargs
        }
        
        return self.add(element, 'transform', params, delay, easing)
    
    def add_custom_animation(self, element, js_code, delay=0):
        """
        Add a custom JavaScript animation to the sequence.
        
        Args:
            element: SVG element to animate
            js_code: JavaScript code for the animation
            delay: Delay before this animation starts (in seconds)
            
        Returns:
            Self for method chaining
        """
        params = {
            "code": js_code
        }
        
        return self.add(element, 'custom', params, delay)
    
    def stagger(self, elements, animation_func, base_delay=0, stagger_amount=0.05):
        """
        Add staggered animations for multiple elements.
        
        Args:
            elements: List of SVG elements
            animation_func: Function that creates animation for a single element
            base_delay: Base delay before the first animation (in seconds)
            stagger_amount: Delay between consecutive animations (in seconds)
            
        Returns:
            Self for method chaining
        """
        for i, element in enumerate(elements):
            delay = AnimationDelay.staggered_delay(base_delay, i, stagger_amount)
            animation_func(self, element, delay)
        
        return self
    
    def play(self, clear_existing=True):
        """
        Play the animation sequence.
        
        Args:
            clear_existing: Whether to clear existing animations
            
        Returns:
            Self for method chaining
        """
        if self.is_playing:
            self.stop()
        
        self.is_playing = True
        
        # Create and play each animation in the sequence
        for anim in self.animations:
            element = anim["element"]
            delay = anim["delay"]
            
            if anim["type"] == 'attribute':
                params = anim["params"].copy()
                attribute = params.pop("attribute")
                from_value = params.pop("from_value")
                to_value = params.pop("to_value")
                duration = params.pop("duration")
                
                # Add delay to begin parameter if it's not already set
                if "begin" not in params:
                    params["begin"] = f"{delay}s"
                
                # Create the animation
                animation = element.animate(attribute, from_value, to_value, duration, **params)
                
                # Apply easing if specified
                if anim["easing"]:
                    AnimationTiming.apply_easing_to_animation(animation, anim["easing"])
            
            elif anim["type"] == 'transform':
                params = anim["params"].copy()
                transform_type = params.pop("transform_type")
                from_value = params.pop("from_value")
                to_value = params.pop("to_value")
                duration = params.pop("duration")
                
                # Add delay to begin parameter if it's not already set
                if "begin" not in params:
                    params["begin"] = f"{delay}s"
                
                # Create the animation
                animation = element.animate_transform(transform_type, from_value, to_value, duration, **params)
                
                # Apply easing if specified
                if anim["easing"]:
                    AnimationTiming.apply_easing_to_animation(animation, anim["easing"])
            
            elif anim["type"] == 'custom':
                # Execute custom animation code after delay
                if delay > 0:
                    AnimationDelay.delayed_execution(self.mcp, anim["params"]["code"], delay)
                else:
                    self.mcp.execute_js(anim["params"]["code"])
        
        return self
    
    def stop(self):
        """
        Stop the animation sequence.
        
        Returns:
            Self for method chaining
        """
        if not self.is_playing:
            return self
        
        # Execute JavaScript to find and stop all animations in this sequence
        js_code = """
        (function() {
            var animations = document.querySelectorAll('animate, animateTransform');
            for (var i = 0; i < animations.length; i++) {
                var anim = animations[i];
                // Check if this animation belongs to elements in our sequence
                if (anim.parentElement) {
                    anim.beginElement(); // Force animation to start (if delayed)
                    anim.endElement(); // End the animation
                }
            }
            
            // Clear any pending timeouts
            if (window.sequenceTimeouts) {
                for (var id in window.sequenceTimeouts) {
                    clearTimeout(window.sequenceTimeouts[id]);
                }
            }
            
            return true;
        })();
        """
        
        self.mcp.execute_js(js_code)
        self.is_playing = False
        
        return self
    
    def reset(self):
        """
        Reset all animations in the sequence.
        
        Returns:
            Self for method chaining
        """
        self.stop()
        self.animations = []
        return self
    
    def reverse(self):
        """
        Create a reversed version of this sequence.
        
        Returns:
            A new AnimationSequence with reversed animations
        """
        reversed_sequence = AnimationSequence(self.mcp)
        
        # Copy animations in reverse order and swap from/to values
        for anim in reversed(self.animations):
            if anim["type"] in ['attribute', 'transform']:
                # Create a new animation with swapped from/to values
                params = anim["params"].copy()
                from_value = params["from_value"]
                to_value = params["to_value"]
                params["from_value"] = to_value
                params["to_value"] = from_value
                
                reversed_sequence.add(
                    anim["element"],
                    anim["type"],
                    params,
                    anim["delay"],
                    anim["easing"]
                )
            elif anim["type"] == 'custom':
                # Custom animations can't be easily reversed, so just add them as-is
                reversed_sequence.add(
                    anim["element"],
                    anim["type"],
                    anim["params"],
                    anim["delay"]
                )
        
        return reversed_sequence


# Pre-defined animation sequences inspired by Vercel's website

def vercel_staggered_fade_in(mcp, elements, base_delay=0, stagger_amount=0.05):
    """
    Create a Vercel-style staggered fade-in animation sequence.
    
    Args:
        mcp: MCP instance
        elements: List of SVG elements to animate
        base_delay: Base delay before the first animation (in seconds)
        stagger_amount: Delay between consecutive animations (in seconds)
        
    Returns:
        AnimationSequence instance
    """
    sequence = AnimationSequence(mcp)
    
    def create_fade_in(seq, element, delay):
        # Set initial state
        element.set_attribute("opacity", "0")
        element.set_attribute("transform", "translate(0, 15)")
        
        # Add opacity animation
        seq.add_attribute_animation(
            element, "opacity", 0, 1, 
            duration=0.6, delay=delay,
            easing="easeOutExpo"
        )
        
        # Add transform animation
        seq.add_transform_animation(
            element, "translate", "0 15", "0 0",
            duration=0.7, delay=delay,
            easing="easeOutExpo"
        )
    
    # Add staggered animations
    sequence.stagger(elements, create_fade_in, base_delay, stagger_amount)
    
    return sequence


def vercel_content_reveal(mcp, container, content_elements, direction="up", duration=0.8, delay=0):
    """
    Create a Vercel-style content reveal animation sequence.
    
    Args:
        mcp: MCP instance
        container: Container SVG element
        content_elements: List of content elements to reveal
        direction: Direction of reveal ('up', 'down', 'left', 'right')
        duration: Animation duration (in seconds)
        delay: Delay before animation starts (in seconds)
        
    Returns:
        AnimationSequence instance
    """
    sequence = AnimationSequence(mcp)
    
    # Set up initial container state
    container.set_attribute("opacity", "1")
    
    # Hide all content elements initially
    for element in content_elements:
        element.set_attribute("opacity", "0")
    
    # Define translation based on direction
    translations = {
        "up": "0 20",
        "down": "0 -20",
        "left": "20 0",
        "right": "-20 0"
    }
    
    # Default to 'up' if direction is invalid
    translation = translations.get(direction.lower(), "0 20")
    
    # Add container subtle scale animation
    sequence.add_transform_animation(
        container, "scale", "0.98", "1",
        duration=duration, delay=delay,
        easing="easeOutExpo"
    )
    
    # Add staggered content reveal
    for i, element in enumerate(content_elements):
        elem_delay = delay + 0.1 + (i * 0.05)
        
        # Add opacity animation
        sequence.add_attribute_animation(
            element, "opacity", 0, 1, 
            duration=duration * 0.8, delay=elem_delay,
            easing="easeOutExpo"
        )
        
        # Add translation animation
        sequence.add_transform_animation(
            element, "translate", translation, "0 0",
            duration=duration, delay=elem_delay,
            easing="easeOutExpo"
        )
    
    return sequence


def vercel_logo_animation(mcp, logo_element, duration=1.5, delay=0):
    """
    Create a Vercel-style logo reveal animation.
    
    Args:
        mcp: MCP instance
        logo_element: SVG element for the logo
        duration: Animation duration (in seconds)
        delay: Delay before animation starts (in seconds)
        
    Returns:
        AnimationSequence instance
    """
    sequence = AnimationSequence(mcp)
    
    # Set initial state
    logo_element.set_attribute("opacity", "0")
    logo_element.set_attribute("transform", "scale(0.8)")
    
    # Add subtle shadow effect with JavaScript
    shadow_js = f"""
    (function() {{
        var element = document.getElementById('{logo_element.id}');
        if (!element) return;
        
        // Create a filter for the subtle shadow
        var svg = element.closest('svg');
        if (!svg) return;
        
        // Check if filter already exists
        var filterId = 'vercel_logo_shadow';
        if (!document.getElementById(filterId)) {{
            var defs = svg.querySelector('defs');
            if (!defs) {{
                defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
                svg.appendChild(defs);
            }}
            
            var filter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
            filter.setAttribute('id', filterId);
            filter.setAttribute('x', '-20%');
            filter.setAttribute('y', '-20%');
            filter.setAttribute('width', '140%');
            filter.setAttribute('height', '140%');
            
            var feDropShadow = document.createElementNS('http://www.w3.org/2000/svg', 'feDropShadow');
            feDropShadow.setAttribute('dx', '0');
            feDropShadow.setAttribute('dy', '2');
            feDropShadow.setAttribute('stdDeviation', '4');
            feDropShadow.setAttribute('flood-color', 'rgba(0,0,0,0.15)');
            feDropShadow.setAttribute('flood-opacity', '0.5');
            
            filter.appendChild(feDropShadow);
            defs.appendChild(filter);
        }}
        
        // Apply filter to logo
        element.setAttribute('filter', 'url(#' + filterId + ')');
    }})();
    """
    
    # Add custom shadow setup
    sequence.add_custom_animation(logo_element, shadow_js, delay)
    
    # Opacity animation
    sequence.add_attribute_animation(
        logo_element, "opacity", 0, 1,
        duration=duration * 0.8, delay=delay + 0.1,
        easing="easeOutExpo"
    )
    
    # Scale animation with slight bounce (Vercel-style)
    sequence.add_transform_animation(
        logo_element, "scale", "0.8", "1",
        duration=duration, delay=delay + 0.1,
        easing="vercelEntrance"
    )
    
    return sequence 