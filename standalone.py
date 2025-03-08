"""
Standalone version of SVG Animation MCP using Selenium.

This module provides a way to use the SVG Animation MCP
without relying on BrowserTools MCP, using Selenium instead.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class StandaloneBrowser:
    """
    Standalone browser implementation using Selenium.
    """
    
    def __init__(self, headless=False):
        """
        Initialize the standalone browser.
        
        Args:
            headless: Whether to run the browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.init_browser()
    
    def init_browser(self):
        """Initialize the Selenium browser."""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Set up a basic HTML page
        self.driver.get("about:blank")
        self.load_html("""
        <!DOCTYPE html>
        <html>
        <head>
          <title>SVG Animation MCP - Standalone</title>
          <style>
            body {
              margin: 0;
              padding: 0;
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
              background-color: #f0f0f0;
            }
            #animation-container {
              background-color: white;
              border: 1px solid #ccc;
              box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
              width: 800px;
              height: 600px;
            }
          </style>
        </head>
        <body>
          <div id="animation-container"></div>
        </body>
        </html>
        """)
    
    def execute_js(self, code):
        """
        Execute JavaScript code in the browser.
        
        Args:
            code: JavaScript code to execute
        """
        if self.driver is None:
            self.init_browser()
        
        return self.driver.execute_script(code)
    
    def load_html(self, html):
        """
        Load HTML content into the browser.
        
        Args:
            html: HTML content to load
        """
        if self.driver is None:
            self.init_browser()
        
        self.driver.execute_script(f"""
        document.open();
        document.write(`{html}`);
        document.close();
        """)
    
    def take_screenshot(self, filename="screenshot.png"):
        """
        Take a screenshot of the browser.
        
        Args:
            filename: Name of the screenshot file
        """
        if self.driver is None:
            raise ValueError("Browser not initialized")
        
        self.driver.save_screenshot(filename)
    
    def close(self):
        """Close the browser."""
        if self.driver is not None:
            self.driver.quit()
            self.driver = None


def patch_browser_integration():
    """
    Patch the browser_integration module to use StandaloneBrowser.
    
    Call this function before importing any other SVG Animation MCP modules.
    """
    import sys
    import browser_integration
    
    # Create StandaloneBrowser instance
    standalone_browser = StandaloneBrowser(headless=False)
    
    # Patch execute_js function
    def patched_execute_js(code):
        return standalone_browser.execute_js(code)
    
    browser_integration.execute_js = patched_execute_js
    
    # Patch init_browser_environment function
    def patched_init_browser_environment():
        pass  # Already initialized in StandaloneBrowser
    
    browser_integration.init_browser_environment = patched_init_browser_environment
    
    # Add new function to take screenshots
    def take_screenshot(filename="screenshot.png"):
        standalone_browser.take_screenshot(filename)
    
    browser_integration.take_screenshot = take_screenshot
    
    # Make sure standalone_browser gets cleaned up at exit
    import atexit
    atexit.register(standalone_browser.close)
    
    return standalone_browser


if __name__ == "__main__":
    # Example of running in standalone mode
    standalone_browser = patch_browser_integration()
    
    from svg_animation_mcp import MCP
    from utils import generate_star_points, generate_path_data
    
    # Create MCP instance
    mcp = MCP()
    
    # Create SVG canvas
    svg = mcp.create_svg(width=600, height=400, parent_selector="#animation-container")
    
    # Add a rectangle that moves horizontally
    rect = svg.add_rectangle(x=50, y=50, width=100, height=80, fill="red", stroke="black", stroke_width=2)
    rect.animate_transform("translate", from_value=(0, 0), to_value=(400, 0), duration=3)
    
    # Create a star shape using path
    star_points = generate_star_points(cx=300, cy=200, outer_radius=100, inner_radius=50, points=5)
    star_path_data = generate_path_data(star_points) + " Z"  # Z closes the path
    
    star = svg.add_path(d=star_path_data, fill="gold", stroke="orange", stroke_width=2)
    
    # Animate the star rotation
    star.animate_transform("rotate", from_value="0 300 200", to_value="360 300 200", 
                           duration=5, repeat_count="indefinite")
    
    # Wait for animations to run for a while, then take a screenshot
    print("Running animations for 3 seconds...")
    time.sleep(3)
    standalone_browser.take_screenshot("animation_screenshot.png")
    print("Screenshot saved as animation_screenshot.png")
    
    # Wait for user to close the browser
    input("Press Enter to close the browser...")
    standalone_browser.close() 