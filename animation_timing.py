"""
Advanced Animation Timing Module for SVG Animation MCP.

This module provides sophisticated easing functions and timing utilities
inspired by Vercel's smooth, professional animations.
"""

from browser_integration import execute_js

class AnimationTiming:
    """
    Provides advanced animation timing and easing functions.
    
    Implements sophisticated easing functions similar to those used
    in professional web animations like Vercel's website.
    """
    
    @staticmethod
    def initialize(mcp):
        """
        Initialize advanced easing functions in the browser.
        
        Args:
            mcp: MCP instance
            
        Returns:
            True if successful, False otherwise
        """
        js_code = """
        window.VercelEasing = {
            // Linear (for reference)
            linear: t => t,
            
            // Sine easing
            easeInSine: t => 1 - Math.cos((t * Math.PI) / 2),
            easeOutSine: t => Math.sin((t * Math.PI) / 2),
            easeInOutSine: t => -(Math.cos(Math.PI * t) - 1) / 2,
            
            // Quad easing
            easeInQuad: t => t * t,
            easeOutQuad: t => 1 - (1 - t) * (1 - t),
            easeInOutQuad: t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
            
            // Cubic easing
            easeInCubic: t => t * t * t,
            easeOutCubic: t => 1 - Math.pow(1 - t, 3),
            easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
            
            // Quart easing
            easeInQuart: t => t * t * t * t,
            easeOutQuart: t => 1 - Math.pow(1 - t, 4),
            easeInOutQuart: t => t < 0.5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2,
            
            // Quint easing
            easeInQuint: t => t * t * t * t * t,
            easeOutQuint: t => 1 - Math.pow(1 - t, 5),
            easeInOutQuint: t => t < 0.5 ? 16 * t * t * t * t * t : 1 - Math.pow(-2 * t + 2, 5) / 2,
            
            // Expo easing - Vercel often uses these for dramatic effects
            easeInExpo: t => t === 0 ? 0 : Math.pow(2, 10 * t - 10),
            easeOutExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
            easeInOutExpo: t => t === 0 ? 0 : t === 1 ? 1 : t < 0.5 ? Math.pow(2, 20 * t - 10) / 2 : (2 - Math.pow(2, -20 * t + 10)) / 2,
            
            // Circ easing
            easeInCirc: t => 1 - Math.sqrt(1 - Math.pow(t, 2)),
            easeOutCirc: t => Math.sqrt(1 - Math.pow(t - 1, 2)),
            easeInOutCirc: t => t < 0.5 ? (1 - Math.sqrt(1 - Math.pow(2 * t, 2))) / 2 : (Math.sqrt(1 - Math.pow(-2 * t + 2, 2)) + 1) / 2,
            
            // Back easing - great for subtle overshoots
            easeInBack: t => {
                const c1 = 1.70158;
                const c3 = c1 + 1;
                return c3 * t * t * t - c1 * t * t;
            },
            easeOutBack: t => {
                const c1 = 1.70158;
                const c3 = c1 + 1;
                return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
            },
            easeInOutBack: t => {
                const c1 = 1.70158;
                const c2 = c1 * 1.525;
                return t < 0.5
                    ? (Math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
                    : (Math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2;
            },
            
            // Elastic easing
            easeInElastic: t => {
                const c4 = (2 * Math.PI) / 3;
                return t === 0 ? 0 : t === 1 ? 1 : -Math.pow(2, 10 * t - 10) * Math.sin((t * 10 - 10.75) * c4);
            },
            easeOutElastic: t => {
                const c4 = (2 * Math.PI) / 3;
                return t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
            },
            easeInOutElastic: t => {
                const c5 = (2 * Math.PI) / 4.5;
                return t === 0 ? 0 : t === 1 ? 1 : t < 0.5
                    ? -(Math.pow(2, 20 * t - 10) * Math.sin((20 * t - 11.125) * c5)) / 2
                    : (Math.pow(2, -20 * t + 10) * Math.sin((20 * t - 11.125) * c5)) / 2 + 1;
            },
            
            // Bounce easing
            easeInBounce: t => 1 - window.VercelEasing.easeOutBounce(1 - t),
            easeOutBounce: t => {
                const n1 = 7.5625;
                const d1 = 2.75;
                
                if (t < 1 / d1) {
                    return n1 * t * t;
                } else if (t < 2 / d1) {
                    return n1 * (t -= 1.5 / d1) * t + 0.75;
                } else if (t < 2.5 / d1) {
                    return n1 * (t -= 2.25 / d1) * t + 0.9375;
                } else {
                    return n1 * (t -= 2.625 / d1) * t + 0.984375;
                }
            },
            easeInOutBounce: t => t < 0.5
                ? (1 - window.VercelEasing.easeOutBounce(1 - 2 * t)) / 2
                : (1 + window.VercelEasing.easeOutBounce(2 * t - 1)) / 2,
                
            // Vercel-specific custom easings
            // Subtle entrance animation, similar to how Vercel components appear
            vercelEntrance: t => {
                // Combines slight elastic with expo easing for that refined Vercel feel
                return t === 0 ? 0 : t === 1 ? 1 : 
                     Math.pow(2, -8 * t) * Math.sin((t - 0.1) * 6 * Math.PI) + 1 - Math.pow(1.6, -10 * t);
            },
            
            // Subtle UI response, similar to Vercel hover effects
            vercelResponse: t => {
                // Combines a quick start and a subtle overshoot
                return t < 0.6 
                    ? 4 * t * t * t 
                    : 1 + (t - 1) * (2 * (t - 1)) * (2.5 * (t - 1));
            }
        };
        
        // Register SVG SMIL animation easings if not using CSS animations
        if (!window.customSMILeasing) {
            window.customSMILeasing = true;
            
            // Function to convert our easing functions to discrete steps for SMIL
            window.createSMILEasingValues = function(easingFn, steps = 60) {
                let values = [];
                let keyTimes = [];
                
                for (let i = 0; i <= steps; i++) {
                    const t = i / steps;
                    const y = easingFn(t);
                    values.push(y);
                    keyTimes.push(t);
                }
                
                return {
                    values: values.join(';'),
                    keyTimes: keyTimes.join(';')
                };
            };
        }
        """
        
        try:
            execute_js(js_code)
            return True
        except Exception as e:
            print(f"Error initializing animation timing: {str(e)}")
            return False
    
    @staticmethod
    def get_easing_values(easing_name, steps=20):
        """
        Get discrete values for a SMIL animation with the specified easing.
        
        Args:
            easing_name: Name of the easing function
            steps: Number of steps to generate
            
        Returns:
            Dictionary with 'values' and 'keyTimes' strings for SVG animation
        """
        js_code = f"""
        (function() {{
            if (window.VercelEasing && window.VercelEasing['{easing_name}']) {{
                return window.createSMILEasingValues(window.VercelEasing['{easing_name}'], {steps});
            }}
            return null;
        }})();
        """
        
        try:
            result = execute_js(js_code)
            if result:
                return result
            else:
                print(f"Warning: Easing function '{easing_name}' not found. Using 'linear' instead.")
                # Return linear easing as fallback
                values = ";".join([str(i/steps) for i in range(steps+1)])
                key_times = ";".join([str(i/steps) for i in range(steps+1)])
                return {"values": values, "keyTimes": key_times}
        except Exception as e:
            print(f"Error getting easing values: {str(e)}")
            return None
    
    @staticmethod
    def apply_easing_to_animation(animation_element, easing_name):
        """
        Apply an easing function to an existing animation element.
        
        Args:
            animation_element: The SVG animation element (animate or animateTransform)
            easing_name: Name of the easing function to apply
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get easing values
            easing_values = AnimationTiming.get_easing_values(easing_name)
            if not easing_values:
                return False
            
            # Apply easing to animation element
            js_code = f"""
            (function() {{
                var element = document.getElementById('{animation_element.id}');
                if (!element) return false;
                
                // Apply easing values and key times
                element.setAttribute('values', '{easing_values["values"]}');
                element.setAttribute('keyTimes', '{easing_values["keyTimes"]}');
                return true;
            }})();
            """
            
            result = execute_js(js_code)
            return result
        except Exception as e:
            print(f"Error applying easing to animation: {str(e)}")
            return False


class AnimationDelay:
    """Utilities for precise timing and delays with animation sequences."""
    
    @staticmethod
    def staggered_delay(base_delay, index, stagger_amount=0.1):
        """
        Calculate a staggered delay for sequential animations.
        
        Args:
            base_delay: Base delay in seconds
            index: Index of the item in sequence
            stagger_amount: Amount to stagger each item by
            
        Returns:
            Total delay in seconds
        """
        return base_delay + (index * stagger_amount)
    
    @staticmethod
    def delayed_execution(mcp, code, delay_seconds):
        """
        Execute code after a specific delay.
        
        Args:
            mcp: MCP instance
            code: JavaScript code to execute
            delay_seconds: Delay in seconds
            
        Returns:
            ID of the timeout (can be used to cancel)
        """
        js_code = f"""
        (function() {{
            var timeoutId = setTimeout(function() {{
                {code}
            }}, {delay_seconds * 1000});
            return timeoutId;
        }})();
        """
        
        return execute_js(js_code)
    
    @staticmethod
    def cancel_delayed_execution(timeout_id):
        """
        Cancel a delayed execution.
        
        Args:
            timeout_id: ID of the timeout to cancel
            
        Returns:
            True if successful, False otherwise
        """
        js_code = f"""
        (function() {{
            clearTimeout({timeout_id});
            return true;
        }})();
        """
        
        return execute_js(js_code)


def apply_vercel_entrance(element, duration=0.8, delay=0):
    """
    Apply a Vercel-inspired entrance animation to an element.
    
    Args:
        element: The SVG element to animate
        duration: Animation duration in seconds
        delay: Delay before animation starts in seconds
        
    Returns:
        Dictionary of animation objects
    """
    # Set initial state
    element.set_attribute("opacity", "0")
    element.set_attribute("transform", "scale(0.97)")
    
    # Create animations
    opacity_anim = element.animate("opacity", from_value=0, to_value=1, 
                                 duration=duration, begin=f"{delay}s")
    
    scale_anim = element.animate_transform("scale", from_value="0.97", to_value="1", 
                                        duration=duration, begin=f"{delay}s")
    
    # Apply Vercel's signature easing
    AnimationTiming.apply_easing_to_animation(opacity_anim, "easeOutExpo")
    AnimationTiming.apply_easing_to_animation(scale_anim, "vercelEntrance")
    
    return {
        "opacity": opacity_anim,
        "scale": scale_anim
    }


def apply_vercel_exit(element, duration=0.5, delay=0):
    """
    Apply a Vercel-inspired exit animation to an element.
    
    Args:
        element: The SVG element to animate
        duration: Animation duration in seconds
        delay: Delay before animation starts in seconds
        
    Returns:
        Dictionary of animation objects
    """
    # Create animations
    opacity_anim = element.animate("opacity", from_value=1, to_value=0, 
                                 duration=duration, begin=f"{delay}s", fill="freeze")
    
    scale_anim = element.animate_transform("scale", from_value="1", to_value="0.95", 
                                        duration=duration, begin=f"{delay}s", fill="freeze")
    
    # Apply Vercel's signature easing
    AnimationTiming.apply_easing_to_animation(opacity_anim, "easeInCubic")
    AnimationTiming.apply_easing_to_animation(scale_anim, "easeInCubic")
    
    return {
        "opacity": opacity_anim,
        "scale": scale_anim
    }


def apply_vercel_hover(element, scale=1.02, duration=0.2):
    """
    Apply a Vercel-inspired hover effect to an element.
    
    Args:
        element: The SVG element to apply hover effect to
        scale: Maximum scale factor on hover
        duration: Animation duration in seconds
        
    Returns:
        True if successful, False otherwise
    """
    js_code = f"""
    (function() {{
        var element = document.getElementById('{element.id}');
        if (!element) return false;
        
        var originalTransform = element.getAttribute('transform') || '';
        
        // Add hover effect
        element.addEventListener('mouseenter', function() {{
            if (window.VercelEasing) {{
                element.style.transition = 'transform {duration}s';
                element.style.transform = 'scale({scale})';
                element.style.transitionTimingFunction = 'cubic-bezier(0.2, 0, 0, 1)';
            }}
        }});
        
        element.addEventListener('mouseleave', function() {{
            if (window.VercelEasing) {{
                element.style.transition = 'transform {duration}s';
                element.style.transform = 'scale(1)';
                element.style.transitionTimingFunction = 'cubic-bezier(0.2, 0, 0, 1)';
            }}
        }});
        
        return true;
    }})();
    """
    
    return execute_js(js_code) 