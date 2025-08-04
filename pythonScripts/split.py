#!/usr/bin/env python3
# Save as: pythonScripts/split.py

"""
Enhanced document splitter that uses YAML configuration files
to split large documents into modules.
Now creates files without numerical prefixes and generates a map file.
"""

import os
import re
import yaml
import argparse
from pathlib import Path

class ConfigBasedSplitter:
    def __init__(self, config_name, input_file=None):
        self.config_name = config_name
        self.config_dir = Path(__file__).parent / "data"
        self.modules_dir = Path.cwd() / "modules"
        self.modules_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self.load_config(input_file)
        
    def load_config(self, input_file=None):
        """Load the document configuration or create one if it doesn't exist"""
        config_path = self.config_dir / f"{self.config_name}.yaml"
        if not config_path.exists():
            print(f"Configuration not found: {config_path}")
            print("Creating configuration automatically...")
            return self.create_config_from_document(input_file)
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # If input_file is provided, validate that the configuration matches the document
        if input_file:
            if not self.validate_config_against_document(config, input_file):
                print(f"Configuration doesn't match document structure. Regenerating...")
                return self.create_config_from_document(input_file)
        
        return config
    
    def validate_config_against_document(self, config, input_file):
        """Validate that the configuration patterns match the document structure"""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Find all level 1, level 2, and level 3 headers in the document
        doc_headers_level1 = []
        doc_headers_level2 = []
        doc_headers_level3 = []
        for line in lines:
            match = re.match(r'^#\s+(.+)$', line)
            if match:
                doc_headers_level1.append(match.group(1))
            else:
                match = re.match(r'^##\s+(.+)$', line)
                if match:
                    doc_headers_level2.append(match.group(1))
                else:
                    match = re.match(r'^###\s+(.+)$', line)
                    if match:
                        doc_headers_level3.append(match.group(1))
        
        # Check if all configuration patterns exist in the document
        outline = config.get('document_outline', [])
        for section in outline:
            pattern = section.get('start_pattern', '')
            # Extract the heading from the pattern (remove #, ##, or ### prefix)
            if pattern.startswith('# '):
                heading = pattern[2:]
                if heading not in doc_headers_level1:
                    return False
            elif pattern.startswith('## '):
                heading = pattern[3:]
                if heading not in doc_headers_level2:
                    return False
            elif pattern.startswith('### '):
                heading = pattern[4:]
                if heading not in doc_headers_level3:
                    return False
        
        return True
    
    def create_config_from_document(self, input_file=None):
        """Create a configuration by analyzing the document structure"""
        
        if input_file is None:
            print("Creating basic configuration...")
            print("You can customize this later by editing the configuration file.")
            
            # Create a basic configuration
            config = {
                'filename': f"{self.config_name.title()}_Document.md",
                'prefix': self.config_name.upper(),
                'title': f"{self.config_name.title()} Document",
                'document_outline': [
                    {
                        'id': 'overview',
                        'heading': 'Overview',
                        'start_pattern': '## Overview',
                        'end_pattern': '## Next Section'
                    },
                    {
                        'id': 'content',
                        'heading': 'Main Content',
                        'start_pattern': '## Next Section',
                        'end_pattern': None
                    }
                ]
            }
        else:
            print(f"Analyzing document structure to create configuration...")
            
            # Read the document and extract headings
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Find all level 1, level 2, and level 3 headers (#, ##, and ###)
            level1_headers = []
            level2_headers = []
            level3_headers = []
            
            for i, line in enumerate(lines):
                match = re.match(r'^#\s+(.+)$', line)
                if match:
                    heading = match.group(1)
                    level1_headers.append((i, heading))
                else:
                    match = re.match(r'^##\s+(.+)$', line)
                    if match:
                        heading = match.group(1)
                        level2_headers.append((i, heading))
                    else:
                        match = re.match(r'^###\s+(.+)$', line)
                        if match:
                            heading = match.group(1)
                            level3_headers.append((i, heading))
            
            # Use level 1 headers if available, otherwise use level 2 headers, otherwise use level 3 headers
            if len(level1_headers) > 1:  # More than just the title
                print(f"Found {len(level1_headers)} level 1 headers, using those for sections.")
                headers_to_use = level1_headers
                header_prefix = '#'
            elif len(level2_headers) > 1:  # More than just a subtitle
                print(f"Found {len(level2_headers)} level 2 headers, using those for sections.")
                headers_to_use = level2_headers
                header_prefix = '##'
            elif len(level3_headers) > 0:
                print(f"Found {len(level3_headers)} level 3 headers, using those for sections.")
                headers_to_use = level3_headers
                header_prefix = '###'
            else:
                print("No suitable headers found. Creating basic configuration.")
                return self.create_config_from_document()
            
            # Create configuration based on actual headings
            document_outline = []
            for i, (line_idx, heading) in enumerate(headers_to_use):
                # Create a clean ID from the heading
                clean_id = re.sub(r'[^a-zA-Z0-9\s]', '', heading.lower())
                clean_id = re.sub(r'\s+', '_', clean_id.strip())
                
                # Determine end pattern
                if i < len(headers_to_use) - 1:
                    next_heading = headers_to_use[i + 1][1]
                    end_pattern = f'{header_prefix} {next_heading}'
                else:
                    end_pattern = None
                
                section = {
                    'id': clean_id,
                    'heading': heading,
                    'start_pattern': f'{header_prefix} {heading}',
                    'end_pattern': end_pattern
                }
                document_outline.append(section)
            
            # Create filename from document name
            doc_name = Path(input_file).stem
            filename = f"{doc_name.replace(' ', '_')}.md"
            
            config = {
                'filename': filename,
                'prefix': self.config_name.upper(),
                'title': doc_name,
                'document_outline': document_outline
            }
        
        # Save the configuration
        config_path = self.config_dir / f"{self.config_name}.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Created configuration: {config_path}")
        return config
    
    def split_document(self, input_file):
        """Split a document based on its configuration"""
        
        # Read the input document
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        prefix = self.config['prefix']
        outline = self.config['document_outline']
        
        print(f"\nSplitting document using {self.config_name} configuration...")
        print(f"Prefix: {prefix}")
        print("-" * 50)
        
        # Create module map
        module_map = {
            'document_name': self.config_name,
            'prefix': prefix,
            'module_order': [],
            'modules': {}
        }
        
        # Process each section
        for index, section in enumerate(outline):
            section_id = section['id']
            start_pattern = section['start_pattern']
            end_pattern = section.get('end_pattern')
            
            # Extract section content
            section_content = self.extract_section(lines, start_pattern, end_pattern)
            
            # Generate module filename (without numerical prefix)
            module_filename = f"{prefix}-{section_id}.md"
            module_path = self.modules_dir / module_filename
            
            # Write module file
            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(section_content)
            
            # Add to module map
            module_map['module_order'].append(section_id)
            module_map['modules'][section_id] = {
                'heading': section.get('heading', ''),
                'description': section.get('description', ''),
                'start_pattern': start_pattern,
                'end_pattern': end_pattern,
                'index': index
            }
            
            word_count = len(section_content.split())
            print(f"  ✓ Created: {module_filename} ({word_count} words)")
        
        # Write module map file
        map_filename = f"{self.config_name}_map.yaml"
        map_path = self.modules_dir / map_filename
        with open(map_path, 'w', encoding='utf-8') as f:
            yaml.dump(module_map, f, default_flow_style=False, indent=2)
        
        print(f"\n✓ Created module map: {map_filename}")
        print(f"✓ Split complete! {len(outline)} modules created in modules/")
        print(f"\nModule order (for AI reference):")
        for i, module_id in enumerate(module_map['module_order']):
            heading = module_map['modules'][module_id]['heading']
            print(f"  {i+1}. {module_id} - {heading}")
    
    def extract_section(self, lines, start_pattern, end_pattern):
        """Extract content between start and end patterns"""
        
        start_idx = None
        end_idx = None
        
        # Find start index
        for i, line in enumerate(lines):
            if start_pattern in line:
                start_idx = i
                break
        
        if start_idx is None:
            return f"<!-- Section not found: {start_pattern} -->\n"
        
        # Find end index
        if end_pattern:
            for i in range(start_idx + 1, len(lines)):
                if end_pattern in lines[i]:
                    end_idx = i
                    break
        else:
            # No end pattern means go to end of document
            end_idx = len(lines)
        
        # Extract and return the section
        section_lines = lines[start_idx:end_idx]
        return '\n'.join(section_lines)
    
    def analyze_document(self, input_file):
        """Analyze a document to help identify section patterns"""
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        print(f"\nDocument Analysis: {input_file}")
        print("=" * 50)
        
        # Find all headers
        headers = []
        for i, line in enumerate(lines):
            # Match markdown headers
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                heading = match.group(2)
                headers.append((i + 1, level, heading))
        
        # Display headers
        print("\nDocument Structure:")
        for line_num, level, heading in headers:
            indent = "  " * (level - 1)
            print(f"Line {line_num:4d}: {indent}{'#' * level} {heading}")
        
        # Statistics
        print(f"\nDocument Statistics:")
        print(f"  Total lines: {len(lines)}")
        print(f"  Total words: {len(content.split())}")
        print(f"  Total headers: {len(headers)}")
        
        # Compare with configuration
        if hasattr(self, 'config'):
            print(f"\nConfiguration Mapping:")
            outline = self.config['document_outline']
            
            for section in outline:
                pattern = section['start_pattern']
                found = False
                for line_num, level, heading in headers:
                    # Check if the pattern matches the full line (including markdown syntax)
                    full_line = '#' * level + ' ' + heading
                    if pattern in full_line:
                        found = True
                        print(f"  ✓ {section['id']}: '{pattern}' found in '{full_line}' (line {line_num})")
                        break
                
                if not found:
                    print(f"  ✗ {section['id']}: '{pattern}' not found in headers")

