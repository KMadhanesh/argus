# argus/setup.py

from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of your requirements file
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    # --- Project Metadata ---
    name="orpheus-assistant",
    version="0.1.0",
    author="theArchitectEngineer101",
    author_email="techproblems.solver@gmail.com",
    description="An AI assistant for development, automation, and system orchestration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theArchitectEngineer101/argus", # URL do seu repositório Argus

    # --- Package Configuration ---
    # find_packages() automatically discovers all packages (folders with __init__.py)
    packages=find_packages(),
    
    # Tells Python where to look for the packages
    package_dir={'': '.'},

    # --- Dependencies ---
    # Reads dependencies from the requirements.txt file
    install_requires=requirements,

    # --- Entry Point ---
    # This is the key part that creates the command-line tool.
    # It maps the command 'orpheus' to the 'main' function inside the 'orpheus_core' module.
    entry_points={
        'console_scripts': [
            'orpheus = orpheus.orpheus_core:main',
        ],
    },

    # --- Classifiers ---
    # Provides metadata to PyPI (Python Package Index)
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires='>=3.10',
)