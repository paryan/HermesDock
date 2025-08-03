#!/usr/bin/env python3
# Save as: pythonScripts/new_doc.py

"""
Script to generate a new document configuration and create initial module files.
"""

import os
import yaml
import re
from pathlib import Path

def generate_prefix(title):
    """Generate a prefix from the document title"""
    # Extract significant words and take first letter of each
    words = re.findall(r'\b[A-Z][a-z]+|\b[A-Z]+\b', title)
    if len(words) >= 2:
        prefix = ''.join(w[0] for w in words[:4])  # Max 4 letters
    else:
        # Fallback: use first 3-4 characters
        prefix = re.sub(r'[^A-Z]', '', title.upper())[:4]
    
    return prefix.upper()

def sanitize_filename(text):
    """Convert text to a safe filename"""
    # Remove special characters and replace spaces with hyphens
    safe = re.sub(r'[^\w\s-]', '', text)
    safe = re.sub(r'[-\s]+', '-', safe)
    return safe.lower().strip('-')

def create_document_config():
    """Interactive script to create a new document configuration"""
    
    print("New Document Configuration Generator")
    print("=" * 50)
    
    # Get document information
    print("\n1. Basic Information")
    title = input("Document title: ").strip()
    
    # Generate filename
    default_filename = f"{title.replace(' ', '_')}.md"
    filename = input(f"Output filename [{default_filename}]: ").strip()
    if not filename:
        filename = default_filename
    
    # Generate prefix
    auto_prefix = generate_prefix(title)
    prefix = input(f"Document prefix [{auto_prefix}]: ").strip().upper()
    if not prefix:
        prefix = auto_prefix
    
    # Get configuration name
    config_name = input("Configuration name (e.g., 'roadmap', 'architecture'): ").strip().lower()
    config_name = sanitize_filename(config_name)
    
    # Document outline
    print("\n2. Document Outline")
    print("Enter sections one by one. Press Enter with empty ID to finish.")
    
    outline = []
    index = 0
    
    while True:
        print(f"\nSection {index + 1}:")
        section_id = input("  Section ID (e.g., 'executive-summary'): ").strip()
        if not section_id:
            break
        
        section_id = sanitize_filename(section_id)
        heading = input("  Section heading: ").strip()
        
        # For pattern detection
        start_pattern = input("  Start pattern in source doc (optional): ").strip()
        
        outline.append({
            'id': section_id,
            'heading': heading,
            'start_pattern': start_pattern if start_pattern else f"## {heading}",
            'end_pattern': None  # Will be filled in next iteration
        })
        
        # Set end pattern for previous section
        if index > 0:
            outline[index - 1]['end_pattern'] = start_pattern if start_pattern else f"## {heading}"
        
        index += 1
    
    # Create configuration
    config = {
        'filename': filename,
        'prefix': prefix,
        'title': title,
        'document_outline': outline
    }
    
    # Save configuration
    config_dir = Path(__file__).parent / "data"
    config_dir.mkdir(exist_ok=True)
    
    config_path = config_dir / f"{config_name}.yaml"
    
    # Check if file exists
    if config_path.exists():
        overwrite = input(f"\n{config_name}.yaml already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Cancelled.")
            return
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"\n✓ Created configuration: {config_path}")
    
    # Create module files
    create_modules = input("\nCreate empty module files? (y/n): ")
    if create_modules.lower() == 'y':
        create_module_files(config)
    
    print("\n✓ Document configuration complete!")
    print(f"\nTo build this document: python3 pythonScripts/build.py build --doc {config_name}")

def create_module_files(config):
    """Create empty module files based on configuration"""
    
    modules_dir = Path.cwd() / "modules"
    modules_dir.mkdir(exist_ok=True)
    
    prefix = config['prefix']
    outline = config['document_outline']
    
    print("\nCreating module files...")
    
    for index, section in enumerate(outline):
        module_filename = f"{prefix}-{index:02d}-{section['id']}.md"
        module_path = modules_dir / module_filename
        
        if not module_path.exists():
            with open(module_path, 'w') as f:
                f.write(f"# {section['heading']}\n\n")
                f.write(f"<!-- Content for {section['id']} section -->\n\n")
            print(f"  ✓ Created: {module_filename}")
        else:
            print(f"  ⚠ Exists: {module_filename}")

def list_configurations():
    """List all existing document configurations"""
    
    config_dir = Path(__file__).parent / "data"
    configs = list(config_dir.glob("*.yaml"))
    
    if not configs:
        print("No document configurations found.")
        return
    
    print("\nExisting Document Configurations:")
    print("-" * 50)
    
    for config_file in sorted(configs):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"\n{config_file.stem}:")
        print(f"  Title: {config['title']}")
        print(f"  Prefix: {config['prefix']}")
        print(f"  Sections: {len(config['document_outline'])}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Create new document configurations')
    parser.add_argument('--list', action='store_true', 
                       help='List existing configurations')
    
    args = parser.parse_args()
    
    if args.list:
        list_configurations()
    else:
        create_document_config()

if __name__ == "__main__":
    main()