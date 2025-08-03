#!/usr/bin/env python3
# Save as: pythonScripts/setup_pandoc.py

"""
Helper script to check and guide pandoc installation for document conversion.
"""

import subprocess
import platform
import sys

def check_pandoc():
    """Check if pandoc is installed and get version"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, version_line
        return False, None
    except FileNotFoundError:
        return False, None

def check_latex():
    """Check if LaTeX is installed (needed for PDF generation)"""
    latex_commands = ['xelatex', 'pdflatex', 'lualatex']
    
    for cmd in latex_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return True, cmd
        except FileNotFoundError:
            continue
    
    return False, None

def get_install_instructions():
    """Get platform-specific installation instructions"""
    system = platform.system()
    
    instructions = {
        'Darwin': {  # macOS
            'pandoc': [
                "Using Homebrew (recommended):",
                "  brew install pandoc",
                "",
                "Or download from: https://pandoc.org/installing.html"
            ],
            'latex': [
                "For PDF generation, install BasicTeX or MacTeX:",
                "  brew install --cask basictex",
                "  # OR for full installation:",
                "  brew install --cask mactex",
                "",
                "After installation, you may need to add to PATH:",
                "  export PATH=\"/Library/TeX/texbin:$PATH\""
            ]
        },
        'Linux': {
            'pandoc': [
                "Ubuntu/Debian:",
                "  sudo apt-get update",
                "  sudo apt-get install pandoc",
                "",
                "Fedora:",
                "  sudo dnf install pandoc",
                "",
                "Arch:",
                "  sudo pacman -S pandoc",
                "",
                "Or download from: https://pandoc.org/installing.html"
            ],
            'latex': [
                "For PDF generation, install TeX Live:",
                "",
                "Ubuntu/Debian:",
                "  sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-recommended",
                "",
                "Fedora:",
                "  sudo dnf install texlive-xetex texlive-collection-fontsrecommended",
                "",
                "Arch:",
                "  sudo pacman -S texlive-core texlive-latexextra"
            ]
        },
        'Windows': {
            'pandoc': [
                "Download the installer from:",
                "  https://pandoc.org/installing.html",
                "",
                "Or use Chocolatey:",
                "  choco install pandoc",
                "",
                "Or use Scoop:",
                "  scoop install pandoc"
            ],
            'latex': [
                "For PDF generation, install MiKTeX or TeX Live:",
                "",
                "MiKTeX (recommended for Windows):",
                "  Download from: https://miktex.org/download",
                "",
                "Or use Chocolatey:",
                "  choco install miktex",
                "",
                "After installation, MiKTeX will automatically install",
                "packages as needed during PDF generation."
            ]
        }
    }
    
    return instructions.get(system, {
        'pandoc': ["Please visit https://pandoc.org/installing.html for installation instructions."],
        'latex': ["Please install a LaTeX distribution for PDF generation."]
    })

def test_conversion():
    """Test if conversion works with a simple example"""
    print("\nTesting document conversion...")
    
    # Create a test markdown file
    test_md = "test_conversion.md"
    with open(test_md, 'w') as f:
        f.write("# Test Document\n\n")
        f.write("This is a **test** document for conversion.\n\n")
        f.write("- Item 1\n")
        f.write("- Item 2\n")
        f.write("- Item 3\n")
    
    # Test DOCX conversion
    docx_success = False
    try:
        result = subprocess.run(['pandoc', test_md, '-o', 'test.docx'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Word document conversion works!")
            docx_success = True
            # Clean up
            import os
            os.remove('test.docx')
        else:
            print("✗ Word document conversion failed:", result.stderr)
    except Exception as e:
        print("✗ Word document conversion error:", str(e))
    
    # Test PDF conversion
    pdf_success = False
    try:
        result = subprocess.run(['pandoc', test_md, '-o', 'test.pdf'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ PDF conversion works!")
            pdf_success = True
            # Clean up
            import os
            os.remove('test.pdf')
        else:
            print("✗ PDF conversion failed (LaTeX may not be installed)")
            print("  Note: You can still generate Word documents without LaTeX")
    except Exception as e:
        print("✗ PDF conversion error:", str(e))
    
    # Clean up test file
    import os
    os.remove(test_md)
    
    return docx_success, pdf_success

def main():
    print("HermesDock Document Conversion Setup")
    print("=" * 50)
    
    # Check pandoc
    pandoc_installed, pandoc_version = check_pandoc()
    
    if pandoc_installed:
        print(f"✓ Pandoc is installed: {pandoc_version}")
    else:
        print("✗ Pandoc is not installed")
    
    # Check LaTeX
    latex_installed, latex_cmd = check_latex()
    
    if latex_installed:
        print(f"✓ LaTeX is installed: {latex_cmd}")
    else:
        print("✗ LaTeX is not installed (needed for PDF generation)")
    
    print()
    
    # Get installation instructions if needed
    if not pandoc_installed or not latex_installed:
        instructions = get_install_instructions()
        
        if not pandoc_installed:
            print("To install Pandoc:")
            print("-" * 40)
            for line in instructions['pandoc']:
                print(line)
            print()
        
        if not latex_installed:
            print("To install LaTeX (for PDF generation):")
            print("-" * 40)
            for line in instructions['latex']:
                print(line)
            print()
            print("Note: LaTeX is optional. You can still generate Word documents without it.")
            print()
    
    # Test conversion if pandoc is installed
    if pandoc_installed:
        docx_works, pdf_works = test_conversion()
        
        print("\nConversion Capabilities:")
        print("-" * 40)
        print(f"Word documents (.docx): {'✓ Ready' if docx_works else '✗ Not working'}")
        print(f"PDF documents (.pdf):   {'✓ Ready' if pdf_works else '✗ LaTeX required'}")
        
        if docx_works:
            print("\nYou can now use:")
            print("  ./hermesdock.sh convert <doc>    # Convert specific document")
            print("  ./hermesdock.sh convert-all      # Convert all documents")
        else:
            print("\nPlease install pandoc first to enable document conversion.")
            sys.exit(1)

if __name__ == "__main__":
    main()