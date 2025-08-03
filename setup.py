#!/usr/bin/env python3
# Save as: setup.py (in root directory)

"""
Setup script to create the new folder structure and migrate existing files.
"""

import os
import shutil
from pathlib import Path

def setup_directory_structure():
    """Create the new directory structure"""

    print("Setting up HermesDock document collaboration structure...")
    print("=" * 50)

    # Define directory structure
    directories = [
        "modules",
        "dist",
        "dist/docx",
        "dist/pdfs",
        "changeLogs",
        "downloadedChanges",
        "pythonScripts",
        "pythonScripts/data"
    ]

    # Create directories
    for dir_name in directories:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_name}/")

    # Create initial changelog
    changelog_path = Path("changeLogs/CHANGELOG.md")
    if not changelog_path.exists():
        with open(changelog_path, 'w') as f:
            f.write("# Changelog\n\n")
            f.write("All notable changes to the HermesDock documentation will be documented in this file.\n\n")
            f.write("## [4.0] - Initial Modular Version\n\n")
            f.write("### Added\n")
            f.write("- Modular documentation structure\n")
            f.write("- Dynamic build system with YAML configuration\n")
            f.write("- Organized folder structure\n\n")
        print(f"✓ Created: {changelog_path}")

    # Create README for downloadedChanges
    downloaded_readme = Path("downloadedChanges/README.md")
    if not downloaded_readme.exists():
        with open(downloaded_readme, 'w') as f:
            f.write("# Downloaded Changes\n\n")
            f.write("This directory stores changes and updates downloaded from AI chat sessions.\n\n")
            f.write("## Naming Convention\n")
            f.write("- `YYYY-MM-DD_description.md` - For dated changes\n")
            f.write("- `module_name_changes.md` - For module-specific changes\n")
        print(f"✓ Created: {downloaded_readme}")

    print("\n✓ Directory structure created successfully!")

def create_wrapper_scripts():
    """Create the main hermesdock.sh script"""

    print("\nCreating main script...")

    # hermesdock.sh is created separately and should already exist
    if os.path.exists("hermesdock.sh"):
        print("✓ hermesdock.sh already exists")
    else:
        print("⚠ hermesdock.sh not found - please create it manually")

# def create_sample_modules():
#     """Create sample module files to demonstrate the structure"""
#
#     print("\nCreating sample modules...")
#
#     samples = [
#         ("CSA-00-overview.md", "# Component Strategy Assessment Framework Overview\n\n<!-- Add overview content here -->"),
#         ("PRD-00-executive-summary.md", "# Product Requirements Executive Summary\n\n<!-- Add PRD executive summary here -->"),
#         ("STRATEGY-00-executive-summary.md", "# Strategy Executive Summary\n\n<!-- Add strategy executive summary here -->"),
#         ("Shared-glossary.md", "# Glossary\n\n<!-- Add common terms and definitions here -->"),
#         ("Shared-version-history.md", "# Version History\n\n## Version 4.0\n- Initial modular structure"),
#         ("Shared-references.md", "# References\n\n<!-- Add external references here -->")
#     ]
#
#     modules_dir = Path("modules")
#     for filename, content in samples:
#         filepath = modules_dir / filename
#         if not filepath.exists():
#             with open(filepath, 'w') as f:
#                 f.write(content)
#             print(f"✓ Created sample: {filename}")

def create_gitignore():
    """Create a .gitignore file for the project"""

    gitignore_content = """# Build output
dist/

# Backups
backups/
*.backup

# Python
__pycache__/
*.py[cod]
*$py.class
*.pyc

# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.temp
temp_*
"""

    with open(".gitignore", 'w') as f:
        f.write(gitignore_content)
    print("\n✓ Created .gitignore")

def create_main_readme():
    """Create the main README file"""

    readme_content = """# HermesDock - Focused Document Collaboration

## Overview

HermesDock is a powerful document collaboration tool that enables focused editing while maintaining full document context.
It allows users to work on individual sections while AI has access to the complete document, enabling targeted regeneration and seamless integration of changes back into the main document.

## Directory Structure

```
HermesDock/
├── modules/              # All modular documentation files
├── dist/                 # Built documentation (generated)
├── changeLogs/          # Version history and changelogs
├── downloadedChanges/   # Changes from AI chat sessions
├── pythonScripts/       # Build and helper scripts
└── pythonScripts/data/  # Document configuration files
```

## Quick Start

1. **Build all documents:**
   ```bash
   ./hermesdock.sh build
   ```

2. **Build specific document:**
   ```bash
   ./hermesdock.sh build <doc_name>
   ```

3. **Validate modules:**
   ```bash
   ./hermesdock.sh validate
   ```

4. **List available configurations:**
   ```bash
   ./hermesdock.sh list
   ```

## Adding New Documents

1. Create a configuration file in `pythonScripts/data/newdoc.yaml`
2. Define the document structure (see existing configs for examples)
3. Create module files in `modules/` with the appropriate prefix
4. Run `./hermesdock.sh build <doc_name>` to build

## Module Naming Convention

`PREFIX-description.md`

- **PREFIX**: Document identifier (USERGUIDE, API, MANUAL, etc.)
- **description**: Brief description of the module content
- **Ordering**: Controlled by map files (`PREFIX_map.yaml`) for flexibility

## Configuration Files

Document structures are defined in YAML files in `pythonScripts/data/`. 
Each configuration specifies:
- Output filename
- Document title
- Module prefix
- Document outline with module IDs and headings

See existing configuration files for examples.
"""

    with open("README.md", 'w') as f:
        f.write(readme_content)
    print("✓ Created README.md")

def create_default_configs():
    """Create default YAML configuration files"""

    print("\nCreating default configuration files...")

    # Import the config creation script
    import sys
    sys.path.append('pythonScripts')

    try:
        from create_configs import main as create_configs
        create_configs()
    except:
        # If import fails, create a minimal notice
        config_dir = Path("pythonScripts/data")
        readme_path = config_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write("# Configuration Files\n\n")
            f.write("Run `python3 pythonScripts/create_configs.py` to create default configurations.\n")
        print("✓ Created configuration README")

def main():
    print("HermesDock Document Collaboration Setup")
    print("=" * 50)

    # Setup directory structure
    setup_directory_structure()

    # Create wrapper scripts
    create_wrapper_scripts()

    # # Create sample modules
    # create_sample_modules()

    # Create .gitignore
    create_gitignore()

    # Create main README
    create_main_readme()

    # Note: Configurations will be created when users split documents
    print("\nNote: Document configurations will be created when you split documents.")
    print("Run './hermesdock.sh setup-configs' when you're ready to create configurations.")

    print("\n✓ Setup complete!")
    print("\nNext steps:")
    print("1. Create document configurations when needed:")
    print("   ./hermesdock.sh setup-configs")
    print("2. Split your documents into modules:")
    print("   ./hermesdock.sh split 'your-document.md' --config <config_name>")
    print("3. Run ./hermesdock.sh build to generate all documents")
    print("4. Check dist/ for the output files")

if __name__ == "__main__":
    main()
