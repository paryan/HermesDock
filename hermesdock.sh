#!/bin/bash
# Save as: hermesdock.sh (in root directory)

# HermesDock Document Collaboration CLI
# Provides easy access to all document collaboration functions

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="pythonScripts"

show_help() {
    echo -e "${BLUE}HermesDock Document Collaboration System${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo "Usage: ./hermesdock.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  setup              - Initialize directory structure"
    echo "  setup-configs      - Create default YAML configurations"
    echo "  new                - Create a new document configuration"
    echo "  split <file>       - Split a document into modules"
    echo "  build [doc]        - Build document(s) from modules"
    echo "  validate [doc]     - Validate module structure"
    echo "  list               - List all document configurations"
    echo "  create-map <doc>   - Create module map for document"
    echo "  convert [doc]      - Convert document to Word/PDF"
    echo "  new-config         - Create a new document configuration"
    echo "  list-templates     - List available configuration templates"
    echo "  reset              - Reset all generated files (start over)"
    echo "  clean              - Clean build directory"
    echo "  help               - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./hermesdock.sh setup"
    echo "  ./hermesdock.sh setup-configs"
    echo "  ./hermesdock.sh new"
    echo "  ./hermesdock.sh split document.md --config <config_name>"
    echo "  ./hermesdock.sh build             # Build all documents"
    echo "  ./hermesdock.sh build <doc_name>  # Build specific document"
    echo "  ./hermesdock.sh validate"
    echo "  ./hermesdock.sh reset             # Start over with clean slate"
}

case "$1" in
    setup)
        echo -e "${YELLOW}Setting up HermesDock document collaboration structure...${NC}"
        python3 setup.py
        ;;
    
    setup-configs)
        echo -e "${YELLOW}Creating default YAML configurations...${NC}"
        python3 "$SCRIPT_DIR/create_configs.py"
        ;;
    
    new)
        echo -e "${YELLOW}Creating new document configuration...${NC}"
        python3 "$SCRIPT_DIR/new_doc.py"
        ;;
    
    new-config)
        echo -e "${YELLOW}Creating new document configuration...${NC}"
        python3 "$SCRIPT_DIR/new_doc.py"
        ;;
    
    list-templates)
        echo -e "${YELLOW}Available configuration templates:${NC}"
        python3 -c "
import sys
sys.path.append('pythonScripts')
from create_configs import list_available_configs
list_available_configs()
"
        ;;
    
    split)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify input file${NC}"
            echo "Usage: ./hermesdock.sh split <file> --config <name>"
            exit 1
        fi
        python3 "$SCRIPT_DIR/split.py" "$2" "${@:3}"
        ;;
    
    build)
        if [ -z "$2" ]; then
            echo -e "${YELLOW}Building all documents...${NC}"
            python3 "$SCRIPT_DIR/build.py" build-all
        else
            echo -e "${YELLOW}Building $2 document...${NC}"
            python3 "$SCRIPT_DIR/build.py" build --doc "$2"
        fi
        ;;
    
    validate)
        if [ -z "$2" ]; then
            echo -e "${YELLOW}Validating all modules...${NC}"
            python3 "$SCRIPT_DIR/build.py" validate
        else
            echo -e "${YELLOW}Validating $2 modules...${NC}"
            python3 "$SCRIPT_DIR/build.py" validate --doc "$2"
        fi
        ;;
    
    list)
        echo -e "${YELLOW}Available document configurations:${NC}"
        python3 "$SCRIPT_DIR/build.py" list
        ;;
    
    create-map)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify document name${NC}"
            echo "Usage: ./hermesdock.sh create-map <doc_name>"
            exit 1
        fi
        echo -e "${YELLOW}Creating module map for $2...${NC}"
        python3 "$SCRIPT_DIR/build.py" create-map --doc "$2"
        ;;
    
    convert)
        if [ -z "$2" ]; then
            echo -e "${YELLOW}Converting all documents...${NC}"
            python3 "$SCRIPT_DIR/convert.py" convert-all
        else
            echo -e "${YELLOW}Converting $2 document...${NC}"
            python3 "$SCRIPT_DIR/convert.py" convert --doc "$2"
        fi
        ;;
    
    convert-all)
        echo -e "${YELLOW}Converting all documents...${NC}"
        python3 "$SCRIPT_DIR/convert.py" convert-all
        ;;
    
    reset)
        echo -e "${YELLOW}Resetting all generated files...${NC}"
        echo -e "${YELLOW}This will remove all modules, built documents, converted files, and configurations.${NC}"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Removing modules...${NC}"
            rm -rf modules/*
            echo -e "${YELLOW}Removing built documents...${NC}"
            rm -rf dist
            echo -e "${YELLOW}Removing converted files...${NC}"
            # Converted files are in dist/, so they're already removed above
            echo -e "${YELLOW}Removing configurations...${NC}"
            rm -f pythonScripts/data/*.yaml
            echo -e "${GREEN}✓ Reset complete! All generated files and configurations removed.${NC}"
            echo -e "${BLUE}You can now start fresh with:${NC}"
            echo -e "  ./hermesdock.sh setup-configs"
            echo -e "  ./hermesdock.sh split 'document.md' --config <config_name>"
        else
            echo -e "${BLUE}Reset cancelled.${NC}"
        fi
        ;;
    
    clean)
        echo -e "${YELLOW}Cleaning build directory...${NC}"
        rm -rf dist/*
        echo -e "${GREEN}✓ Build directory cleaned${NC}"
        ;;
    
    help|--help|-h|"")
        show_help
        ;;
    
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac