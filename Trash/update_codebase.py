#!/usr/bin/env python3
"""
SVG Animation MCP Codebase Update Script

This script helps users update their existing code to be compatible
with the latest version of the SVG Animation MCP library.

It scans Python files in the specified directory (current directory by default)
and applies necessary updates to the code.
"""

import argparse
import os
import re
import sys
from typing import List, Dict, Tuple
import shutil


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Update SVG Animation MCP codebase')
    parser.add_argument('--directory', '-d', type=str, default='.',
                        help='Directory containing Python files to update (default: current directory)')
    parser.add_argument('--backup', '-b', action='store_true',
                        help='Create backup files (.bak) before modifying')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be changed without modifying files')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed information about changes')
    return parser.parse_args()


def find_python_files(directory: str) -> List[str]:
    """
    Find all Python files in the specified directory and its subdirectories.
    
    Args:
        directory: Directory to scan
        
    Returns:
        List of Python file paths
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def backup_file(file_path: str):
    """
    Create a backup of a file.
    
    Args:
        file_path: Path to the file to back up
    """
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")


def update_imports(content: str, verbose: bool) -> Tuple[str, bool]:
    """
    Update import statements in the content.
    
    Args:
        content: File content
        verbose: Whether to show detailed information
        
    Returns:
        Tuple of (updated content, whether changes were made)
    """
    changes_made = False
    
    # Update browser_integration imports
    pattern = r'from browser_integration import (.*?)\n'
    match = re.search(pattern, content)
    if match:
        imports = match.group(1)
        if 'BrowserIntegrationError' not in imports and 'execute_js' in imports:
            new_imports = imports.strip()
            if new_imports:
                new_imports += ', BrowserIntegrationError'
            else:
                new_imports = 'BrowserIntegrationError'
            new_line = f'from browser_integration import {new_imports}\n'
            content = re.sub(pattern, new_line, content)
            changes_made = True
            if verbose:
                print(f"Updated browser_integration import: {new_line.strip()}")
    
    # Update svg_animation_mcp imports
    pattern = r'from svg_animation_mcp import (.*?)\n'
    match = re.search(pattern, content)
    if match:
        imports = match.group(1)
        if 'MCPError' not in imports and 'MCP' in imports:
            new_imports = imports.strip()
            if new_imports:
                new_imports += ', MCPError'
            else:
                new_imports = 'MCPError'
            new_line = f'from svg_animation_mcp import {new_imports}\n'
            content = re.sub(pattern, new_line, content)
            changes_made = True
            if verbose:
                print(f"Updated svg_animation_mcp import: {new_line.strip()}")
    
    # Update utils imports
    pattern = r'from utils import (.*?)\n'
    match = re.search(pattern, content)
    if match:
        imports = match.group(1)
        for new_util in ['validate_color', 'validate_number', 'escape_js_string']:
            if new_util not in imports:
                new_imports = imports.strip()
                if new_imports:
                    new_imports += f', {new_util}'
                else:
                    new_imports = new_util
                new_line = f'from utils import {new_imports}\n'
                content = re.sub(pattern, new_line, content)
                changes_made = True
                if verbose:
                    print(f"Updated utils import: {new_line.strip()}")
    
    return content, changes_made


def update_error_handling(content: str, verbose: bool) -> Tuple[str, bool]:
    """
    Add error handling to code using MCP.
    
    Args:
        content: File content
        verbose: Whether to show detailed information
        
    Returns:
        Tuple of (updated content, whether changes were made)
    """
    changes_made = False
    
    # Simple pattern to detect if there's already try/except blocks
    has_try_except = re.search(r'\btry\s*:', content) is not None
    
    # If there's no error handling and there are MCP method calls, wrap in try/except
    if (not has_try_except and 
        (re.search(r'mcp\s*=\s*MCP\(\)', content) is not None) and
        (re.search(r'(?:execute_js|create_svg|add_rectangle|add_circle|add_path|add_text)\(', content) is not None)):
        
        # Find the main code block
        main_pattern = r'(?:^|\n)(?:if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:|\s*def\s+main\s*\(\s*\)\s*:)(.*?)(?=\n\S|\Z)'
        match = re.search(main_pattern, content, re.DOTALL)
        
        if match:
            main_block = match.group(1)
            indentation = re.match(r'(\s*)', main_block).group(1)
            
            # Wrap the block in try/except
            wrapped_block = f"{indentation}try:{main_block}"
            
            # Add except blocks
            wrapped_block += f"\n{indentation}except MCPError as e:"
            wrapped_block += f"\n{indentation}    print(f\"MCP Error: {{e}}\")"
            wrapped_block += f"\n{indentation}except BrowserIntegrationError as e:"
            wrapped_block += f"\n{indentation}    print(f\"Browser Integration Error: {{e}}\")"
            wrapped_block += f"\n{indentation}except Exception as e:"
            wrapped_block += f"\n{indentation}    print(f\"Unexpected error: {{e}}\")"
            
            # Replace the original block
            content = re.sub(main_pattern, f"\nif __name__ == \"__main__\":{wrapped_block}", content, flags=re.DOTALL)
            changes_made = True
            if verbose:
                print("Added error handling with try/except blocks")
    
    return content, changes_made


def update_animation_calls(content: str, verbose: bool) -> Tuple[str, bool]:
    """
    Update animation method calls to use the new API.
    
    Args:
        content: File content
        verbose: Whether to show detailed information
        
    Returns:
        Tuple of (updated content, whether changes were made)
    """
    changes_made = False
    
    # Update animation attribute calls
    pattern = r'([a-zA-Z0-9_]+)\.animate\([\'"]([a-zA-Z0-9_-]+)[\'"],\s*[\'"]([^\'"]*)[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*,'
    for match in re.finditer(pattern, content):
        obj, attr, from_val, to_val = match.groups()
        
        # If values are strings without variables, we need to validate them
        if attr.lower() in ('fill', 'stroke') and not re.search(r'\{|\$|\+', from_val):
            new_pattern = f'{obj}.animate(\'{attr}\', \'{from_val}\', \'{to_val}\','
            new_content = f'{obj}.animate(\'{attr}\', validate_color(\'{from_val}\'), validate_color(\'{to_val}\'),'
            
            # Only replace the specific instance
            content = content.replace(new_pattern, new_content, 1)
            changes_made = True
            if verbose:
                print(f"Updated color animation call: {new_content}")
    
    # Update animation transform calls
    pattern = r'([a-zA-Z0-9_]+)\.animate_transform\([\'"]([a-zA-Z0-9_-]+)[\'"],\s*'
    for match in re.finditer(pattern, content):
        obj, transform_type = match.groups()
        
        # Check if transform type is valid
        if transform_type not in ['translate', 'scale', 'rotate', 'skewX', 'skewY']:
            old_transform = f'{obj}.animate_transform(\'{transform_type}\','
            new_transform = f'# Warning: Invalid transform type \'{transform_type}\'\n    {old_transform}'
            
            # Only replace the specific instance
            content = content.replace(old_transform, new_transform, 1)
            changes_made = True
            if verbose:
                print(f"Marked invalid transform type: {transform_type}")
    
    return content, changes_made


def update_file(file_path: str, backup: bool, dry_run: bool, verbose: bool) -> bool:
    """
    Update a single Python file.
    
    Args:
        file_path: Path to the file to update
        backup: Whether to create a backup
        dry_run: Whether to actually modify the file
        verbose: Whether to show detailed information
        
    Returns:
        Whether changes were made
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        changes_made = False
        
        # Apply updates
        content, imports_changed = update_imports(content, verbose)
        changes_made = changes_made or imports_changed
        
        content, error_handling_changed = update_error_handling(content, verbose)
        changes_made = changes_made or error_handling_changed
        
        content, animation_calls_changed = update_animation_calls(content, verbose)
        changes_made = changes_made or animation_calls_changed
        
        if changes_made and not dry_run:
            if backup:
                backup_file(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Updated: {file_path}")
        elif changes_made and dry_run:
            print(f"Would update: {file_path}")
        elif verbose:
            print(f"No changes needed: {file_path}")
            
        return changes_made
    
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False


def main():
    """Main entry point for the script."""
    args = parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return 1
    
    python_files = find_python_files(args.directory)
    if not python_files:
        print(f"No Python files found in {args.directory}")
        return 0
    
    print(f"Found {len(python_files)} Python files to scan")
    
    if args.dry_run:
        print("Dry run mode - no files will be modified")
    
    updated_files = 0
    for file_path in python_files:
        if update_file(file_path, args.backup, args.dry_run, args.verbose):
            updated_files += 1
    
    if args.dry_run:
        print(f"Would update {updated_files} files")
    else:
        print(f"Updated {updated_files} files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 