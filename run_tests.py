#!/usr/bin/env python3
"""
Test runner script for SVG Animation MCP.

This script provides an easy way to run tests with different configurations.

Usage:
    python run_tests.py [OPTIONS]

Options:
    --all           Run all tests, including browser tests
    --unit          Run only unit tests (default)
    --performance   Run performance tests
    --browser       Run browser tests (requires browser environment)
    --coverage      Generate coverage report
    --verbose, -v   Verbose output
"""
import argparse
import os
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Run tests for SVG Animation MCP")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--browser", action="store_true", help="Run browser tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Default to unit tests if no specific test type is specified
    if not any([args.all, args.unit, args.performance, args.browser]):
        args.unit = True
    
    # Set up the pytest command
    pytest_cmd = ["pytest"]
    
    # Add verbosity option
    if args.verbose:
        pytest_cmd.append("-v")
    
    # Add coverage if requested
    if args.coverage:
        pytest_cmd.extend(["--cov=.", "--cov-report=term", "--cov-report=html"])
    
    # Filter tests based on options
    if args.all:
        # Run all tests
        os.environ["FULL_BROWSER_TESTS"] = "true"
        os.environ["BROWSER_TESTS"] = "true"
    elif args.unit:
        # Run only unit tests (exclude browser and performance tests)
        pytest_cmd.append("-m not browser")
        pytest_cmd.append("tests/test_mcp_core.py tests/test_svg.py tests/test_animation.py tests/test_utils.py tests/test_browser_integration.py")
    elif args.performance:
        # Run only performance tests
        pytest_cmd.append("tests/test_performance.py")
    elif args.browser:
        # Run only browser tests
        os.environ["FULL_BROWSER_TESTS"] = "true"
        os.environ["BROWSER_TESTS"] = "true"
        pytest_cmd.append("-m browser")
    
    # Run the tests
    print(f"Running command: {' '.join(pytest_cmd)}")
    result = subprocess.run(pytest_cmd)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main()) 