def merge_shared_modules():
    """Merge shared modules that don't belong to a specific document"""
    
    modules_dir = Path.cwd() / "modules"
    shared_files = list(modules_dir.glob("Shared-*.md"))
    
    if not shared_files:
        print("No shared modules found.")
        return
    
    print("\nShared Modules:")
    for file in sorted(shared_files):
        size = file.stat().st_size
        print(f"  - {file.name} ({size} bytes)")

def main():
    parser = argparse.ArgumentParser(description='Split documents using configuration files')
    parser.add_argument('input_file', help='Input document to split')
    parser.add_argument('--config', required=True,
                       help='Configuration name (found in pythonScripts/data/*.yaml)')
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze document structure without splitting')
    
    args = parser.parse_args()
    
    try:
        splitter = ConfigBasedSplitter(args.config, args.input_file)
        
        if args.analyze:
            splitter.analyze_document(args.input_file)
        else:
            splitter.split_document(args.input_file)
            
            # Check for shared modules
            merge_shared_modules()
            
            print("\nNext steps:")
            print(f"1. Review the generated modules in modules/")
            print(f"2. Run validation: ./hermesdock.sh validate {args.config}")
            print(f"3. Build document: ./hermesdock.sh build {args.config}")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"\nAvailable configurations:")
        
        config_dir = Path(__file__).parent / "data"
        for config_file in config_dir.glob("*.yaml"):
            print(f"  - {config_file.stem}")

if __name__ == "__main__":
    main()