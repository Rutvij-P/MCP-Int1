"""
End-to-end browser tests for the MCP.

These tests require a real browser environment and check that SVG elements are
actually rendered correctly in a web browser.

Note: These tests are marked with the 'browser' marker, so they can be skipped
in environments where browser testing is not possible by using:
pytest -m "not browser"
"""
import pytest
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from svg_animation_mcp import MCP

# Mark all tests in this file as browser tests
pytestmark = pytest.mark.browser

@pytest.fixture(scope="module")
def browser():
    """Fixture to provide a browser instance for testing."""
    # Skip if running in CI environment without browser support
    if os.environ.get('CI') == 'true' and os.environ.get('BROWSER_TESTS') != 'true':
        pytest.skip("Browser tests disabled in CI")
    
    # Set up Chrome options for testing
    chrome_options = Options()
    if os.environ.get('CI') == 'true':
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Create the browser instance
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set up a simple HTML page for testing
    driver.get("data:text/html,<html><body><div id='container'></div></body></html>")
    
    yield driver
    
    # Clean up
    driver.quit()

@pytest.fixture
def real_mcp():
    """Fixture to provide a real MCP instance that uses the actual browser integration."""
    return MCP()

@pytest.mark.skipif(os.environ.get('FULL_BROWSER_TESTS') != 'true', 
                   reason="Full browser tests only run when explicitly enabled")
def test_svg_rendering(browser, real_mcp):
    """Test that SVG elements are correctly rendered in a real browser."""
    # Create SVG in the container
    svg = real_mcp.create_svg(width=500, height=300, parent_selector="#container")
    
    # Add shapes
    circle = svg.add_circle(cx=150, cy=150, r=50, fill="red")
    rect = svg.add_rectangle(x=250, y=100, width=100, height=100, fill="blue")
    
    # Wait for SVG to be rendered
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "svg"))
    )
    
    # Check that SVG was created with correct dimensions
    svg_element = browser.find_element(By.TAG_NAME, "svg")
    assert svg_element.get_attribute("width") == "500"
    assert svg_element.get_attribute("height") == "300"
    
    # Check that circle was created with correct attributes
    circle_element = browser.find_element(By.ID, circle.id)
    assert circle_element.get_attribute("cx") == "150"
    assert circle_element.get_attribute("cy") == "150"
    assert circle_element.get_attribute("r") == "50"
    assert circle_element.get_attribute("fill") == "red"
    
    # Check that rectangle was created with correct attributes
    rect_element = browser.find_element(By.ID, rect.id)
    assert rect_element.get_attribute("x") == "250"
    assert rect_element.get_attribute("y") == "100"
    assert rect_element.get_attribute("width") == "100"
    assert rect_element.get_attribute("height") == "100"
    assert rect_element.get_attribute("fill") == "blue"

@pytest.mark.skipif(os.environ.get('FULL_BROWSER_TESTS') != 'true', 
                   reason="Full browser tests only run when explicitly enabled")
def test_animation_rendering(browser, real_mcp):
    """Test that animations are correctly applied in a real browser."""
    # Create SVG
    svg = real_mcp.create_svg(width=500, height=300, parent_selector="#container")
    
    # Create a circle to animate
    circle = svg.add_circle(cx=250, cy=150, r=30, fill="green")
    
    # Add animation
    anim_id = circle.animate("r", from_value=30, to_value=80, duration=0.5, repeat_count=1)
    
    # Wait for animation to be created
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, anim_id))
    )
    
    # Check animation element attributes
    animation = browser.find_element(By.ID, anim_id)
    assert animation.get_attribute("attributeName") == "r"
    assert animation.get_attribute("from") == "30"
    assert animation.get_attribute("to") == "80"
    assert animation.get_attribute("dur") == "0.5s"
    assert animation.get_attribute("repeatCount") == "1"
    
    # Wait for animation to finish (let's wait a bit more than duration to be safe)
    time.sleep(0.7)
    
    # The radius should now be 80
    circle_element = browser.find_element(By.ID, circle.id)
    assert circle_element.get_attribute("r") == "80" 

@pytest.mark.skipif(os.environ.get('FULL_BROWSER_TESTS') != 'true', 
                   reason="Full browser tests only run when explicitly enabled")
def test_remove_animation(browser, real_mcp):
    """Test that removing animations works correctly in a real browser."""
    # Create SVG
    svg = real_mcp.create_svg(width=500, height=300, parent_selector="#container")
    
    # Create a rectangle
    rect = svg.add_rectangle(x=200, y=100, width=100, height=100, fill="purple")
    
    # Add animation
    anim_id = rect.animate("width", from_value=100, to_value=200, duration=5, repeat_count="indefinite")
    
    # Wait for animation to be created
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, anim_id))
    )
    
    # Remove the animation
    rect.remove_animation(anim_id)
    
    # Wait a moment for the removal to take effect
    time.sleep(0.5)
    
    # The animation element should no longer exist
    animation_elements = browser.find_elements(By.ID, anim_id)
    assert len(animation_elements) == 0 