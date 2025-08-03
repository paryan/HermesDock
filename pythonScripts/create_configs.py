#!/usr/bin/env python3
# Save as: pythonScripts/create_configs.py

"""
Create YAML configuration files for document types.
Supports interactive creation and external configuration sources.
"""

import yaml
import json
from pathlib import Path

def create_empty_config():
    """Create an empty configuration template"""
    return {
        'filename': '',
        'prefix': '',
        'title': '',
        'document_outline': []
    }

def add_section_to_outline(outline, section_id, heading, start_pattern, end_pattern=None):
    """Add a section to the document outline"""
    outline.append({
        'id': section_id,
        'heading': heading,
        'start_pattern': start_pattern,
        'end_pattern': end_pattern
    })

def create_config_interactively():
    """Create a configuration interactively"""
    print("\nCreating new document configuration...")
    print("=" * 50)
    
    config = create_empty_config()
    
    # Get basic information
    config['filename'] = input("Output filename (e.g., My_Document.md): ").strip()
    config['prefix'] = input("Module prefix (e.g., MYDOC): ").strip().upper()
    config['title'] = input("Document title: ").strip()
    
    print(f"\nNow let's define the document sections for {config['prefix']}...")
    print("Enter section details (press Enter on section ID to finish):")
    
    outline = []
    section_num = 1
    
    while True:
        print(f"\n--- Section {section_num} ---")
        section_id = input("Section ID (e.g., overview, introduction): ").strip()
        
        if not section_id:
            break
            
        heading = input("Section heading: ").strip()
        start_pattern = input("Start pattern (e.g., '## Overview'): ").strip()
        end_pattern = input("End pattern (optional, press Enter to skip): ").strip()
        
        if not end_pattern:
            end_pattern = None
            
        add_section_to_outline(outline, section_id, heading, start_pattern, end_pattern)
        section_num += 1
    
    config['document_outline'] = outline
    return config

