"""
Physics Engine for SVG Animation MCP.

This module provides a simple physics engine for adding realistic
physical behaviors to SVG elements.
"""

import math
import time
from browser_integration import execute_js

class PhysicsBody:
    """
    Represents a physical body in the physics simulation.
    
    Maps to an SVG element and applies physics calculations to update its position.
    """
    
    def __init__(self, element_id, mass=1.0, position=(0, 0), velocity=(0, 0), 
                 acceleration=(0, 0), restitution=0.8, friction=0.1):
        """
        Initialize a physics body.
        
        Args:
            element_id: ID of the SVG element
            mass: Mass of the body (affects force calculations)
            position: Initial (x, y) position
            velocity: Initial (vx, vy) velocity
            acceleration: Initial (ax, ay) acceleration
            restitution: Bounciness (0-1)
            friction: Friction coefficient (0-1)
        """
        self.element_id = element_id
        self.mass = mass
        self.position = list(position)
        self.velocity = list(velocity)
        self.acceleration = list(acceleration)
        self.forces = [0, 0]
        self.restitution = restitution
        self.friction = friction
        self.fixed = False  # If True, position is fixed (immovable)
        self.shape_type = "circle"  # Default shape type
        self.radius = 10  # Default radius for circle collision detection
        self.width = 20  # Default width for rectangle collision detection
        self.height = 20  # Default height for rectangle collision detection
        self.in_collision = False
    
    def apply_force(self, force):
        """
        Apply a force to the body.
        
        Args:
            force: (fx, fy) force vector
        """
        if not self.fixed:
            self.forces[0] += force[0]
            self.forces[1] += force[1]
    
    def set_fixed(self, fixed=True):
        """
        Set whether the body's position is fixed.
        
        Args:
            fixed: If True, the body won't move regardless of forces
        """
        self.fixed = fixed
    
    def update(self, dt):
        """
        Update the physics body's state for a time step.
        
        Args:
            dt: Time step in seconds
        """
        if self.fixed:
            return
        
        # Calculate acceleration from forces (F = ma)
        self.acceleration[0] = self.forces[0] / self.mass
        self.acceleration[1] = self.forces[1] / self.mass
        
        # Update velocity (v = v0 + at)
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        
        # Apply friction
        if abs(self.velocity[0]) > 0.01:
            friction_x = -math.copysign(self.friction * self.mass * 9.8, self.velocity[0])
            self.velocity[0] += (friction_x / self.mass) * dt
        else:
            self.velocity[0] = 0
            
        if abs(self.velocity[1]) > 0.01:
            friction_y = -math.copysign(self.friction * self.mass * 9.8, self.velocity[1])
            self.velocity[1] += (friction_y / self.mass) * dt
        else:
            self.velocity[1] = 0
        
        # Update position (p = p0 + vt)
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        
        # Reset forces for next update
        self.forces = [0, 0]
    
    def distance_to(self, other):
        """
        Calculate distance to another physics body.
        
        Args:
            other: Another PhysicsBody
            
        Returns:
            Distance between centers
        """
        dx = self.position[0] - other.position[0]
        dy = self.position[1] - other.position[1]
        return math.sqrt(dx*dx + dy*dy)
    
    def check_collision(self, other):
        """
        Check for collision with another physics body.
        
        Args:
            other: Another PhysicsBody
            
        Returns:
            True if colliding, False otherwise
        """
        # Simple circle-circle collision detection
        if self.shape_type == "circle" and other.shape_type == "circle":
            min_distance = self.radius + other.radius
            return self.distance_to(other) < min_distance
        
        # Simple AABB collision for rectangles
        elif self.shape_type == "rectangle" and other.shape_type == "rectangle":
            self_left = self.position[0]
            self_right = self.position[0] + self.width
            self_top = self.position[1]
            self_bottom = self.position[1] + self.height
            
            other_left = other.position[0]
            other_right = other.position[0] + other.width
            other_top = other.position[1]
            other_bottom = other.position[1] + other.height
            
            return not (self_right < other_left or 
                       self_left > other_right or 
                       self_bottom < other_top or 
                       self_top > other_bottom)
        
        # Mixed circle-rectangle collision
        elif self.shape_type == "circle" and other.shape_type == "rectangle":
            # Find the closest point on the rectangle to the circle
            closest_x = max(other.position[0], min(self.position[0], other.position[0] + other.width))
            closest_y = max(other.position[1], min(self.position[1], other.position[1] + other.height))
            
            # Calculate distance from the closest point to the circle's center
            dx = self.position[0] - closest_x
            dy = self.position[1] - closest_y
            distance_squared = dx*dx + dy*dy
            
            return distance_squared < (self.radius * self.radius)
        
        elif other.shape_type == "circle" and self.shape_type == "rectangle":
            return other.check_collision(self)
        
        # Default to no collision for unsupported shape combinations
        return False
    
    def resolve_collision(self, other):
        """
        Resolve collision with another physics body.
        
        Args:
            other: Another PhysicsBody
        """
        if self.fixed and other.fixed:
            return  # Both objects are fixed, do nothing
        
        # Calculate relative velocity
        relative_velocity = [
            self.velocity[0] - other.velocity[0],
            self.velocity[1] - other.velocity[1]
        ]
        
        # Calculate collision normal
        normal = [
            other.position[0] - self.position[0],
            other.position[1] - self.position[1]
        ]
        
        # Normalize the normal vector
        length = math.sqrt(normal[0]*normal[0] + normal[1]*normal[1])
        if length == 0:
            normal = [0, 1]  # Default normal if centers are at the same position
        else:
            normal = [normal[0]/length, normal[1]/length]
        
        # Calculate relative velocity along the normal
        relative_velocity_normal = (
            relative_velocity[0] * normal[0] + 
            relative_velocity[1] * normal[1]
        )
        
        # If objects are moving away from each other, do nothing
        if relative_velocity_normal > 0:
            return
        
        # Calculate restitution (bounciness)
        e = min(self.restitution, other.restitution)
        
        # Calculate impulse scalar
        j = -(1 + e) * relative_velocity_normal
        j /= (1 / self.mass) + (1 / other.mass)
        
        # Apply impulse to velocities
        impulse = [j * normal[0], j * normal[1]]
        
        if not self.fixed:
            self.velocity[0] += impulse[0] / self.mass
            self.velocity[1] += impulse[1] / self.mass
        
        if not other.fixed:
            other.velocity[0] -= impulse[0] / other.mass
            other.velocity[1] -= impulse[1] / other.mass
        
        # Slightly separate the objects to prevent sticking
        separation_factor = 0.01
        if not self.fixed and not other.fixed:
            self.position[0] -= normal[0] * separation_factor
            self.position[1] -= normal[1] * separation_factor
            other.position[0] += normal[0] * separation_factor
            other.position[1] += normal[1] * separation_factor
        elif not self.fixed:
            self.position[0] -= normal[0] * separation_factor * 2
            self.position[1] -= normal[1] * separation_factor * 2
        elif not other.fixed:
            other.position[0] += normal[0] * separation_factor * 2
            other.position[1] += normal[1] * separation_factor * 2


