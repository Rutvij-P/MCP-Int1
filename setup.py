from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="svg-animation-mcp",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Machine Communication Protocol (MCP) for SVG animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/svg-animation-mcp",
    package_dir={"": "src"},
    packages=["mcp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Optional dependencies for using as a standalone application
        "selenium>=4.1.0",
        "webdriver-manager>=3.8.0",
    ],
) 