def load_config_from_file(file_path):
    """Load configuration from an external file (JSON or YAML)"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        if file_path.suffix.lower() == '.json':
            return json.load(f)
        else:
            return yaml.safe_load(f)

def create_config_from_template(template_name):
    """Create a configuration from a predefined template"""
    templates = {
        'basic': {
            'filename': 'Basic_Document.md',
            'prefix': 'BASIC',
            'title': 'Basic Document Template',
            'document_outline': [
                {
                    'id': 'introduction',
                    'heading': 'Introduction',
                    'start_pattern': '## Introduction',
                    'end_pattern': '## Main Content'
                },
                {
                    'id': 'main-content',
                    'heading': 'Main Content',
                    'start_pattern': '## Main Content',
                    'end_pattern': '## Conclusion'
                },
                {
                    'id': 'conclusion',
                    'heading': 'Conclusion',
                    'start_pattern': '## Conclusion',
                    'end_pattern': None
                }
            ]
        },
        'technical': {
            'filename': 'Technical_Document.md',
            'prefix': 'TECH',
            'title': 'Technical Document Template',
            'document_outline': [
                {
                    'id': 'overview',
                    'heading': 'Technical Overview',
                    'start_pattern': '## Overview',
                    'end_pattern': '## Architecture'
                },
                {
                    'id': 'architecture',
                    'heading': 'System Architecture',
                    'start_pattern': '## Architecture',
                    'end_pattern': '## Implementation'
                },
                {
                    'id': 'implementation',
                    'heading': 'Implementation Details',
                    'start_pattern': '## Implementation',
                    'end_pattern': '## Testing'
                },
                {
                    'id': 'testing',
                    'heading': 'Testing Strategy',
                    'start_pattern': '## Testing',
                    'end_pattern': '## Deployment'
                },
                {
                    'id': 'deployment',
                    'heading': 'Deployment Guide',
                    'start_pattern': '## Deployment',
                    'end_pattern': None
                }
            ]
        }
    }
    
    if template_name not in templates:
        raise ValueError(f"Template '{template_name}' not found. Available templates: {list(templates.keys())}")
    
    return templates[template_name]

def create_all_configs():
    """Create configuration files based on user choice"""
    
    # Ensure data directory exists
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    print("HermesDock Configuration Creator")
    print("=" * 50)
    print("\nChoose how to create configurations:")
    print("1. Interactive creation")
    print("2. Use predefined template")
    print("3. Load from external file")
    print("4. Create sample configurations (for testing)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    created_configs = []
    
    if choice == '1':
        # Interactive creation
        while True:
            config = create_config_interactively()
            config_name = input(f"\nSave as (e.g., {config['prefix'].lower()}): ").strip()
            
            if not config_name:
                break
                
            config_path = data_dir / f'{config_name}.yaml'
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"✓ Created: {config_path}")
            created_configs.append(config_name)
            
            another = input("\nCreate another configuration? (y/N): ").strip().lower()
            if another != 'y':
                break
    
    elif choice == '2':
        # Use template
        print("\nAvailable templates:")
        print("- basic: Simple document with intro, content, conclusion")
        print("- technical: Technical document with architecture, implementation, etc.")
        
        template_name = input("Enter template name: ").strip()
        config_name = input("Save as (e.g., mydoc): ").strip()
        
        try:
            config = create_config_from_template(template_name)
            config_path = data_dir / f'{config_name}.yaml'
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"✓ Created: {config_path}")
            created_configs.append(config_name)
        except ValueError as e:
            print(f"Error: {e}")
    
    elif choice == '3':
        # Load from external file
        file_path = input("Enter path to configuration file (JSON or YAML): ").strip()
        config_name = input("Save as (e.g., mydoc): ").strip()
        
        try:
            config = load_config_from_file(file_path)
            config_path = data_dir / f'{config_name}.yaml'
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"✓ Created: {config_path}")
            created_configs.append(config_name)
        except Exception as e:
            print(f"Error loading file: {e}")
    
    elif choice == '4':
        # Create sample configurations for testing
        sample_configs = {
            'sample1': {
                'filename': 'Sample_Document_1.md',
                'prefix': 'SAMPLE1',
                'title': 'Sample Document 1',
                'document_outline': [
                    {
                        'id': 'intro',
                        'heading': 'Introduction',
                        'start_pattern': '## Introduction',
                        'end_pattern': '## Section 1'
                    },
                    {
                        'id': 'section1',
                        'heading': 'Section 1',
                        'start_pattern': '## Section 1',
                        'end_pattern': '## Section 2'
                    },
                    {
                        'id': 'section2',
                        'heading': 'Section 2',
                        'start_pattern': '## Section 2',
                        'end_pattern': None
                    }
                ]
            },
            'sample2': {
                'filename': 'Sample_Document_2.md',
                'prefix': 'SAMPLE2',
                'title': 'Sample Document 2',
                'document_outline': [
                    {
                        'id': 'overview',
                        'heading': 'Overview',
                        'start_pattern': '## Overview',
                        'end_pattern': '## Details'
                    },
                    {
                        'id': 'details',
                        'heading': 'Details',
                        'start_pattern': '## Details',
                        'end_pattern': None
                    }
                ]
            }
        }
        
        for config_name, config_data in sample_configs.items():
            config_path = data_dir / f'{config_name}.yaml'
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
            
            print(f"✓ Created: {config_path}")
            created_configs.append(config_name)
    
    else:
        print("Invalid choice. Exiting.")
        return
    
    if created_configs:
        print(f"\n✓ Created {len(created_configs)} configuration(s)!")
        print("\nYou can now split your documents using:")
        print("  ./hermesdock.sh split 'document.md' --config <config_name>")
        print("\nCreated configurations:")
        for config_name in created_configs:
            print(f"  - {config_name}")
    else:
        print("\nNo configurations were created.")

def list_available_configs():
    """List all available configuration templates"""
    print("\nAvailable configuration templates:")
    print("-" * 50)
    print("\nPredefined templates:")
    print("- basic: Simple document with intro, content, conclusion")
    print("- technical: Technical document with architecture, implementation, etc.")
    print("\nYou can also:")
    print("- Create configurations interactively")
    print("- Load configurations from external files")
    print("- Use sample configurations for testing")

def main():
    """Main function to create configurations"""
    create_all_configs()

if __name__ == "__main__":
    main()