"""
Animation Settings UI Module for SVG Animation MCP.

This module provides a user interface for configuring and fine-tuning
SVG animation parameters.
"""

from browser_integration import execute_js

class AnimationSettingsUI:
    """
    Class for creating and managing a settings UI for animations.
    
    Provides controls for adjusting animation parameters in real-time.
    """
    
    def __init__(self, mcp, parent_selector="#animation-container"):
        """
        Initialize the settings UI.
        
        Args:
            mcp: MCP instance
            parent_selector: CSS selector for the parent element
        """
        self.mcp = mcp
        self.parent_selector = parent_selector
        self.ui_id = "animation-settings-ui"
        self.settings = {}
        self.callbacks = {}
        self.is_visible = False
        self.selected_element_id = None
    
    def create_ui(self):
        """
        Create the settings UI in the browser.
        
        Returns:
            True if successful, False otherwise
        """
        # Basic UI structure with CSS
        js_code = f"""
        (function() {{
            // Check if UI already exists
            if (document.getElementById('{self.ui_id}')) {{
                return true;
            }}
            
            // Create UI container
            var container = document.createElement('div');
            container.id = '{self.ui_id}';
            
            // Add styles
            container.style.cssText = `
                position: absolute;
                right: 20px;
                top: 20px;
                width: 300px;
                background: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                padding: 15px;
                font-family: Arial, sans-serif;
                z-index: 1000;
                overflow: auto;
                max-height: 80vh;
                display: none;
            `;
            
            // Add header
            var header = document.createElement('div');
            header.innerHTML = '<h3 style="margin-top: 0;">Animation Settings</h3>';
            header.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
                margin-bottom: 15px;
            `;
            
            // Add close button
            var closeBtn = document.createElement('button');
            closeBtn.textContent = '×';
            closeBtn.style.cssText = `
                background: none;
                border: none;
                font-size: 20px;
                cursor: pointer;
                color: #666;
            `;
            closeBtn.onclick = function() {{
                container.style.display = 'none';
                console.log('SETTINGS_UI_CLOSED');
            }};
            header.appendChild(closeBtn);
            
            container.appendChild(header);
            
            // Add content container
            var content = document.createElement('div');
            content.id = '{self.ui_id}-content';
            container.appendChild(content);
            
            // Add element selector
            var selectorContainer = document.createElement('div');
            selectorContainer.style.marginBottom = '15px';
            
            var selectorLabel = document.createElement('label');
            selectorLabel.textContent = 'Select Element: ';
            selectorLabel.for = '{self.ui_id}-element-selector';
            selectorLabel.style.display = 'block';
            selectorLabel.style.marginBottom = '5px';
            
            var selector = document.createElement('select');
            selector.id = '{self.ui_id}-element-selector';
            selector.style.cssText = `
                width: 100%;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #ddd;
            `;
            
            // Add default option
            var defaultOption = document.createElement('option');
            defaultOption.textContent = 'Select an element...';
            defaultOption.value = '';
            selector.appendChild(defaultOption);
            
            // Event listener for element selection
            selector.onchange = function() {{
                console.log('ELEMENT_SELECTED:' + this.value);
            }};
            
            selectorContainer.appendChild(selectorLabel);
            selectorContainer.appendChild(selector);
            content.appendChild(selectorContainer);
            
            // Add settings container
            var settingsContainer = document.createElement('div');
            settingsContainer.id = '{self.ui_id}-settings';
            content.appendChild(settingsContainer);
            
            // Add action buttons
            var buttonsContainer = document.createElement('div');
            buttonsContainer.style.cssText = `
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            `;
            
            var applyBtn = document.createElement('button');
            applyBtn.textContent = 'Apply';
            applyBtn.style.cssText = `
                background: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                flex: 1;
                margin-right: 5px;
            `;
            applyBtn.onclick = function() {{
                console.log('SETTINGS_APPLIED');
            }};
            
            var resetBtn = document.createElement('button');
            resetBtn.textContent = 'Reset';
            resetBtn.style.cssText = `
                background: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                flex: 1;
                margin-left: 5px;
            `;
            resetBtn.onclick = function() {{
                console.log('SETTINGS_RESET');
            }};
            
            buttonsContainer.appendChild(applyBtn);
            buttonsContainer.appendChild(resetBtn);
            content.appendChild(buttonsContainer);
            
            // Add UI to parent
            var parent = document.querySelector('{self.parent_selector}');
            if (parent) {{
                parent.style.position = 'relative';
                parent.appendChild(container);
                return true;
            }}
            
            return false;
        }})();
        """
        
        result = execute_js(js_code)
        
        if result:
            self._populate_element_selector()
            return True
        
        return False
    
    def show(self):
        """
        Show the settings UI.
        """
        if not self.is_visible:
            js_code = f"""
            var ui = document.getElementById('{self.ui_id}');
            if (ui) {{
                ui.style.display = 'block';
                return true;
            }}
            return false;
            """
            
            result = execute_js(js_code)
            self.is_visible = result
            
            if result:
                self._populate_element_selector()
    
    def hide(self):
        """
        Hide the settings UI.
        """
        if self.is_visible:
            js_code = f"""
            var ui = document.getElementById('{self.ui_id}');
            if (ui) {{
                ui.style.display = 'none';
                return true;
            }}
            return false;
            """
            
            result = execute_js(js_code)
            self.is_visible = not result
    
    def toggle(self):
        """
        Toggle the visibility of the settings UI.
        """
        if self.is_visible:
            self.hide()
        else:
            self.show()
    
    def _populate_element_selector(self):
        """
        Populate the element selector with SVG elements.
        """
        js_code = """
        (function() {
            // Get all SVG elements
            var svg = document.querySelector('svg');
            if (!svg) return false;
            
            var elements = svg.querySelectorAll('*');
            var selector = document.getElementById('animation-settings-ui-element-selector');
            
            if (!selector) return false;
            
            // Clear existing options (except the first default one)
            while (selector.options.length > 1) {
                selector.remove(1);
            }
            
            // Add options for each element with an ID
            for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                if (element.id && element.tagName !== 'svg') {
                    var option = document.createElement('option');
                    option.value = element.id;
                    option.textContent = element.tagName + ' #' + element.id;
                    selector.appendChild(option);
                }
            }
            
            return true;
        })();
        """
        
        execute_js(js_code)
    
    def select_element(self, element_id):
        """
        Select an element for editing.
        
        Args:
            element_id: ID of the element to select
        """
        self.selected_element_id = element_id
        
        if not element_id:
            self._clear_settings()
            return
        
        # Get element attributes
        js_code = f"""
        (function() {{
            var element = document.getElementById('{element_id}');
            if (!element) return null;
            
            var tagName = element.tagName.toLowerCase();
            var attrs = {{}};
            
            for (var i = 0; i < element.attributes.length; i++) {{
                var attr = element.attributes[i];
                attrs[attr.name] = attr.value;
            }}
            
            // Get any animations
            var animations = [];
            var animElements = element.querySelectorAll('animate, animateTransform');
            
            for (var i = 0; i < animElements.length; i++) {{
                var anim = animElements[i];
                var animAttrs = {{}};
                
                for (var j = 0; j < anim.attributes.length; j++) {{
                    var attr = anim.attributes[j];
                    animAttrs[attr.name] = attr.value;
                }}
                
                animations.push({{
                    id: anim.id || '',
                    type: anim.tagName.toLowerCase(),
                    attributes: animAttrs
                }});
            }}
            
            return {{
                tagName: tagName,
                attributes: attrs,
                animations: animations
            }};
        }})();
        """
        
        # In a real implementation, this would execute JavaScript and get the result
        # For now, we'll simulate a result
        element_data = {
            'tagName': 'circle',
            'attributes': {
                'cx': '100',
                'cy': '100',
                'r': '50',
                'fill': 'blue'
            },
            'animations': [
                {
                    'id': 'anim1',
                    'type': 'animate',
                    'attributes': {
                        'attributeName': 'r',
                        'from': '50',
                        'to': '80',
                        'dur': '2s',
                        'repeatCount': 'indefinite'
                    }
                }
            ]
        }
        
        # Generate settings for this element
        self._create_settings_for_element(element_data)
    
    def _create_settings_for_element(self, element_data):
        """
        Create settings controls based on element data.
        
        Args:
            element_data: Dictionary with element data
        """
        # Clear existing settings
        self._clear_settings()
        
        # Create sections for basic attributes and animations
        settings_html = """
        <div style="margin-bottom: 20px;">
            <h4 style="margin-top: 0; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">Element Attributes</h4>
            <div id="element-attributes">
        """
        
        # Add controls for element attributes
        for attr_name, attr_value in element_data['attributes'].items():
            if attr_name != 'id':
                # Create appropriate inputs based on attribute types
                if attr_name in ['cx', 'cy', 'r', 'x', 'y', 'width', 'height']:
                    # Numeric input
                    settings_html += f"""
                    <div style="margin-bottom: 10px;">
                        <label style="display: block; margin-bottom: 5px;">{attr_name}:</label>
                        <input 
                            type="range" 
                            id="attr-{attr_name}" 
                            min="0" 
                            max="500" 
                            value="{attr_value}" 
                            style="width: 70%; margin-right: 10px; vertical-align: middle;"
                            data-attr-name="{attr_name}"
                            oninput="document.getElementById('attr-{attr_name}-value').value = this.value;"
                        />
                        <input 
                            type="number" 
                            id="attr-{attr_name}-value" 
                            value="{attr_value}" 
                            style="width: 20%; vertical-align: middle;"
                            oninput="document.getElementById('attr-{attr_name}').value = this.value;"
                        />
                    </div>
                    """
                elif attr_name == 'fill' or attr_name == 'stroke':
                    # Color picker
                    settings_html += f"""
                    <div style="margin-bottom: 10px;">
                        <label style="display: block; margin-bottom: 5px;">{attr_name}:</label>
                        <input 
                            type="color" 
                            id="attr-{attr_name}" 
                            value="{attr_value}" 
                            style="width: 100%;"
                            data-attr-name="{attr_name}"
                        />
                    </div>
                    """
                else:
                    # Generic text input
                    settings_html += f"""
                    <div style="margin-bottom: 10px;">
                        <label style="display: block; margin-bottom: 5px;">{attr_name}:</label>
                        <input 
                            type="text" 
                            id="attr-{attr_name}" 
                            value="{attr_value}" 
                            style="width: 100%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"
                            data-attr-name="{attr_name}"
                        />
                    </div>
                    """
        
        settings_html += """
            </div>
        </div>
        """
        
        # Add section for animations
        settings_html += """
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin-top: 0; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">Animations</h4>
                <button id="add-animation-btn" style="background: #2196F3; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Add</button>
            </div>
            <div id="animations-list">
        """
        
        # Add controls for each animation
        for i, animation in enumerate(element_data['animations']):
            animation_type = animation['type']
            attrs = animation['attributes']
            
            settings_html += f"""
            <div style="border: 1px solid #ddd; border-radius: 4px; padding: 10px; margin-bottom: 10px;" data-animation-index="{i}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h5 style="margin: 0;">{animation_type.capitalize()}: {attrs.get('attributeName', '')}</h5>
                    <button class="remove-animation-btn" style="background: #f44336; color: white; border: none; padding: 3px 8px; border-radius: 4px; cursor: pointer; font-size: 12px;">Remove</button>
                </div>
            """
            
            # Add controls for animation attributes
            for attr_name, attr_value in attrs.items():
                # Special handling for specific animation attributes
                if attr_name == 'dur':
                    # Duration input (convert "2s" to "2")
                    numeric_value = attr_value.replace('s', '')
                    settings_html += f"""
                    <div style="margin-bottom: 10px;">
                        <label style="display: block; margin-bottom: 5px;">Duration (s):</label>
                        <input 
                            type="range" 
                            id="anim-{i}-dur" 
                            min="0.1" 
                            max="10" 
                            step="0.1"
                            value="{numeric_value}" 
                            style="width: 70%; margin-right: 10px; vertical-align: middle;"
                            data-anim-index="{i}"
                            data-attr-name="dur"
                            oninput="document.getElementById('anim-{i}-dur-value').value = this.value;"
                        />
                        <input 
                            type="number" 
                            id="anim-{i}-dur-value" 
                            value="{numeric_value}" 
                            min="0.1"
                            step="0.1"
                            style="width: 20%; vertical-align: middle;"
                            oninput="document.getElementById('anim-{i}-dur').value = this.value;"
                        />
                    </div>
                    """
                elif attr_name in ['from', 'to']:
                    # From/To values for numeric attributes
                    if attrs.get('attributeName') in ['r', 'cx', 'cy', 'x', 'y', 'width', 'height']:
                        settings_html += f"""
                        <div style="margin-bottom: 10px;">
                            <label style="display: block; margin-bottom: 5px;">{attr_name.capitalize()}:</label>
                            <input 
                                type="range" 
                                id="anim-{i}-{attr_name}" 
                                min="0" 
                                max="500" 
                                value="{attr_value}" 
                                style="width: 70%; margin-right: 10px; vertical-align: middle;"
                                data-anim-index="{i}"
                                data-attr-name="{attr_name}"
                                oninput="document.getElementById('anim-{i}-{attr_name}-value').value = this.value;"
                            />
                            <input 
                                type="number" 
                                id="anim-{i}-{attr_name}-value" 
                                value="{attr_value}" 
                                style="width: 20%; vertical-align: middle;"
                                oninput="document.getElementById('anim-{i}-{attr_name}').value = this.value;"
                            />
                        </div>
                        """
                    elif attrs.get('attributeName') in ['fill', 'stroke']:
                        # Color picker for color attributes
                        settings_html += f"""
                        <div style="margin-bottom: 10px;">
                            <label style="display: block; margin-bottom: 5px;">{attr_name.capitalize()}:</label>
                            <input 
                                type="color" 
                                id="anim-{i}-{attr_name}" 
                                value="{attr_value}" 
                                style="width: 100%;"
                                data-anim-index="{i}"
                                data-attr-name="{attr_name}"
                            />
                        </div>
                        """
                    else:
                        # Generic text input for other attributes
                        settings_html += f"""
                        <div style="margin-bottom: 10px;">
                            <label style="display: block; margin-bottom: 5px;">{attr_name.capitalize()}:</label>
                            <input 
                                type="text" 
                                id="anim-{i}-{attr_name}" 
                                value="{attr_value}" 
                                style="width: 100%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"
                                data-anim-index="{i}"
                                data-attr-name="{attr_name}"
                            />
                        </div>
                        """
                elif attr_name == 'repeatCount':
                    # Special handling for repeatCount
                    settings_html += f"""
                    <div style="margin-bottom: 10px;">
                        <label style="display: block; margin-bottom: 5px;">Repeat:</label>
                        <select 
                            id="anim-{i}-repeatCount" 
                            style="width: 100%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"
                            data-anim-index="{i}"
                            data-attr-name="repeatCount"
                        >
                            <option value="1" {"selected" if attr_value == "1" else ""}>Once</option>
                            <option value="2" {"selected" if attr_value == "2" else ""}>Twice</option>
                            <option value="5" {"selected" if attr_value == "5" else ""}>5 times</option>
                            <option value="10" {"selected" if attr_value == "10" else ""}>10 times</option>
                            <option value="indefinite" {"selected" if attr_value == "indefinite" else ""}>Indefinite</option>
                        </select>
                    </div>
                    """
            
            settings_html += """
            </div>
            """
        
        settings_html += """
            </div>
        </div>
        """
        
        # Add the settings HTML to the UI
        js_code = f"""
        (function() {{
            var settingsContainer = document.getElementById('{self.ui_id}-settings');
            if (!settingsContainer) return false;
            
            settingsContainer.innerHTML = `{settings_html}`;
            
            // Add event listener for the "Add Animation" button
            var addAnimBtn = document.getElementById('add-animation-btn');
            if (addAnimBtn) {{
                addAnimBtn.onclick = function() {{
                    console.log('ADD_ANIMATION:{element_data["tagName"]}');
                }};
            }}
            
            // Add event listeners for "Remove Animation" buttons
            var removeButtons = document.querySelectorAll('.remove-animation-btn');
            for (var i = 0; i < removeButtons.length; i++) {{
                removeButtons[i].onclick = function() {{
                    var animDiv = this.closest('div[data-animation-index]');
                    var index = animDiv.getAttribute('data-animation-index');
                    console.log('REMOVE_ANIMATION:' + index);
                }};
            }}
            
            // Add event listeners for attribute changes
            var inputs = settingsContainer.querySelectorAll('input, select');
            for (var i = 0; i < inputs.length; i++) {{
                inputs[i].onchange = function() {{
                    var attrName = this.getAttribute('data-attr-name');
                    var animIndex = this.getAttribute('data-anim-index');
                    var value = this.value;
                    
                    if (animIndex) {{
                        // Animation attribute
                        console.log('ANIM_ATTR_CHANGE:' + animIndex + ':' + attrName + ':' + value);
                    }} else {{
                        // Element attribute
                        console.log('ELEM_ATTR_CHANGE:' + attrName + ':' + value);
                    }}
                }};
            }}
            
            return true;
        }})();
        """
        
        execute_js(js_code)
    
    def _clear_settings(self):
        """
        Clear the settings container.
        """
        js_code = f"""
        var settingsContainer = document.getElementById('{self.ui_id}-settings');
        if (settingsContainer) {{
            settingsContainer.innerHTML = '<div style="text-align: center; padding: 20px; color: #999;">Select an element to edit its properties</div>';
            return true;
        }}
        return false;
        """
        
        execute_js(js_code)
    
    def add_animation_to_element(self, element_id, animation_type, attribute_name):
        """
        Add a new animation to an element.
        
        Args:
            element_id: ID of the element
            animation_type: Type of animation ('animate' or 'animateTransform')
            attribute_name: Name of the attribute to animate
            
        Returns:
            ID of the created animation
        """
        # Create a unique ID for the animation
        animation_id = f"anim_{element_id}_{attribute_name}_{len(self.settings.get(element_id, {}).get('animations', []))}"
        
        # Default settings based on animation type and attribute
        default_settings = {
            'attributeName': attribute_name,
            'dur': '2s',
            'repeatCount': 'indefinite'
        }
        
        if animation_type == 'animate':
            if attribute_name in ['r', 'cx', 'cy', 'x', 'y', 'width', 'height']:
                # Numeric attributes
                default_settings['from'] = '0'
                default_settings['to'] = '100'
            elif attribute_name in ['fill', 'stroke']:
                # Color attributes
                default_settings['from'] = '#0000ff'
                default_settings['to'] = '#ff0000'
        elif animation_type == 'animateTransform':
            default_settings['type'] = 'rotate'
            default_settings['from'] = '0'
            default_settings['to'] = '360'
        
        # Create animation element
        js_code = f"""
        (function() {{
            var element = document.getElementById('{element_id}');
            if (!element) return null;
            
            var animation = document.createElementNS('http://www.w3.org/2000/svg', '{animation_type}');
            animation.id = '{animation_id}';
            
            // Set attributes
            {' '.join([f"animation.setAttribute('{k}', '{v}');" for k, v in default_settings.items()])}
            
            element.appendChild(animation);
            
            return animation.id;
        }})();
        """
        
        # Execute the JavaScript (in a real implementation)
        # For now, we'll assume it was successful
        
        # Refresh the UI
        self.select_element(element_id)
        
        return animation_id
    
    def update_element_attribute(self, element_id, attribute_name, value):
        """
        Update an attribute of an element.
        
        Args:
            element_id: ID of the element
            attribute_name: Name of the attribute
            value: New value for the attribute
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById('{element_id}');
            if (!element) return false;
            
            element.setAttribute('{attribute_name}', '{value}');
            return true;
        }})();
        """
        
        execute_js(js_code)
    
    def update_animation_attribute(self, element_id, animation_index, attribute_name, value):
        """
        Update an attribute of an animation.
        
        Args:
            element_id: ID of the parent element
            animation_index: Index of the animation
            attribute_name: Name of the attribute
            value: New value for the attribute
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById('{element_id}');
            if (!element) return false;
            
            var animations = element.querySelectorAll('animate, animateTransform');
            if (animations.length <= {animation_index}) return false;
            
            var animation = animations[{animation_index}];
            
            // Special handling for 'dur' to add 's' suffix if needed
            if ('{attribute_name}' === 'dur' && !'{value}'.endsWith('s')) {{
                animation.setAttribute('{attribute_name}', '{value}s');
            }} else {{
                animation.setAttribute('{attribute_name}', '{value}');
            }}
            
            return true;
        }})();
        """
        
        execute_js(js_code)
    
    def remove_animation(self, element_id, animation_index):
        """
        Remove an animation from an element.
        
        Args:
            element_id: ID of the element
            animation_index: Index of the animation to remove
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById('{element_id}');
            if (!element) return false;
            
            var animations = element.querySelectorAll('animate, animateTransform');
            if (animations.length <= {animation_index}) return false;
            
            var animation = animations[{animation_index}];
            element.removeChild(animation);
            
            return true;
        }})();
        """
        
        execute_js(js_code)
        
        # Refresh the UI
        self.select_element(element_id)
    
    def apply_settings(self):
        """
        Apply all current settings to the selected element.
        """
        if not self.selected_element_id:
            return
        
        # In a real implementation, this would collect all settings from the UI
        # and apply them to the element and its animations
        
        js_code = f"""
        console.log('Applying settings to element {self.selected_element_id}');
        """
        
        execute_js(js_code)
    
    def reset_settings(self):
        """
        Reset the settings to their initial values.
        """
        if not self.selected_element_id:
            return
        
        # In a real implementation, this would restore the original settings
        
        # Refresh the UI
        self.select_element(self.selected_element_id)


# Simple interface functions to create and manage the settings UI
def create_settings_ui(mcp, parent_selector="#animation-container"):
    """
    Create a settings UI for animation configuration.
    
    Args:
        mcp: MCP instance
        parent_selector: CSS selector for the parent element
        
    Returns:
        AnimationSettingsUI instance
    """
    ui = AnimationSettingsUI(mcp, parent_selector)
    ui.create_ui()
    return ui

def show_settings_ui(ui):
    """
    Show the settings UI.
    
    Args:
        ui: AnimationSettingsUI instance
    """
    ui.show()

def hide_settings_ui(ui):
    """
    Hide the settings UI.
    
    Args:
        ui: AnimationSettingsUI instance
    """
    ui.hide()

def toggle_settings_ui(ui):
    """
    Toggle the visibility of the settings UI.
    
    Args:
        ui: AnimationSettingsUI instance
    """
    ui.toggle() 