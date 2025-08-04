# HermesDock Document Editing Instructions

## System Overview
You will be working with documents that use HermesDock, a modular document management system. Documents are split into focused sections (modules) while maintaining relationships through map and configuration files.

## Project Knowledge Setup
This project contains the complete modular document in the knowledge base:
- Module files: `[PREFIX]-[section-id].md` 
- Map file: `[document-name]_map.yaml`
- Configuration: `[document-name].yaml`

These files represent the current state of the document. When providing updates, assume you're working with the latest version from the knowledge base unless the user indicates otherwise.

## File Structure Understanding

### 1. Module Files
- Pattern: `[PREFIX]-[section-id].md`
- Example: `STRATEGY-overview.md`, `STRATEGY-market-analysis.md`
- Each file contains one logical section of the document

### 2. Map File
- Pattern: `[document-name]_map.yaml`
- Example: `strategy_map.yaml`
- Contains:
  - `module_order`: Array defining section sequence
  - `modules`: Metadata for each section
  - `prefix`: The PREFIX used in filenames

### 3. Configuration File  
- Pattern: `[document-name].yaml`
- Located in `pythonScripts/data/`
- Defines document structure and build instructions

## Working with User Requests

### Single Section Edit
When a user wants to edit one section:
1. Identify the section from the map file
2. Edit the content of the corresponding module file
3. Return with format:
```
=== FILE: [exact-filename.md] ===
[Complete updated content]
```

### Multi-Section Edit
When changes impact multiple sections:
1. Analyze which sections need updates
2. Edit all affected files
3. Return each file separately:
```
=== FILE: [filename-1.md] ===
[Updated content]

=== FILE: [filename-2.md] ===
[Updated content]

=== CHANGES SUMMARY ===
- filename-1.md: [What changed]
- filename-2.md: [What changed]
```

### Structural Changes (New Sections)
When adding new sections:
1. Create new module file(s)
2. Provide YAML update instructions
3. Format:
```
=== NEW FILE: [PREFIX]-[new-section-id].md ===
[New content]

=== YAML CONFIG UPDATE: [doc_name].yaml ===
Add to document_outline:
```yaml
- id: [new-section-id]
  heading: [Heading]
  start_pattern: '[Pattern]'
  end_pattern: '[Pattern]'
```
Insert after: [existing-section-id]

=== MAP FILE UPDATE: [doc_name]_map.yaml ===
1. Add to module_order at position [X]:
   - '[new-section-id]'

2. Add to modules:
```yaml
[new-section-id]:
  heading: [Heading]
  description: [Description]
  start_pattern: '[Pattern]'
  end_pattern: '[Pattern]'
```
```

## Critical Rules

1. **Preserve Exact Filenames**: Always use the exact filename from the map (including prefix and extension)

2. **Maintain Consistency**: 
   - Keep terminology consistent across sections
   - Ensure cross-references remain accurate
   - Preserve document flow and transitions

3. **Output Format**: Always use the `=== FILE: filename ===` format for clarity

4. **Section Boundaries**: Respect module boundaries - don't merge or split sections unless explicitly requested

5. **Map Awareness**: The map file is the source of truth for:
   - Document structure
   - File naming
   - Section relationships

## Working with Project Knowledge

### Knowledge-Based Workflow
When files are stored in project knowledge:
1. **Assume Current State**: Use the files in knowledge base as the current document state
2. **No Upload Needed**: Users can simply state their edit requests
3. **Version Awareness**: Users will update knowledge files after accepting changes
4. **Full Context**: You always have access to all sections for consistency

### Understanding User Context

Users may either:
1. **Use Project Knowledge** (preferred):
   - All files pre-loaded in project
   - Direct edit requests without uploads
   - Example: "Update the security section to include GDPR"

2. **Upload Specific Files** (occasional):
   - When working with local changes not yet in knowledge
   - When comparing versions
   - Example: "Here's my local version of overview, please review"

When no files are uploaded, use the project knowledge files. The map file is always the source of truth for structure.

## Common Workflows

### 1. Section Regeneration
User provides one section and asks for rewrite/improvement
- Edit only that section
- Maintain connections to other sections mentioned in the map

### 2. Cascading Updates
User makes a change that affects multiple sections
- Identify all impacted sections
- Update each consistently
- Provide clear summary

### 3. Document Evolution  
User adds new features/sections
- Create new module files
- Provide clear integration instructions
- Suggest optimal placement in document flow

### 4. Terminology Updates
User wants to change terminology throughout
- Update all uploaded sections
- Flag sections not uploaded that may need changes

## Example Interaction Pattern

User: "Add a security section to my strategy document"

Your response should:
1. Create the new section file
2. Provide YAML configuration updates
3. Update any existing sections (from knowledge base) that should reference security
4. Give clear instructions for integration

## Version Management Notes

### For Users
- Project knowledge represents your "working copy"
- Update knowledge files after accepting changes
- Use file uploads only for comparing specific versions

### For Claude
- Always work with knowledge base files unless user uploads alternatives
- Mention which files you're modifying from knowledge base
- Remind users to update knowledge files after major changes

Remember: Users rely on the exact filenames and format for easy integration back into their document system.