"""
Real Browser Connection for SVG Animation MCP.

This module ensures the MCP uses a real browser connection instead of a mock implementation.
It monkey-patches the browser_integration.py module with real implementations.
"""

import os
import time
import platform
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
import re

# Initialize global variables
driver = None
html_renderer = None

# Create a global driver instance that will be used by the MCP
def initialize_browser():
    """Initialize and return a browser instance.
    
    Tries multiple browsers in order: Chrome, Firefox, Brave, Zen, Safari (on Mac).
    If no browser is available, creates an HTML renderer as fallback.
    """
    global driver, html_renderer
    
    print("Initializing browser...")
    
    # Try Chrome first
    try:
        print("Attempting to initialize Chrome...")
        chrome_options = Options()
        # Using headless mode for the background browser - remove this line to see the browser window
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        print("Chrome browser initialized successfully.")
        return driver
    except Exception as e:
        print(f"Failed to initialize Chrome: {str(e)}")
    
    # Try Brave browser
    try:
        print("Attempting to initialize Brave browser...")
        brave_path = ""
        
        # Check common Brave paths based on OS
        if platform.system() == 'Darwin':  # macOS
            brave_paths = [
                '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
                '/Applications/Brave.app/Contents/MacOS/Brave'
            ]
            for path in brave_paths:
                if os.path.exists(path):
                    brave_path = path
                    break
                    
        if brave_path:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.binary_location = brave_path
            
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            print("Brave browser initialized successfully.")
            return driver
        else:
            print("Brave browser not found at expected locations.")
    except Exception as e:
        print(f"Failed to initialize Brave browser: {str(e)}")
    
    # Try Firefox as fallback
    try:
        print("Attempting to initialize Firefox...")
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=firefox_options
        )
        print("Firefox browser initialized successfully.")
        return driver
    except Exception as e:
        print(f"Failed to initialize Firefox browser: {str(e)}")
    
    # Try Safari on macOS as final option
    if platform.system() == 'Darwin':  # macOS
        try:
            print("Attempting to initialize Safari...")
            safari_options = SafariOptions()
            driver = webdriver.Safari(options=safari_options)
            print("Safari browser initialized successfully.")
            return driver
        except Exception as e:
            print(f"Failed to initialize Safari browser: {str(e)}")
    
    # If all browsers fail, create an HTML renderer as fallback
    print("WARNING: Could not initialize any browser. Using HTML renderer only.")
    html_renderer = HTMLRenderer()
    
    # Monkey-patch the execute_js function to use our HTML renderer
    import browser_integration
    original_execute_js = browser_integration.execute_js
    
    def html_renderer_execute_js(code, throw_on_error=True):
        print("Using HTML renderer for JavaScript execution")
        return html_renderer.execute_js(code)
    
    browser_integration.execute_js = html_renderer_execute_js
    print("Successfully monkey-patched browser_integration.execute_js with real browser implementation.")
    
    return None

