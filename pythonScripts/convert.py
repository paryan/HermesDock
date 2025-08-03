#!/usr/bin/env python3
# Save as: pythonScripts/convert.py

"""
Convert markdown documents to Word (docx) and PDF formats with date stamps.
Uses pandoc for high-quality conversion.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import yaml

class DocumentConverter:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.dist_dir = self.root_dir / "dist"
        self.docx_dir = self.dist_dir / "docx"
        self.pdf_dir = self.dist_dir / "pdfs"
        self.config_dir = Path(__file__).parent / "data"
        
        # Create output directories
        self.docx_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Get current date
        self.date_suffix = datetime.now().strftime("_%Y%m%d")
        
    def check_pandoc(self):
        """Check if pandoc is installed"""
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_output_filename(self, input_file, format_type):
        """Generate output filename with date suffix"""
        stem = input_file.stem
        if format_type == 'docx':
            return self.docx_dir / f"{stem}{self.date_suffix}.docx"
        else:
            return self.pdf_dir / f"{stem}{self.date_suffix}.pdf"
    
    def convert_to_docx(self, input_file):
        """Convert markdown to Word document"""
        output_file = self.get_output_filename(input_file, 'docx')
        
        # Pandoc command with nice formatting options
        cmd = [
            'pandoc',
            str(input_file),
            '-o', str(output_file),
            '--reference-doc', str(self.get_reference_docx()),
            '--toc',  # Table of contents
            '--toc-depth=3',
            '-V', 'colorlinks=true',
            '-V', 'linkcolor=blue',
            '-V', 'urlcolor=blue'
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ Created: {output_file.name}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error converting to DOCX: {e}")
            # Fallback: try without reference doc
            cmd.remove('--reference-doc')
            cmd.remove(str(self.get_reference_docx()))
            try:
                subprocess.run(cmd, check=True)
                print(f"  ✓ Created: {output_file.name} (without template)")
                return output_file
            except subprocess.CalledProcessError as e2:
                print(f"  ✗ Failed to convert to DOCX: {e2}")
                return None
    
    def convert_to_pdf(self, input_file):
        """Convert markdown to PDF"""
        output_file = self.get_output_filename(input_file, 'pdf')
        
        # Pandoc command for PDF with nice formatting
        cmd = [
            'pandoc',
            str(input_file),
            '-o', str(output_file),
            '--pdf-engine=xelatex',  # Better Unicode support
            '--toc',
            '--toc-depth=3',
            '-V', 'geometry:margin=1in',
            '-V', 'colorlinks=true',
            '-V', 'linkcolor=blue',
            '-V', 'urlcolor=blue',
            '-V', 'toccolor=black',
            '-V', 'fontsize=11pt',
            '-V', 'mainfont=Arial',  # Professional font
            '--highlight-style=tango'  # Code highlighting
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ Created: {output_file.name}")
            return output_file
        except subprocess.CalledProcessError as e:
            # Fallback to simpler PDF engine
            cmd[cmd.index('--pdf-engine=xelatex')] = '--pdf-engine=pdflatex'
            # Remove font specification for pdflatex
            cmd = [arg for arg in cmd if not arg.startswith('mainfont=')]
            
            try:
                subprocess.run(cmd, check=True)
                print(f"  ✓ Created: {output_file.name} (using pdflatex)")
                return output_file
            except subprocess.CalledProcessError as e2:
                print(f"  ✗ Failed to convert to PDF: {e2}")
                return None
    
    def get_reference_docx(self):
        """Get or create reference Word template"""
        template_path = self.config_dir / "reference.docx"
        
        if not template_path.exists():
            # Create a basic reference document
            self.create_reference_docx(template_path)
        
        return template_path
    
    def create_reference_docx(self, path):
        """Create a reference Word document with HermesDock styling"""
        # Create a minimal markdown for the template
        temp_md = path.parent / "temp_reference.md"
        with open(temp_md, 'w') as f:
            f.write("# HermesDock Document Template\n\n")
            f.write("This is a reference document for styling.\n")
        
        # Convert to docx
        cmd = ['pandoc', str(temp_md), '-o', str(path)]
        try:
            subprocess.run(cmd, check=True)
            temp_md.unlink()  # Remove temp file
        except:
            pass  # Template creation failed, will use default
    
    def convert_document(self, doc_name, formats=['docx', 'pdf']):
        """Convert a specific document to requested formats"""
        # Find the markdown file
        md_file = self.dist_dir / f"{self.get_filename_for_doc(doc_name)}"
        
        if not md_file.exists():
            print(f"Error: {md_file} not found")
            print("Make sure to build the document first: ./hermesdock.sh build")
            return
        
        print(f"\nConverting {doc_name}...")
        print(f"Source: {md_file.name}")
        
        results = {}
        
        if 'docx' in formats:
            results['docx'] = self.convert_to_docx(md_file)
        
        if 'pdf' in formats:
            results['pdf'] = self.convert_to_pdf(md_file)
        
        return results
    
    def get_filename_for_doc(self, doc_name):
        """Get the output filename for a document from its config"""
        config_path = self.config_dir / f"{doc_name}.yaml"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config['filename']
        
        # Try to find the actual file in dist directory
        dist_files = list(self.dist_dir.glob("*.md"))
        for file in dist_files:
            if doc_name.lower() in file.name.lower():
                return file.name
        
        # Fallback to generic name
        return f"{doc_name}.md"
    
    def convert_all(self, formats=['docx', 'pdf']):
        """Convert all documents in dist/ to requested formats"""
        md_files = list(self.dist_dir.glob("*.md"))
        
        if not md_files:
            print("No markdown files found in dist/")
            print("Run './hermesdock.sh build' first to generate documents")
            print("Or run './hermesdock.sh build <doc_name>' to build a specific document")
            return
        
        print(f"\nConverting {len(md_files)} documents...")
        
        for md_file in md_files:
            print(f"\nProcessing: {md_file.name}")
            
            if 'docx' in formats:
                self.convert_to_docx(md_file)
            
            if 'pdf' in formats:
                self.convert_to_pdf(md_file)
        
        print("\n✓ Conversion complete!")
        print(f"\nOutput locations:")
        if 'docx' in formats:
            print(f"  Word documents: {self.docx_dir}/")
        if 'pdf' in formats:
            print(f"  PDF documents: {self.pdf_dir}/")
    
    def clean_old_versions(self, days=30):
        """Remove old versions of converted documents"""
        import re
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        removed_count = 0
        
        # Check both directories
        for dir_path in [self.docx_dir, self.pdf_dir]:
            if not dir_path.exists():
                continue
            
            for file in dir_path.iterdir():
                # Extract date from filename
                match = re.search(r'_(\d{8})\.(docx|pdf)$', file.name)
                if match:
                    file_date = datetime.strptime(match.group(1), '%Y%m%d')
                    if file_date < cutoff_date:
                        file.unlink()
                        removed_count += 1
                        print(f"  ✓ Removed old file: {file.name}")
        
        if removed_count > 0:
            print(f"\n✓ Cleaned {removed_count} old files")
        else:
            print("\n✓ No old files to clean")

def main():
    parser = argparse.ArgumentParser(description='Convert markdown to Word and PDF')
    parser.add_argument('action', choices=['convert', 'convert-all', 'clean'],
                       help='Action to perform')
    parser.add_argument('--doc', help='Document name (for convert action)')
    parser.add_argument('--format', choices=['docx', 'pdf', 'both'], 
                       default='both', help='Output format(s)')
    parser.add_argument('--days', type=int, default=30,
                       help='Days to keep old versions (for clean action)')
    
    args = parser.parse_args()
    
    converter = DocumentConverter()
    
    # Check if pandoc is installed
    if not converter.check_pandoc():
        print("Error: pandoc is not installed")
        print("\nTo install pandoc:")
        print("  Ubuntu/Debian: sudo apt-get install pandoc texlive-xetex")
        print("  macOS: brew install pandoc basictex")
        print("  Windows: Download from https://pandoc.org/installing.html")
        sys.exit(1)
    
    # Determine formats
    if args.format == 'both':
        formats = ['docx', 'pdf']
    else:
        formats = [args.format]
    
    if args.action == 'convert':
        if not args.doc:
            print("Error: --doc required for convert action")
            sys.exit(1)
        converter.convert_document(args.doc, formats)
    
    elif args.action == 'convert-all':
        converter.convert_all(formats)
    
    elif args.action == 'clean':
        print(f"Cleaning files older than {args.days} days...")
        converter.clean_old_versions(args.days)
    
    else:
        print("Error: Unknown action")
        sys.exit(1)

if __name__ == "__main__":
    main()