class PhysicsEngine:
    """
    Physics engine that manages multiple physics bodies and simulates interactions.
    """
    
    def __init__(self, gravity=(0, 9.8), bounds=(0, 0, 800, 600)):
        """
        Initialize the physics engine.
        
        Args:
            gravity: (gx, gy) gravity vector
            bounds: (min_x, min_y, max_x, max_y) simulation boundaries
        """
        self.bodies = {}
        self.gravity = gravity
        self.bounds = bounds
        self.running = False
        self.last_time = None
    
    def add_body(self, body):
        """
        Add a physics body to the simulation.
        
        Args:
            body: PhysicsBody to add
            
        Returns:
            The added body
        """
        self.bodies[body.element_id] = body
        return body
    
    def create_body_from_element(self, element_id, element_type, position, options=None):
        """
        Create a physics body from an SVG element.
        
        Args:
            element_id: ID of the SVG element
            element_type: Type of the element ('circle', 'rect', etc.)
            position: (x, y) initial position
            options: Additional options
            
        Returns:
            The created PhysicsBody
        """
        if options is None:
            options = {}
        
        body = PhysicsBody(
            element_id=element_id,
            mass=options.get('mass', 1.0),
            position=position,
            velocity=options.get('velocity', (0, 0)),
            restitution=options.get('restitution', 0.8),
            friction=options.get('friction', 0.1)
        )
        
        # Set shape-specific properties
        if element_type == 'circle':
            body.shape_type = "circle"
            body.radius = options.get('radius', 20)
        elif element_type == 'rect':
            body.shape_type = "rectangle"
            body.width = options.get('width', 40)
            body.height = options.get('height', 40)
        
        # Add the body to the simulation
        self.add_body(body)
        return body
    
    def remove_body(self, element_id):
        """
        Remove a physics body from the simulation.
        
        Args:
            element_id: ID of the body to remove
        """
        if element_id in self.bodies:
            del self.bodies[element_id]
    
    def update(self, dt=None):
        """
        Update the physics simulation for a time step.
        
        Args:
            dt: Time step in seconds (if None, will calculate based on elapsed time)
        """
        current_time = time.time()
        
        if dt is None:
            if self.last_time is None:
                dt = 1/60  # Default to 60 FPS
            else:
                dt = current_time - self.last_time
                # Cap dt to avoid large time steps
                dt = min(dt, 1/30)
        
        self.last_time = current_time
        
        # Apply gravity to all bodies
        for body in self.bodies.values():
            if not body.fixed:
                body.apply_force((self.gravity[0] * body.mass, self.gravity[1] * body.mass))
        
        # Update all bodies
        for body in self.bodies.values():
            body.update(dt)
            
            # Handle boundary collisions
            min_x, min_y, max_x, max_y = self.bounds
            
            if body.shape_type == "circle":
                # Bottom boundary
                if body.position[1] + body.radius > max_y:
                    body.position[1] = max_y - body.radius
                    body.velocity[1] = -body.velocity[1] * body.restitution
                
                # Top boundary
                if body.position[1] - body.radius < min_y:
                    body.position[1] = min_y + body.radius
                    body.velocity[1] = -body.velocity[1] * body.restitution
                
                # Right boundary
                if body.position[0] + body.radius > max_x:
                    body.position[0] = max_x - body.radius
                    body.velocity[0] = -body.velocity[0] * body.restitution
                
                # Left boundary
                if body.position[0] - body.radius < min_x:
                    body.position[0] = min_x + body.radius
                    body.velocity[0] = -body.velocity[0] * body.restitution
            
            elif body.shape_type == "rectangle":
                # Bottom boundary
                if body.position[1] + body.height > max_y:
                    body.position[1] = max_y - body.height
                    body.velocity[1] = -body.velocity[1] * body.restitution
                
                # Top boundary
                if body.position[1] < min_y:
                    body.position[1] = min_y
                    body.velocity[1] = -body.velocity[1] * body.restitution
                
                # Right boundary
                if body.position[0] + body.width > max_x:
                    body.position[0] = max_x - body.width
                    body.velocity[0] = -body.velocity[0] * body.restitution
                
                # Left boundary
                if body.position[0] < min_x:
                    body.position[0] = min_x
                    body.velocity[0] = -body.velocity[0] * body.restitution
        
        # Handle collisions between bodies
        body_ids = list(self.bodies.keys())
        for i in range(len(body_ids)):
            for j in range(i + 1, len(body_ids)):
                body_a = self.bodies[body_ids[i]]
                body_b = self.bodies[body_ids[j]]
                
                if body_a.check_collision(body_b):
                    body_a.resolve_collision(body_b)
                    body_a.in_collision = True
                    body_b.in_collision = True
                else:
                    body_a.in_collision = False
                    body_b.in_collision = False
        
        # Update SVG element positions
        self._update_svg_positions()
    
    def _update_svg_positions(self):
        """
        Update the positions of SVG elements based on physics bodies.
        """
        for body_id, body in self.bodies.items():
            if body.shape_type == "circle":
                js_code = f"""
                var element = document.getElementById('{body_id}');
                if (element) {{
                    element.setAttribute('cx', '{body.position[0]}');
                    element.setAttribute('cy', '{body.position[1]}');
                    
                    // Optionally visualize collision state
                    if ({str(body.in_collision).lower()}) {{
                        element.setAttribute('stroke', 'red');
                        element.setAttribute('stroke-width', '2');
                    }} else {{
                        element.setAttribute('stroke', 'none');
                    }}
                }}
                """
            elif body.shape_type == "rectangle":
                js_code = f"""
                var element = document.getElementById('{body_id}');
                if (element) {{
                    element.setAttribute('x', '{body.position[0]}');
                    element.setAttribute('y', '{body.position[1]}');
                    
                    // Optionally visualize collision state
                    if ({str(body.in_collision).lower()}) {{
                        element.setAttribute('stroke', 'red');
                        element.setAttribute('stroke-width', '2');
                    }} else {{
                        element.setAttribute('stroke', 'none');
                    }}
                }}
                """
            else:
                # Default for other shapes - use transform
                js_code = f"""
                var element = document.getElementById('{body_id}');
                if (element) {{
                    element.setAttribute('transform', 'translate({body.position[0]}, {body.position[1]})');
                }}
                """
            
            execute_js(js_code)
    
    def start(self, fps=60):
        """
        Start the physics simulation.
        
        Args:
            fps: Target frames per second
        """
        if self.running:
            return
        
        self.running = True
        self.last_time = time.time()
        
        # Set up a JavaScript interval to call update regularly
        interval_ms = int(1000 / fps)
        js_code = f"""
        window.physicsInterval = setInterval(() => {{
            // This will be a placeholder for Python to detect when to run an update
            console.log('PHYSICS_UPDATE_TRIGGER');
        }}, {interval_ms});
        """
        execute_js(js_code)
        
        # In a real implementation, we would need to set up a way to
        # bridge between JavaScript interval and Python update calls
        # This would depend on the specific BrowserTools MCP implementation
    
    def stop(self):
        """
        Stop the physics simulation.
        """
        if not self.running:
            return
        
        self.running = False
        
        # Clear the JavaScript interval
        js_code = """
        if (window.physicsInterval) {
            clearInterval(window.physicsInterval);
            window.physicsInterval = null;
        }
        """
        execute_js(js_code)
    
    def apply_explosion_force(self, position, force, radius):
        """
        Apply an explosion force to all bodies within a radius.
        
        Args:
            position: (x, y) center of explosion
            force: Force magnitude at the center
            radius: Radius of the explosion
        """
        for body in self.bodies.values():
            if body.fixed:
                continue
                
            dx = body.position[0] - position[0]
            dy = body.position[1] - position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < radius:
                # Calculate normalized direction vector
                if distance > 0:
                    direction = [dx/distance, dy/distance]
                else:
                    direction = [0, -1]  # Default direction if at explosion center
                
                # Force decreases with distance from center
                distance_factor = 1 - (distance / radius)
                magnitude = force * distance_factor
                
                # Apply force
                body.apply_force([direction[0] * magnitude, direction[1] * magnitude])
    
    def apply_wind_force(self, direction, strength):
        """
        Apply a wind force to all bodies.
        
        Args:
            direction: (dx, dy) normalized direction vector
            strength: Strength of the wind
        """
        for body in self.bodies.values():
            if not body.fixed:
                # Calculate cross-sectional area (simplified)
                area = body.radius * 2 if body.shape_type == "circle" else body.width * body.height
                
                # Apply force proportional to area
                force = [direction[0] * strength * area, direction[1] * strength * area]
                body.apply_force(force)
    
    def apply_attraction_force(self, attractor_position, strength, min_distance=10):
        """
        Apply an attraction force towards a point.
        
        Args:
            attractor_position: (x, y) position to attract towards
            strength: Strength of attraction
            min_distance: Minimum distance to prevent extreme forces
        """
        for body in self.bodies.values():
            if not body.fixed:
                dx = attractor_position[0] - body.position[0]
                dy = attractor_position[1] - body.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < min_distance:
                    continue
                
                # Calculate normalized direction vector
                direction = [dx/distance, dy/distance]
                
                # Force decreases with square of distance (like gravity)
                force_magnitude = strength * body.mass / (distance * distance)
                
                # Apply force
                body.apply_force([direction[0] * force_magnitude, direction[1] * force_magnitude])
                
    def create_spring(self, body_a_id, body_b_id, stiffness=0.5, rest_length=100, damping=0.1):
        """
        Create a spring connection between two bodies.
        
        Args:
            body_a_id: ID of the first body
            body_b_id: ID of the second body
            stiffness: Spring stiffness (0-1)
            rest_length: Rest length of the spring
            damping: Damping factor (0-1)
            
        Returns:
            Function to apply spring forces
        """
        if body_a_id not in self.bodies or body_b_id not in self.bodies:
            return None
        
        def apply_spring_force():
            body_a = self.bodies.get(body_a_id)
            body_b = self.bodies.get(body_b_id)
            
            if body_a is None or body_b is None:
                return
            
            # Calculate displacement vector
            dx = body_b.position[0] - body_a.position[0]
            dy = body_b.position[1] - body_a.position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance == 0:
                return  # Avoid division by zero
            
            # Calculate spring force (F = -k * x)
            displacement = distance - rest_length
            force_magnitude = stiffness * displacement
            
            # Calculate normalized direction vector
            direction = [dx/distance, dy/distance]
            
            # Calculate relative velocity
            dvx = body_b.velocity[0] - body_a.velocity[0]
            dvy = body_b.velocity[1] - body_a.velocity[1]
            
            # Calculate damping force (F = -c * v)
            # Project velocity onto the spring axis
            relative_velocity_along_spring = dvx * direction[0] + dvy * direction[1]
            damping_force = -damping * relative_velocity_along_spring
            
            # Total force magnitude
            total_force_magnitude = force_magnitude + damping_force
            
            # Apply forces
            force_a = [direction[0] * total_force_magnitude, direction[1] * total_force_magnitude]
            force_b = [-force_a[0], -force_a[1]]
            
            body_a.apply_force(force_a)
            body_b.apply_force(force_b)
            
            # Optionally visualize the spring
            js_code = f"""
            // Draw or update a line between the two bodies
            var line = document.getElementById('spring_{body_a_id}_{body_b_id}');
            if (!line) {{
                var svg = document.querySelector('svg');
                if (svg) {{
                    line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('id', 'spring_{body_a_id}_{body_b_id}');
                    line.setAttribute('stroke', '#999999');
                    line.setAttribute('stroke-width', '2');
                    line.setAttribute('stroke-dasharray', '5,5');
                    svg.appendChild(line);
                }}
            }}
            if (line) {{
                line.setAttribute('x1', '{body_a.position[0]}');
                line.setAttribute('y1', '{body_a.position[1]}');
                line.setAttribute('x2', '{body_b.position[0]}');
                line.setAttribute('y2', '{body_b.position[1]}');
            }}
            """
            execute_js(js_code)
        
        return apply_spring_force


