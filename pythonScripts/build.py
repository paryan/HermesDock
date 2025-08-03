#!/usr/bin/env python3
# Save as: pythonScripts/build.py

"""
Dynamic document build system that uses configuration files
to build modular documents into complete markdown files.
Now uses map-based ordering instead of numerical prefixes.
"""

import os
import sys
import yaml
import argparse
from datetime import datetime
from pathlib import Path

class DocumentBuilder:
    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()
        self.modules_dir = self.root_dir / "modules"
        self.dist_dir = self.root_dir / "dist"
        self.config_dir = Path(__file__).parent / "data"
        
        # Create directories if they don't exist
        self.modules_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load document configuration from YAML file"""
        config_path = self.config_dir / config_file
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_module_map(self, config_name):
        """Load module map for a document"""
        map_path = self.modules_dir / f"{config_name}_map.yaml"
        if map_path.exists():
            with open(map_path, 'r') as f:
                return yaml.safe_load(f)
        return None
    
    def get_module_filename(self, prefix, module_id):
        """Generate module filename without numerical prefix"""
        return f"{prefix}-{module_id}.md"
    
    def build_document(self, config_name):
        """Build a document based on its configuration and module map"""
        # Load configuration
        config = self.load_config(f"{config_name}.yaml")
        
        prefix = config['prefix']
        filename = config['filename']
        title = config['title']
        outline = config['document_outline']
        
        # Load module map if it exists
        module_map = self.load_module_map(config_name)
        
        print(f"\nBuilding {config_name.upper()} document...")
        print(f"Output: {filename}")
        print("-" * 50)
        
        # Start building the document
        output_path = self.dist_dir / filename
        with open(output_path, 'w') as output:
            # Write header
            output.write(f"# {title}\n\n")
            output.write(f"<!-- This document was automatically generated from modular components -->\n")
            output.write(f"<!-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
            
            # Process each module based on map or outline
            modules_found = 0
            module_order = self.get_module_order(outline, module_map)
            
            for index, module_id in enumerate(module_order):
                module_file = self.get_module_filename(prefix, module_id)
                module_path = self.modules_dir / module_file
                
                if module_path.exists():
                    # Add separator between sections (except for first)
                    if index > 0:
                        output.write("\n---\n\n")
                    
                    # Write module content
                    with open(module_path, 'r') as module_content:
                        output.write(module_content.read())
                        output.write("\n")
                    
                    modules_found += 1
                    print(f"  ✓ Added: {module_file}")
                else:
                    print(f"  ⚠ Missing: {module_file}")
        
        print(f"\n✓ Built {filename} with {modules_found}/{len(module_order)} modules")
        return output_path
    
    def get_module_order(self, outline, module_map):
        """Get module order from map or fallback to outline"""
        if module_map and 'module_order' in module_map:
            return module_map['module_order']
        else:
            # Fallback to outline order
            return [module['id'] for module in outline]
    
    def build_all(self):
        """Build all documents based on available configurations"""
        config_files = list(self.config_dir.glob("*.yaml"))
        
        if not config_files:
            print("No configuration files found in pythonScripts/data/")
            print("Run './hermesdock.sh setup-configs' to create default configurations")
            return
        
        print(f"\nFound {len(config_files)} document configurations")
        
        for config_file in config_files:
            config_name = config_file.stem
            try:
                self.build_document(config_name)
            except Exception as e:
                print(f"\n✗ Error building {config_name}: {e}")
        
        print(f"\n✓ All documents built in {self.dist_dir}/")
    
    def list_configs(self):
        """List all available document configurations"""
        config_files = list(self.config_dir.glob("*.yaml"))
        
        if not config_files:
            print("\nNo configuration files found in pythonScripts/data/")
            print("Run './hermesdock.sh setup-configs' to create default configurations")
            return
        
        print("\nAvailable document configurations:")
        print("-" * 50)
        
        for config_file in config_files:
            config = self.load_config(config_file.name)
            print(f"\n{config_file.stem}:")
            print(f"  Prefix: {config['prefix']}")
            print(f"  Output: {config['filename']}")
            print(f"  Modules: {len(config['document_outline'])}")
            
            # Check if map exists
            map_path = self.modules_dir / f"{config_file.stem}_map.yaml"
            if map_path.exists():
                print(f"  Map: ✓ {map_path.name}")
            else:
                print(f"  Map: ✗ No map file found")
    
    def validate_modules(self, config_name):
        """Validate that all required modules exist for a document"""
        config = self.load_config(f"{config_name}.yaml")
        prefix = config['prefix']
        outline = config['document_outline']
        module_map = self.load_module_map(config_name)
        
        print(f"\nValidating modules for {config_name.upper()}...")
        print("-" * 50)
        
        # Get module order
        module_order = self.get_module_order(outline, module_map)
        
        missing = 0
        for module_id in module_order:
            module_file = self.get_module_filename(prefix, module_id)
            module_path = self.modules_dir / module_file
            
            if module_path.exists():
                print(f"  ✓ {module_file}")
            else:
                print(f"  ✗ Missing: {module_file}")
                missing += 1
        
        if missing == 0:
            print(f"\n✓ All modules present for {config_name}")
        else:
            print(f"\n⚠ {missing} modules missing for {config_name}")
        
        return missing == 0
    
    def create_module_map(self, config_name):
        """Create a module map file for a document"""
        config = self.load_config(f"{config_name}.yaml")
        outline = config['document_outline']
        
        # Create map structure
        module_map = {
            'document_name': config_name,
            'prefix': config['prefix'],
            'module_order': [module['id'] for module in outline],
            'modules': {}
        }
        
        # Add module metadata
        for module in outline:
            module_map['modules'][module['id']] = {
                'heading': module.get('heading', ''),
                'description': module.get('description', ''),
                'start_pattern': module.get('start_pattern', ''),
                'end_pattern': module.get('end_pattern', '')
            }
        
        # Write map file
        map_path = self.modules_dir / f"{config_name}_map.yaml"
        with open(map_path, 'w') as f:
            yaml.dump(module_map, f, default_flow_style=False, indent=2)
        
        print(f"✓ Created module map: {map_path}")
        return map_path

def main():
    parser = argparse.ArgumentParser(description='Dynamic document build system')
    parser.add_argument('action', choices=['build', 'build-all', 'list', 'validate', 'create-map'],
                       help='Action to perform')
    parser.add_argument('--doc', help='Document name (for build/validate/create-map)')
    parser.add_argument('--root', help='Root directory (defaults to parent of script dir)')
    
    args = parser.parse_args()
    
    builder = DocumentBuilder(args.root)
    
    if args.action == 'build':
        if not args.doc:
            print("Error: --doc required for build action")
            sys.exit(1)
        builder.build_document(args.doc)
    
    elif args.action == 'build-all':
        builder.build_all()
    
    elif args.action == 'list':
        builder.list_configs()
    
    elif args.action == 'create-map':
        if not args.doc:
            print("Error: --doc required for create-map action")
            sys.exit(1)
        builder.create_module_map(args.doc)
    
    elif args.action == 'validate':
        if args.doc:
            builder.validate_modules(args.doc)
        else:
            # Validate all
            config_files = list(builder.config_dir.glob("*.yaml"))
            if not config_files:
                print("No configuration files found in pythonScripts/data/")
                print("Run './hermesdock.sh setup-configs' to create default configurations")
                sys.exit(1)
            
            all_valid = True
            for config_file in config_files:
                if not builder.validate_modules(config_file.stem):
                    all_valid = False
            
            if all_valid:
                print("\n✓ All documents have complete modules")
            else:
                print("\n⚠ Some documents have missing modules")

if __name__ == "__main__":
    main()