"""
Demo script for SVG Animation MCP.

This script demonstrates the usage of SVG Animation MCP
by creating various SVG animations.
"""

from src.mcp.svg_animation_mcp import MCP
from src.mcp.browser_integration import init_browser_environment, clear_svg_animations
from src.mcp.utils import generate_star_points, generate_polygon_points, generate_path_data

def demo_simple_shapes():
    """
    Demonstrate simple shape animations.
    """
    print("Running simple shapes demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=600, height=400, parent_selector="#animation-container")
    
    # Add a rectangle that moves horizontally
    rect = svg.add_rectangle(x=50, y=50, width=100, height=80, fill="red", stroke="black", stroke_width=2)
    rect.animate_transform("translate", from_value=(0, 0), to_value=(400, 0), duration=3)
    
    # Add a circle that changes size
    circle = svg.add_circle(cx=300, cy=200, r=50, fill="blue", stroke="black", stroke_width=2)
    circle.animate("r", from_value=50, to_value=100, duration=2, repeat_count="indefinite")
    
    # Add text that changes color
    text = svg.add_text(x=300, y=300, text="SVG Animation MCP", fill="purple", 
                       font_size="24px", text_anchor="middle")
    text.animate("fill", from_value="purple", to_value="orange", duration=1.5, repeat_count="indefinite")
    
    print("Simple shapes demo running. Check the browser window.")


def demo_path_animations():
    """
    Demonstrate path-based animations.
    """
    print("Running path animations demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=600, height=400, parent_selector="#animation-container")
    
    # Create a star shape using path
    star_points = generate_star_points(cx=300, cy=200, outer_radius=100, inner_radius=50, points=5)
    star_path_data = generate_path_data(star_points) + " Z"  # Z closes the path
    
    star = svg.add_path(d=star_path_data, fill="gold", stroke="orange", stroke_width=2)
    
    # Animate the star rotation
    star.animate_transform("rotate", from_value="0 300 200", to_value="360 300 200", 
                          duration=5, repeat_count="indefinite")
    
    # Add a pulsing circle in the center
    circle = svg.add_circle(cx=300, cy=200, r=20, fill="red")
    circle.animate("r", from_value=20, to_value=30, duration=1, repeat_count="indefinite")
    circle.animate("fill", from_value="red", to_value="yellow", duration=1, repeat_count="indefinite")
    
    print("Path animations demo running. Check the browser window.")


def demo_complex_animation():
    """
    Demonstrate a more complex animation with multiple elements.
    """
    print("Running complex animation demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Background
    svg.add_rectangle(x=0, y=0, width=800, height=600, fill="#f0f8ff")
    
    # Create multiple polygons that rotate
    colors = ["#ff7f50", "#9370db", "#3cb371", "#ff6347", "#4682b4"]
    for i in range(5):
        points = generate_polygon_points(cx=400, cy=300, radius=100 + i*30, sides=i+3)
        path_data = generate_path_data(points) + " Z"
        shape = svg.add_path(d=path_data, fill="none", stroke=colors[i], stroke_width=2)
        shape.animate_transform("rotate", 
                               from_value=f"0 400 300", 
                               to_value=f"{360 * (1 if i % 2 == 0 else -1)} 400 300", 
                               duration=10 / (i+1),
                               repeat_count="indefinite")
    
    # Add bouncing balls
    for i in range(10):
        x = 100 + i * 60
        y = 100
        circle = svg.add_circle(cx=x, cy=y, r=15, fill=colors[i % len(colors)])
        # Vertical bounce animation
        circle.animate("cy", from_value=y, to_value=500, duration=1 + i * 0.1, 
                      repeat_count="indefinite", values=f"{y};500;{y}", key_times="0;0.5;1")
    
    # Add text with animation
    text = svg.add_text(x=400, y=550, text="SVG Animation Machine Communication Protocol", 
                       fill="#333", font_size="24px", text_anchor="middle")
    text.animate("font-size", from_value="24px", to_value="28px", duration=2, repeat_count="indefinite")
    
    print("Complex animation demo running. Check the browser window.")


def demo_custom_js_animation():
    """
    Demonstrate using custom JavaScript for more advanced animations.
    """
    print("Running custom JavaScript animation demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Add a background
    svg.add_rectangle(x=0, y=0, width=800, height=600, fill="#222")
    
    # Add multiple circles for the particle effect
    for i in range(50):
        svg.add_circle(cx=400, cy=300, r=5, fill="white", id=f"particle_{i}")
    
    # Add custom JavaScript for a particle explosion effect
    custom_js = """
    // Get all particles
    var particles = [];
    for (var i = 0; i < 50; i++) {
        particles.push(document.getElementById('particle_' + i));
    }
    
    // Set random initial velocities
    var velocities = particles.map(function() {
        return {
            x: (Math.random() - 0.5) * 10,
            y: (Math.random() - 0.5) * 10
        };
    });
    
    // Animation function
    function animate() {
        for (var i = 0; i < particles.length; i++) {
            var particle = particles[i];
            var velocity = velocities[i];
            
            // Get current position
            var cx = parseFloat(particle.getAttribute('cx'));
            var cy = parseFloat(particle.getAttribute('cy'));
            
            // Update position
            cx += velocity.x;
            cy += velocity.y;
            
            // Bounce off edges
            if (cx < 0 || cx > 800) {
                velocity.x *= -0.9;
                cx = Math.max(0, Math.min(800, cx));
            }
            if (cy < 0 || cy > 600) {
                velocity.y *= -0.9;
                cy = Math.max(0, Math.min(600, cy));
            }
            
            // Apply gravity towards center
            var dx = 400 - cx;
            var dy = 300 - cy;
            var distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > 5) {
                velocity.x += dx / distance * 0.2;
                velocity.y += dy / distance * 0.2;
            }
            
            // Apply friction
            velocity.x *= 0.99;
            velocity.y *= 0.99;
            
            // Update element
            particle.setAttribute('cx', cx);
            particle.setAttribute('cy', cy);
            
            // Set color based on velocity
            var speed = Math.sqrt(velocity.x * velocity.x + velocity.y * velocity.y);
            var hue = Math.floor(speed * 15);
            particle.setAttribute('fill', 'hsl(' + hue + ', 100%, 50%)');
            particle.setAttribute('r', Math.min(10, 3 + speed));
        }
        
        requestAnimationFrame(animate);
    }
    
    // Start animation
    animate();
    """
    
    mcp.execute_js(custom_js)
    
    print("Custom JavaScript animation demo running. Check the browser window.")


def main():
    """
    Run all demos.
    """
    print("SVG Animation MCP Demo")
    print("======================")
    
    while True:
        print("\nChoose a demo to run:")
        print("1. Simple Shapes")
        print("2. Path Animations")
        print("3. Complex Animation")
        print("4. Custom JavaScript Animation")
        print("5. Run All Demos")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == "1":
            clear_svg_animations()
            demo_simple_shapes()
        elif choice == "2":
            clear_svg_animations()
            demo_path_animations()
        elif choice == "3":
            clear_svg_animations()
            demo_complex_animation()
        elif choice == "4":
            clear_svg_animations()
            demo_custom_js_animation()
        elif choice == "5":
            print("\nRunning all demos sequentially...")
            clear_svg_animations()
            demo_simple_shapes()
            input("Press Enter to continue to the next demo...")
            
            clear_svg_animations()
            demo_path_animations()
            input("Press Enter to continue to the next demo...")
            
            clear_svg_animations()
            demo_complex_animation()
            input("Press Enter to continue to the next demo...")
            
            clear_svg_animations()
            demo_custom_js_animation()
        elif choice == "0":
            print("Exiting demo.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 