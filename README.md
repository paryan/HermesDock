# HermesDock - Focused Document Collaboration

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