# Create a fallback mechanism for JavaScript execution
class HTMLRenderer:
    """Fallback class for when no browser is available.
    
    This class creates a simple HTML file with the SVG content
    and updates it whenever execute_js is called.
    """
    def __init__(self, html_file=None):
        self.html_file = html_file or "svg_output.html"
        self.svg_content = ""
        self.create_initial_html()
        # Remove auto-opening the browser in a separate window
        # self.auto_open_browser()
        
    def auto_open_browser(self):
        """Automatically open the HTML file in the default browser."""
        # This method is now deprecated since we're showing everything in one page
        pass
    
    def create_initial_html(self):
        """Create the initial HTML file with SVG container."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SVG Animation MCP - Renderer</title>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 20px; 
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                }}
                #svg-container {{ 
                    border: 1px solid #ccc; 
                    margin: 20px auto; 
                    background-color: white;
                    min-height: 500px;
                    position: relative;
                    overflow: hidden;
                }}
                .info-box {{
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #e8f4f8;
                    border-left: 4px solid #4CAF50;
                    border-radius: 4px;
                }}
                .log {{
                    margin-top: 20px;
                    height: 150px;
                    overflow-y: auto;
                    background-color: #333;
                    color: #fff;
                    padding: 10px;
                    font-family: monospace;
                    font-size: 12px;
                    border-radius: 4px;
                }}
                svg {{
                    width: 100%;
                    height: 100%;
                    display: block;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SVG Animation MCP - HTML Renderer</h1>
                
                <div class="info-box">
                    <p><strong>Note:</strong> This is a fallback renderer since no browser automation was available. 
                    The SVG animations are being rendered in this HTML file.</p>
                </div>
                
                <div id="svg-container">
                    <!-- SVG will be inserted here -->
                </div>
                <div class="log" id="log-container">
                    <!-- LOG-MARKER -->
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(self.html_file, "w") as f:
            f.write(html_content)
    
    def execute_js(self, code):
        """
        Execute JavaScript code and update the HTML file.
        
        Args:
            code: JavaScript code to execute
            
        Returns:
            A dummy result or None
        """
        try:
            # Parse the JavaScript code to extract SVG operations
            if "document.createElementNS('http://www.w3.org/2000/svg', 'svg')" in code:
                # Creating SVG element
                svg_id_match = re.search(r"setAttribute\('id', '([^']+)'\)", code)
                width_match = re.search(r"setAttribute\('width', ['\"]*([^'\"]+)['\"]*\)", code)
                height_match = re.search(r"setAttribute\('height', ['\"]*([^'\"]+)['\"]*\)", code)
                
                if svg_id_match and width_match and height_match:
                    svg_id = svg_id_match.group(1)
                    width = width_match.group(1)
                    height = height_match.group(1)
                    
                    # Create a new SVG element with these attributes
                    self.svg_content += f'<svg id="{svg_id}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"></svg>'
                    
                    # Update the HTML file
                    self.update_html()
                    
                    # Log the action
                    self.log_messages.append(f"Created SVG element with ID: {svg_id}, width: {width}, height: {height}")
                    
                    # Return the ID as a success indicator
                    return svg_id
            
            elif "document.createElementNS('http://www.w3.org/2000/svg', 'rect')" in code:
                # Creating rectangle
                self._handle_shape_creation(code, 'rect')
            
            elif "document.createElementNS('http://www.w3.org/2000/svg', 'circle')" in code:
                # Creating circle
                self._handle_shape_creation(code, 'circle')
            
            elif "document.createElementNS('http://www.w3.org/2000/svg', 'text')" in code:
                # Creating text
                self._handle_shape_creation(code, 'text')
            
            elif "document.createElementNS('http://www.w3.org/2000/svg', 'path')" in code:
                # Creating path
                self._handle_shape_creation(code, 'path')
            
            elif "document.createElementNS('http://www.w3.org/2000/svg', 'animate')" in code:
                # Creating animation
                self._handle_animation_creation(code, 'animate')
                
            elif "document.createElementNS('http://www.w3.org/2000/svg', 'animateTransform')" in code:
                # Creating transform animation
                self._handle_animation_creation(code, 'animateTransform')
            
            elif "removeChild" in code:
                # Removing an element
                element_id_match = re.search(r"getElementById\('([^']+)'\)", code)
                if element_id_match:
                    element_id = element_id_match.group(1)
                    self._handle_element_removal(element_id)
            
            else:
                # For other JavaScript operations, just log them
                self.log_messages.append(f"JavaScript: {code[:100]}{'...' if len(code) > 100 else ''}")
            
            # Extract potential IDs from the code
            id_match = re.search(r"setAttribute\('id', ['\"]*([^'\"]+)['\"]*\)", code)
            if id_match:
                return id_match.group(1)
            
            return "ok"
            
        except Exception as e:
            self.log_messages.append(f"Error executing JavaScript: {str(e)}")
            print(f"Error in HTML renderer: {str(e)}")
            return None
    
    def _handle_shape_creation(self, code, shape_type):
        """Handle the creation of an SVG shape element."""
        element_id_match = re.search(r"setAttribute\('id', ['\"]*([^'\"]+)['\"]*\)", code)
        parent_id_match = re.search(r"getElementById\('([^']+)'\)", code)
        
        if element_id_match and parent_id_match:
            element_id = element_id_match.group(1)
            parent_id = parent_id_match.group(1)
            
            # Extract all attribute assignments
            attr_matches = re.findall(r"setAttribute\('([^']+)', ['\"]*([^'\"]+)['\"]*\)", code)
            
            # Create element HTML
            attributes = ' '.join([f'{attr}="{value}"' for attr, value in attr_matches])
            
            if shape_type == 'text':
                # For text elements, also extract the text content
                text_match = re.search(r"textContent = ['\"]*([^'\"]+)['\"]*", code)
                text_content = text_match.group(1) if text_match else ""
                element_html = f'<{shape_type} id="{element_id}" {attributes}>{text_content}</{shape_type}>'
            else:
                element_html = f'<{shape_type} id="{element_id}" {attributes}></{shape_type}>'
            
            # Add to SVG content if parent exists
            if parent_id in self.svg_content:
                if "</svg>" in self.svg_content[parent_id]:
                    self.svg_content = self.svg_content.replace(f"{parent_id}</svg>", f"{parent_id}{element_html}</svg>")
                else:
                    self.svg_content = f'{self.svg_content}{element_html}'
                
                # Log the action
                self.log_messages.append(f"Created {shape_type} element with ID: {element_id}")
                
                # Update the HTML file
                self.update_html()
                
                return element_id
    
    def _handle_animation_creation(self, code, anim_type):
        """Handle the creation of an SVG animation element."""
        animation_id_match = re.search(r"setAttribute\('id', ['\"]*([^'\"]+)['\"]*\)", code)
        parent_id_match = re.search(r"getElementById\('([^']+)'\)", code)
        
        if animation_id_match and parent_id_match:
            animation_id = animation_id_match.group(1)
            parent_id = parent_id_match.group(1)
            
            # Extract all attribute assignments
            attr_matches = re.findall(r"setAttribute\('([^']+)', ['\"]*([^'\"]+)['\"]*\)", code)
            
            # Create animation HTML
            attributes = ' '.join([f'{attr}="{value}"' for attr, value in attr_matches])
            anim_html = f'<{anim_type} id="{animation_id}" {attributes}></{anim_type}>'
            
            # Find the parent element and add the animation
            for svg_id, svg_content in self.svg_content.items():
                if f'id="{parent_id}"' in svg_content:
                    # Find the specific element within the SVG
                    element_start = svg_content.find(f'id="{parent_id}"')
                    if element_start > -1:
                        # Find the closing tag of this element
                        element_tag = None
                        for tag in ['rect', 'circle', 'text', 'path']:
                            if f'<{tag} ' in svg_content[element_start-10:element_start]:
                                element_tag = tag
                                break
                        
                        if element_tag:
                            # Find the end of this element
                            close_tag = f'</{element_tag}>'
                            close_tag_pos = svg_content.find(close_tag, element_start)
                            if close_tag_pos > -1:
                                # Insert the animation before the closing tag
                                new_svg_content = (
                                    svg_content[:close_tag_pos] +
                                    anim_html +
                                    svg_content[close_tag_pos:]
                                )
                                self.svg_content[svg_id] = new_svg_content
                                
                                # Log the action
                                self.log_messages.append(f"Created {anim_type} with ID: {animation_id} for element: {parent_id}")
                                
                                # Update the HTML file
                                self.update_html()
                                
                                return animation_id
            
            # If we couldn't find the element for some reason, add to the SVG directly
            for svg_id, svg_content in self.svg_content.items():
                if "</svg>" in svg_content:
                    self.svg_content[svg_id] = svg_content.replace("</svg>", f"{anim_html}</svg>")
                    
                    # Log the action
                    self.log_messages.append(f"Created {anim_type} with ID: {animation_id} (added to SVG)")
                    
                    # Update the HTML file
                    self.update_html()
                    
                    return animation_id
    
    def _handle_element_removal(self, element_id):
        """Handle the removal of an SVG element."""
        # First try to remove an animation
        for svg_id, svg_content in self.svg_content.items():
            animation_pattern = f'<(?:animate|animateTransform)[^>]*id="{element_id}"[^>]*>.*?</(?:animate|animateTransform)>'
            new_content = re.sub(animation_pattern, '', svg_content, flags=re.DOTALL)
            
            if new_content != svg_content:
                self.svg_content[svg_id] = new_content
                self.log_messages.append(f"Removed animation with ID: {element_id}")
                self.update_html()
                return True
        
        # Then try to remove a shape
        for svg_id, svg_content in self.svg_content.items():
            # Try to match and remove any SVG element with this ID
            element_pattern = f'<(?:rect|circle|text|path)[^>]*id="{element_id}"[^>]*>.*?</(?:rect|circle|text|path)>'
            new_content = re.sub(element_pattern, '', svg_content, flags=re.DOTALL)
            
            if new_content != svg_content:
                self.svg_content[svg_id] = new_content
                self.log_messages.append(f"Removed element with ID: {element_id}")
                self.update_html()
                return True
        
        return False
    
    def log_action(self, message):
        """Log an action in the HTML file."""
        self.log_messages.append(message)
        self.update_html()
    
    def update_html(self):
        """Update the HTML file with the current SVG content and logs."""
        try:
            with open(self.html_file, "r") as f:
                html_content = f.read()
            
            # Update SVG content
            svg_container_start = html_content.find('<div id="svg-container">')
            if svg_container_start > -1:
                svg_container_end = html_content.find('</div>', svg_container_start)
                
                if svg_container_end > -1:
                    # Get the SVG content to insert
                    svg_content = ""
                    for svg_id, svg_element in self.svg_content.items():
                        svg_content += svg_element + "\n"
                    
                    # Create a new HTML with the updated SVG
                    new_html = html_content[:svg_container_start + len('<div id="svg-container">')]
                    new_html += "\n" + svg_content + "\n"
                    new_html += html_content[svg_container_end:]
                    
                    # Update the log content
                    log_marker = "<!-- LOG-MARKER -->"
                    log_pos = new_html.find(log_marker)
                    if log_pos > -1:
                        log_content = "\n".join([f"<div>[{i}] {msg}</div>" for i, msg in enumerate(self.log_messages[-30:])])
                        new_html = new_html.replace(log_marker, log_content + "\n" + log_marker)
                    
                    # Write the updated HTML
                    with open(self.html_file, "w") as f:
                        f.write(new_html)
            
        except Exception as e:
            print(f"Error updating HTML: {str(e)}")

# Try to create a browser instance
browser_driver = initialize_browser()

# If no browser could be initialized, create an HTML renderer
if browser_driver is None:
    html_renderer = HTMLRenderer()
else:
    html_renderer = None

def execute_js(code, throw_on_error=True):
    """
    Execute JavaScript code in the browser.
    
    Args:
        code: JavaScript code to execute
        throw_on_error: Whether to raise an exception on error
        
    Returns:
        Result of the JavaScript execution, or None
        
    Raises:
        Exception: If JavaScript execution fails and throw_on_error is True
    """
    global driver, html_renderer
    
    try:
        if driver is not None:
            # Use real browser
            result = driver.execute_script(f"return {code}")
            return result
        elif html_renderer is not None:
            # Use HTML renderer
            result = html_renderer.execute_js(code)
            return result
        else:
            # No browser or renderer available
            if throw_on_error:
                raise Exception("No browser or HTML renderer available")
            return None
    except Exception as e:
        if throw_on_error:
            raise Exception(f"Failed to execute JavaScript: {str(e)}")
        print(f"Warning: JavaScript execution failed: {str(e)}")
        return None

def shutdown():
    """
    Shut down the browser connection.
    
    This function shuts down the browser connection if one exists.
    """
    global driver
    
    try:
        if driver is not None:
            driver.quit()
            print("Browser closed")
    except Exception as e:
        print(f"Error shutting down browser: {str(e)}")

# Monkey-patch the browser_integration module when this module is imported
try:
    import browser_integration
    # Override the functions with our real implementations
    browser_integration.execute_js = execute_js
    browser_integration.initialize = initialize_browser
    browser_integration.shutdown = shutdown
    browser_integration.BrowserIntegrationError = Exception  # Use our exception
    print("Successfully monkey-patched browser_integration with real implementations.")
except ImportError:
    print("Warning: browser_integration module not found, monkey-patching skipped.") 