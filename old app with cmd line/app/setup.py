"""
Setup script for Smart Notes Widget
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Smart Notes Widget - A modern desktop sticky notes application"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="smart-notes-widget",
    version="1.0.0",
    description="A modern desktop sticky notes widget application",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Smart Notes Team",
    author_email="support@smartnotes.com",
    url="https://github.com/smartnotes/widget",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'smart-notes=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment",
        "Topic :: Text Editors",
        "Topic :: Utilities",
    ],
    keywords="sticky notes, desktop widget, productivity, notes",
    project_urls={
        "Bug Reports": "https://github.com/smartnotes/widget/issues",
        "Source": "https://github.com/smartnotes/widget",
        "Documentation": "https://github.com/smartnotes/widget/blob/main/README.md",
    },
) 