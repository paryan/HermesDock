#!/bin/bash
# Save as: workflow_example.sh

# Example workflow demonstrating the complete documentation process
# including building, converting, and managing versions

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}HermesDock Document Collaboration Workflow Example${NC}"
echo -e "${BLUE}===============================================${NC}"
echo ""

# Function to pause and show what's happening
pause_and_explain() {
    echo ""
    echo -e "${YELLOW}→ $1${NC}"
    read -p "Press Enter to continue..."
    echo ""
}

# 1. Initial setup check
echo -e "${GREEN}Step 1: Checking setup...${NC}"
if [ ! -d "modules" ] || [ ! -d "pythonScripts" ]; then
    echo "Running initial setup..."
    python3 setup.py
    chmod +x hermesdock.sh
else
    echo "✓ Setup already complete"
fi

pause_and_explain "Setup ensures all directories and scripts are in place"

# 2. Check pandoc installation
echo -e "${GREEN}Step 2: Checking document conversion capability...${NC}"
python3 pythonScripts/setup_pandoc.py

pause_and_explain "Pandoc is required for Word/PDF conversion"

# 3. Show current state
echo -e "${GREEN}Step 3: Current state of documentation...${NC}"
echo "Modules in modules/:"
ls modules/*.md 2>/dev/null | head -5 || echo "  No modules yet"
echo ""
echo "Documents in dist/:"
ls dist/*.md 2>/dev/null || echo "  No documents built yet"
echo ""
echo "Word documents in dist/docx/:"
ls dist/docx/*.docx 2>/dev/null | tail -3 || echo "  No Word documents yet"
echo ""
echo "PDFs in dist/pdfs/:"
ls dist/pdfs/*.pdf 2>/dev/null | tail -3 || echo "  No PDFs yet"

pause_and_explain "This shows what we have before building"

# 4. Build all documents
echo -e "${GREEN}Step 4: Building all documents from modules...${NC}"
./hermesdock.sh build

pause_and_explain "Markdown documents are now in dist/ without version numbers"

# 5. Convert all to Word and PDF
echo -e "${GREEN}Step 5: Converting to Word and PDF formats...${NC}"
./hermesdock.sh convert-all

pause_and_explain "Word and PDF files now have date stamps (_YYYYMMDD)"

# 6. Show the results
echo -e "${GREEN}Step 6: Viewing the results...${NC}"
echo -e "${BLUE}Markdown files (no version numbers):${NC}"
ls -la dist/*.md 2>/dev/null

echo ""
echo -e "${BLUE}Word documents (with date stamps):${NC}"
ls -la dist/docx/*.docx 2>/dev/null | tail -5

echo ""
echo -e "${BLUE}PDF documents (with date stamps):${NC}"
ls -la dist/pdfs/*.pdf 2>/dev/null | tail -5

pause_and_explain "Notice how Word/PDF files have dates but markdown doesn't"

# 7. Demonstrate making a change
echo -e "${GREEN}Step 7: Making a change and rebuilding...${NC}"
echo ""
echo "Let's say you edited the business model section..."
echo "(In real use, you would: nano modules/STRATEGY-06-business-model.md)"
echo ""
echo "Now rebuilding just the strategy document:"
./hermesdock.sh build strategy

echo ""
echo "And converting just that document:"
./hermesdock.sh convert strategy

pause_and_explain "This creates a new dated version while keeping the old one"

# 8. Clean old versions
echo -e "${GREEN}Step 8: Managing old versions...${NC}"
echo "Current Word documents:"
ls dist/docx/*.docx 2>/dev/null | wc -l | xargs echo "  Total files:"

echo ""
echo "To clean files older than 7 days:"
echo "  ./hermesdock.sh clean-old --days 7"
echo ""
echo "(Not running this now to preserve your files)"

pause_and_explain "Use clean-old to manage disk space"

# 9. Summary
echo -e "${GREEN}Summary of the Complete Workflow:${NC}"
echo "1. ✓ Setup creates the structure"
echo "2. ✓ Split breaks documents into modules"
echo "3. ✓ Build creates clean markdown (no versions)"
echo "4. ✓ Convert creates dated Word/PDF files"
echo "5. ✓ Edit modules and rebuild as needed"
echo "6. ✓ Clean old versions periodically"
echo ""
echo -e "${BLUE}Key Commands to Remember:${NC}"
echo "  ./hermesdock.sh build          # Build all markdown"
echo "  ./hermesdock.sh convert-all    # Convert all to Word/PDF"
echo "  ./hermesdock.sh build strategy # Build specific document"
echo "  ./hermesdock.sh clean-old      # Remove old versions"
echo ""
echo -e "${GREEN}✓ Workflow demonstration complete!${NC}"
