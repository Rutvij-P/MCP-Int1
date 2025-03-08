from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="svg-animation-mcp",
    version="0.2.0",
    author="SVG Animation MCP Team",
    author_email="your.email@example.com",
    description="A Machine Communication Protocol (MCP) for SVG animations with real-time editing",
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
        "flask>=2.0.0,<3.0.0",
        "flask-socketio>=5.3.0,<6.0.0",
        "eventlet>=0.33.0,<1.0.0",
    ],
) 