# Example usage in animation context:
def initialize_physics_animation(svg, mcp):
    """
    Initialize a basic physics animation.
    
    Args:
        svg: SVG object from SVG Animation MCP
        mcp: MCP instance
        
    Returns:
        PhysicsEngine instance
    """
    # Create physics engine with downward gravity
    engine = PhysicsEngine(gravity=(0, 98.0), bounds=(0, 0, 800, 600))
    
    # Create a floor (fixed rectangle)
    floor = svg.add_rectangle(x=0, y=550, width=800, height=50, fill="#444444")
    floor_body = engine.create_body_from_element(
        floor.id, 
        "rect", 
        position=(0, 550), 
        options={"width": 800, "height": 50, "mass": 100}
    )
    floor_body.set_fixed(True)
    
    # Create some circles with physics
    circles = []
    for i in range(10):
        x = 100 + i * 60
        y = 100
        circle = svg.add_circle(cx=x, cy=y, r=20, fill=f"hsl({i*36}, 70%, 50%)")
        
        # Add physics body
        body = engine.create_body_from_element(
            circle.id, 
            "circle", 
            position=(x, y), 
            options={"radius": 20, "restitution": 0.8, "friction": 0.1}
        )
        
        # Add some initial velocity
        body.velocity = [(i - 5) * 20, 0]
        circles.append(body)
    
    # Custom JavaScript for interactivity (mouse interaction)
    js_code = """
    var svg = document.querySelector('svg');
    if (svg) {
        svg.addEventListener('mousemove', function(e) {
            var rect = svg.getBoundingClientRect();
            var mouseX = e.clientX - rect.left;
            var mouseY = e.clientY - rect.top;
            
            // Log mouse position for Python to use
            console.log('MOUSE_POS:' + mouseX + ',' + mouseY);
        });
        
        svg.addEventListener('click', function(e) {
            var rect = svg.getBoundingClientRect();
            var mouseX = e.clientX - rect.left;
            var mouseY = e.clientY - rect.top;
            
            // Log click position for Python to use
            console.log('MOUSE_CLICK:' + mouseX + ',' + mouseY);
        });
    }
    """
    mcp.execute_js(js_code)
    
    # In a real implementation, you would process mouse events
    # and trigger engine.apply_explosion_force() or other physics interactions
    
    return engine 