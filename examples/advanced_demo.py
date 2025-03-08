"""
Advanced Demo for SVG Animation MCP.

This demo showcases the advanced features of the SVG Animation MCP, including:
- AI-powered animation suggestions
- Physics engine for realistic animations
- Shape morphing for smooth transitions
- Interactive settings UI
"""

import time
from src.mcp.svg_animation_mcp import MCP
from src.mcp.browser_integration import init_browser_environment, clear_svg_animations, execute_js
from src.mcp.utils import generate_star_points, generate_path_data
from src.mcp.ai_suggestions import generate_animation_from_text
from src.mcp.physics_engine import initialize_physics_animation
from src.mcp.shape_morphing import morph_element
from src.mcp.animation_settings_ui import create_settings_ui, show_settings_ui

def demo_ai_suggestions():
    """
    Demonstrate AI-powered animation suggestions.
    """
    print("Running AI Suggestions demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Add a title
    title = svg.add_text(x=400, y=50, text="AI Suggestions Demo", 
                      fill="#333", font_size="24px", text_anchor="middle", font_family="Arial")
    
    # Demonstrate AI-generated animations from text descriptions
    descriptions = [
        "Create a red circle that pulses in the top left",
        "Create a blue square that moves from left to right",
        "Create a green star that spins in the center",
        "Create a purple text saying 'Hello World' that fades in and out"
    ]
    
    # Add text description for each animation
    for i, description in enumerate(descriptions):
        y_pos = 120 + i * 120
        text = svg.add_text(x=400, y=y_pos - 40, text=f'"{description}"', 
                          fill="#666", font_size="14px", text_anchor="middle", font_family="Arial")
        
        # Use AI to generate an animation based on the description
        result = generate_animation_from_text(description)
        
        if result['status'] == 'success':
            print(f"Generated animation for: {description}")
        else:
            print(f"Failed to generate animation: {result['message']}")
    
    print("AI Suggestions demo running. Check the browser window.")


def demo_physics_engine():
    """
    Demonstrate physics engine capabilities.
    """
    print("Running Physics Engine demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Add a title
    title = svg.add_text(x=400, y=50, text="Physics Engine Demo", 
                      fill="#333", font_size="24px", text_anchor="middle", font_family="Arial")
    
    # Initialize physics animation
    engine = initialize_physics_animation(svg, mcp)
    
    # Add event handling for mouse interactions
    js_code = """
    var svg = document.querySelector('svg');
    svg.addEventListener('click', function(e) {
        var rect = svg.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        console.log('EXPLOSION:' + x + ',' + y);
    });
    """
    mcp.execute_js(js_code)
    
    # Start the physics simulation
    engine.start()
    
    # This would normally be handled by the BrowserTools MCP event loop
    # For this demo, we'll simulate explosion events manually
    explosion_positions = [(200, 300), (400, 200), (600, 300)]
    
    print("Physics Engine demo running. Check the browser window.")
    print("Simulating explosions...")
    
    # Simulate explosions
    for pos in explosion_positions:
        print(f"Explosion at {pos}")
        engine.apply_explosion_force(pos, 1000, 200)
        time.sleep(1)
    
    # In a real application, the engine would be updated continuously
    # and react to actual user clicks


def demo_shape_morphing():
    """
    Demonstrate shape morphing capabilities.
    """
    print("Running Shape Morphing demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Add a title
    title = svg.add_text(x=400, y=50, text="Shape Morphing Demo", 
                      fill="#333", font_size="24px", text_anchor="middle", font_family="Arial")
    
    # Create shapes for morphing demonstration
    # First row: Basic shapes (circle, square, star)
    circle = svg.add_circle(cx=200, cy=150, r=50, fill="#ff5252", id="morph_circle")
    square = svg.add_rectangle(x=350, y=100, width=100, height=100, fill="#4caf50", id="morph_square")
    
    # Create a star using path
    star_points = generate_star_points(cx=600, cy=150, outer_radius=50, inner_radius=25, points=5)
    star_path = generate_path_data(star_points) + " Z"
    star = svg.add_path(d=star_path, fill="#2196f3", id="morph_star")
    
    # Second row: Complex shapes
    heart_path = "M400,350 C400,330 380,310 350,310 C320,310 300,330 300,360 C300,380 320,400 400,450 C480,400 500,380 500,360 C500,330 480,310 450,310 C420,310 400,330 400,350 Z"
    heart = svg.add_path(d=heart_path, fill="#e91e63", id="morph_heart")
    
    # Add buttons to trigger morphs
    button_style = """
    .morph-button {
        fill: #fff;
        stroke: #333;
        stroke-width: 1;
        cursor: pointer;
    }
    .morph-button-text {
        font-family: Arial;
        font-size: 12px;
        pointer-events: none;
        user-select: none;
    }
    .morph-button:hover {
        fill: #f0f0f0;
    }
    """
    
    js_code = f"""
    // Add CSS styles
    var style = document.createElement('style');
    style.textContent = `{button_style}`;
    document.head.appendChild(style);
    
    // Function to create morph button
    function createMorphButton(x, y, width, height, text, sourceId, targetId) {{
        var svg = document.querySelector('svg');
        
        // Create button group
        var group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        
        // Create button rectangle
        var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', x);
        rect.setAttribute('y', y);
        rect.setAttribute('width', width);
        rect.setAttribute('height', height);
        rect.setAttribute('rx', '5');
        rect.setAttribute('class', 'morph-button');
        rect.setAttribute('data-source', sourceId);
        rect.setAttribute('data-target', targetId);
        
        // Create button text
        var textElem = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        textElem.setAttribute('x', x + width/2);
        textElem.setAttribute('y', y + height/2 + 4);
        textElem.setAttribute('text-anchor', 'middle');
        textElem.setAttribute('class', 'morph-button-text');
        textElem.textContent = text;
        
        // Add click handler
        rect.addEventListener('click', function() {{
            var source = this.getAttribute('data-source');
            var target = this.getAttribute('data-target');
            console.log('MORPH:' + source + ':' + target);
        }});
        
        // Add elements to group
        group.appendChild(rect);
        group.appendChild(textElem);
        
        // Add group to SVG
        svg.appendChild(group);
    }}
    
    // Create buttons for first row morphs
    createMorphButton(150, 200, 100, 30, "Circle → Square", "morph_circle", "morph_square");
    createMorphButton(350, 200, 100, 30, "Square → Star", "morph_square", "morph_star");
    createMorphButton(550, 200, 100, 30, "Star → Circle", "morph_star", "morph_circle");
    
    // Create buttons for second row morphs
    createMorphButton(300, 400, 100, 30, "Heart → Circle", "morph_heart", "morph_circle");
    createMorphButton(450, 400, 100, 30, "Circle → Heart", "morph_circle", "morph_heart");
    """
    
    mcp.execute_js(js_code)
    
    # In a real application, we would handle the morphing based on button clicks
    # For this demo, we'll trigger some morphs automatically
    print("Shape Morphing demo running. Check the browser window.")
    print("Automatically triggering morphs...")
    
    # Simulate clicks on morph buttons
    morphs = [
        ("morph_circle", "morph_square"),
        ("morph_square", "morph_star"),
        ("morph_star", "morph_circle"),
        ("morph_circle", "morph_heart"),
        ("morph_heart", "morph_circle")
    ]
    
    # Perform each morph with a delay between them
    for source_id, target_id in morphs:
        print(f"Morphing {source_id} to {target_id}...")
        morph_element(source_id, target_id, duration=2, mcp=mcp)
        time.sleep(3)  # Wait for morph to complete


def demo_settings_ui():
    """
    Demonstrate interactive settings UI.
    """
    print("Running Settings UI demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Add a title
    title = svg.add_text(x=400, y=50, text="Settings UI Demo", 
                      fill="#333", font_size="24px", text_anchor="middle", font_family="Arial")
    
    # Create some shapes with animations to edit
    circle = svg.add_circle(cx=200, cy=200, r=50, fill="#ff5252", id="settings_circle")
    circle.animate("r", from_value=50, to_value=80, duration=2, repeat_count="indefinite")
    
    rect = svg.add_rectangle(x=350, y=150, width=100, height=100, fill="#4caf50", id="settings_rect")
    rect.animate_transform("rotate", from_value="0 400 200", to_value="360 400 200", 
                         duration=3, repeat_count="indefinite")
    
    star_points = generate_star_points(cx=600, cy=200, outer_radius=50, inner_radius=25, points=5)
    star_path = generate_path_data(star_points) + " Z"
    star = svg.add_path(d=star_path, fill="#2196f3", id="settings_star")
    star.animate("fill", from_value="#2196f3", to_value="#ff9800", 
               duration=2, repeat_count="indefinite")
    
    # Add instructions
    instructions = svg.add_text(x=400, y=350, text="Click on a shape, then use the settings panel to adjust it", 
                             fill="#666", font_size="16px", text_anchor="middle", font_family="Arial")
    
    # Add button to toggle settings UI
    button_rect = svg.add_rectangle(x=350, y=400, width=200, height=40, 
                                  fill="#2196f3", rx=5, ry=5, id="toggle_settings_button")
    button_text = svg.add_text(x=450, y=425, text="Toggle Settings Panel", 
                            fill="white", font_size="16px", text_anchor="middle", 
                            font_family="Arial", pointer_events="none")
    
    # Make elements selectable
    js_code = """
    // Add click handler for shapes
    var shapes = document.querySelectorAll('circle, rect, path');
    for (var i = 0; i < shapes.length; i++) {
        var shape = shapes[i];
        if (shape.id && shape.id.startsWith('settings_')) {
            shape.style.cursor = 'pointer';
            shape.addEventListener('click', function(e) {
                e.stopPropagation();
                console.log('SELECT_ELEMENT:' + this.id);
            });
        }
    }
    
    // Add click handler for settings toggle button
    var toggleButton = document.getElementById('toggle_settings_button');
    if (toggleButton) {
        toggleButton.style.cursor = 'pointer';
        toggleButton.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log('TOGGLE_SETTINGS');
        });
    }
    """
    
    mcp.execute_js(js_code)
    
    # Create and show the settings UI
    ui = create_settings_ui(mcp)
    show_settings_ui(ui)
    
    # In a real application, we would handle element selection and settings changes
    print("Settings UI demo running. Check the browser window.")
    print("The settings panel should be visible. Try selecting different elements.")


def combine_all_features():
    """
    Demonstrate all advanced features combined.
    """
    print("Running Combined Features demo...")
    
    # Initialize browser environment
    init_browser_environment()
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=800, height=600, parent_selector="#animation-container")
    
    # Add a title
    title = svg.add_text(x=400, y=50, text="Combined Features Demo", 
                      fill="#333", font_size="24px", text_anchor="middle", font_family="Arial")
    
    # Section headers
    ai_header = svg.add_text(x=200, y=100, text="AI Suggestions", 
                          fill="#666", font_size="18px", text_anchor="middle", font_family="Arial")
    
    physics_header = svg.add_text(x=600, y=100, text="Physics Engine", 
                               fill="#666", font_size="18px", text_anchor="middle", font_family="Arial")
    
    morph_header = svg.add_text(x=200, y=350, text="Shape Morphing", 
                             fill="#666", font_size="18px", text_anchor="middle", font_family="Arial")
    
    settings_header = svg.add_text(x=600, y=350, text="Settings UI", 
                                fill="#666", font_size="18px", text_anchor="middle", font_family="Arial")
    
    # 1. AI Suggestions - Add a field to enter text and generate animations
    ai_text = svg.add_text(x=200, y=130, text="Enter text prompt below:", 
                        fill="#666", font_size="14px", text_anchor="middle", font_family="Arial")
    
    # Add a simulation of an input field
    ai_input = svg.add_rectangle(x=100, y=140, width=200, height=30, fill="white", 
                              stroke="#ccc", rx=5, ry=5, id="ai_input_field")
    ai_input_text = svg.add_text(x=110, y=160, text="a red circle that pulses", 
                              fill="#333", font_size="14px", text_anchor="start", font_family="Arial", id="ai_input_text")
    
    ai_button = svg.add_rectangle(x=150, y=180, width=100, height=30, fill="#2196f3", 
                               rx=5, ry=5, id="ai_generate_button")
    ai_button_text = svg.add_text(x=200, y=200, text="Generate", 
                               fill="white", font_size="14px", text_anchor="middle", font_family="Arial")
    
    # 2. Physics Engine - Add a simple physics simulation
    # Initialize a smaller physics simulation
    mcp.execute_js("""
    // Create a container for the physics demo
    var svg = document.querySelector('svg');
    var physicsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    physicsGroup.setAttribute('id', 'physics_container');
    physicsGroup.setAttribute('transform', 'translate(500, 130)');
    svg.appendChild(physicsGroup);
    """)
    
    # Create a sub-SVG for physics (don't actually create a new SVG element)
    class SubSVG:
        def __init__(self, mcp, parent_id):
            self.mcp = mcp
            self.id = parent_id
            
        def add_rectangle(self, x, y, width, height, **kwargs):
            element_id = kwargs.get('id', f"rect_{int(time.time() * 1000)}")
            js_code = f"""
            var parent = document.getElementById('{self.id}');
            var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('id', '{element_id}');
            rect.setAttribute('x', '{x}');
            rect.setAttribute('y', '{y}');
            rect.setAttribute('width', '{width}');
            rect.setAttribute('height', '{height}');
            """
            
            for attr, value in kwargs.items():
                if attr != 'id':
                    js_code += f"rect.setAttribute('{attr}', '{value}');"
            
            js_code += "parent.appendChild(rect);"
            execute_js(js_code)
            
            from src.mcp.svg_animation_mcp import Rectangle
            rect_obj = Rectangle(self.mcp, element_id)
            return rect_obj
            
        def add_circle(self, cx, cy, r, **kwargs):
            element_id = kwargs.get('id', f"circle_{int(time.time() * 1000)}")
            js_code = f"""
            var parent = document.getElementById('{self.id}');
            var circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('id', '{element_id}');
            circle.setAttribute('cx', '{cx}');
            circle.setAttribute('cy', '{cy}');
            circle.setAttribute('r', '{r}');
            """
            
            for attr, value in kwargs.items():
                if attr != 'id':
                    js_code += f"circle.setAttribute('{attr}', '{value}');"
            
            js_code += "parent.appendChild(circle);"
            execute_js(js_code)
            
            from src.mcp.svg_animation_mcp import Circle
            circle_obj = Circle(self.mcp, element_id)
            return circle_obj
    
    physics_svg = SubSVG(mcp, "physics_container")
    physics_engine = initialize_physics_animation(physics_svg, mcp)
    
    # 3. Shape Morphing - Add shapes that can be morphed
    source_shape = svg.add_circle(cx=150, cy=400, r=40, fill="#e91e63", id="source_shape")
    target_shape = svg.add_rectangle(x=230, y=380, width=80, height=80, fill="#9c27b0", id="target_shape")
    
    morph_button = svg.add_rectangle(x=150, y=450, width=100, height=30, fill="#2196f3", 
                                  rx=5, ry=5, id="morph_button")
    morph_button_text = svg.add_text(x=200, y=470, text="Morph Shapes", 
                                  fill="white", font_size="14px", text_anchor="middle", font_family="Arial")
    
    # 4. Settings UI - Add a button to toggle settings
    settings_button = svg.add_rectangle(x=550, y=380, width=100, height=30, fill="#2196f3", 
                                     rx=5, ry=5, id="settings_button")
    settings_button_text = svg.add_text(x=600, y=400, text="Show Settings", 
                                     fill="white", font_size="14px", text_anchor="middle", font_family="Arial")
    
    # Create a shape to edit with settings
    editable_shape = svg.add_circle(cx=600, cy=450, r=40, fill="#ff9800", id="editable_shape")
    editable_shape.animate("r", from_value=40, to_value=60, duration=2, repeat_count="indefinite")
    
    # Create the settings UI but don't show it yet
    ui = create_settings_ui(mcp)
    
    # Add interactivity
    js_code = """
    // AI Button
    var aiButton = document.getElementById('ai_generate_button');
    if (aiButton) {
        aiButton.style.cursor = 'pointer';
        aiButton.addEventListener('click', function() {
            var inputText = document.getElementById('ai_input_text');
            if (inputText) {
                console.log('AI_GENERATE:' + inputText.textContent);
            }
        });
    }
    
    // Physics interactivity
    var physicsContainer = document.getElementById('physics_container');
    if (physicsContainer) {
        physicsContainer.addEventListener('click', function(e) {
            var rect = this.getBoundingClientRect();
            var svgRect = document.querySelector('svg').getBoundingClientRect();
            var x = e.clientX - svgRect.left - 500;
            var y = e.clientY - svgRect.top - 130;
            console.log('PHYSICS_CLICK:' + x + ',' + y);
        });
    }
    
    // Morph button
    var morphButton = document.getElementById('morph_button');
    if (morphButton) {
        morphButton.style.cursor = 'pointer';
        morphButton.addEventListener('click', function() {
            console.log('MORPH_SHAPES');
        });
    }
    
    // Settings button
    var settingsButton = document.getElementById('settings_button');
    if (settingsButton) {
        settingsButton.style.cursor = 'pointer';
        settingsButton.addEventListener('click', function() {
            console.log('TOGGLE_SETTINGS');
        });
    }
    
    // Make editable shape clickable
    var editableShape = document.getElementById('editable_shape');
    if (editableShape) {
        editableShape.style.cursor = 'pointer';
        editableShape.addEventListener('click', function() {
            console.log('SELECT_ELEMENT:' + this.id);
        });
    }
    """
    
    mcp.execute_js(js_code)
    
    print("Combined Features demo running. Check the browser window.")
    print("You can interact with each of the four feature demos.")
    
    # Simulate some interactions for the demo
    print("Simulating interactions...")
    
    # 1. AI suggestion
    print("Generating animation from text...")
    generate_animation_from_text("a red circle that pulses")
    
    # 2. Physics click
    print("Triggering physics explosion...")
    physics_engine.apply_explosion_force((0, 0), 500, 100)
    
    # 3. Shape morphing
    print("Morphing shapes...")
    morph_element("source_shape", "target_shape", duration=2, mcp=mcp)
    
    # 4. Settings UI
    print("Showing settings UI...")
    show_settings_ui(ui)
    ui.select_element("editable_shape")


def main():
    """
    Run demonstrations of advanced features.
    """
    print("SVG Animation MCP Advanced Demos")
    print("================================")
    
    while True:
        print("\nChoose a demo to run:")
        print("1. AI Suggestions")
        print("2. Physics Engine")
        print("3. Shape Morphing")
        print("4. Settings UI")
        print("5. Combined Features")
        print("6. Run All Demos")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ")
        
        if choice == "1":
            clear_svg_animations()
            demo_ai_suggestions()
        elif choice == "2":
            clear_svg_animations()
            demo_physics_engine()
        elif choice == "3":
            clear_svg_animations()
            demo_shape_morphing()
        elif choice == "4":
            clear_svg_animations()
            demo_settings_ui()
        elif choice == "5":
            clear_svg_animations()
            combine_all_features()
        elif choice == "6":
            print("\nRunning all demos in sequence...")
            clear_svg_animations()
            demo_ai_suggestions()
            input("\nPress Enter for next demo...")
            
            clear_svg_animations()
            demo_physics_engine()
            input("\nPress Enter for next demo...")
            
            clear_svg_animations()
            demo_shape_morphing()
            input("\nPress Enter for next demo...")
            
            clear_svg_animations()
            demo_settings_ui()
            input("\nPress Enter for next demo...")
            
            clear_svg_animations()
            combine_all_features()
        elif choice == "0":
            print("Exiting demo.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        if choice not in ["0", "6"]:
            input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main() 