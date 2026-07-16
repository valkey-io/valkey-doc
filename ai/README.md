# AI Libraries

This directory contains JSON files for AI libraries that are compatible with Valkey.

## Structure

AI libraries are organized by language:

```
ai/
  python/
    library-name.json
  javascript/
    library-name.json
  ...
```

## JSON Format

Each AI library JSON file should contain the following fields:

```json
{
    "name": "Library Name",
    "description": "Brief description of the AI library and its Valkey integration",
    "repo": "https://github.com/org/repo",
    "installation": "pip install library-name",
    "version": "1.0.0",
    "version_released": "2025-01-15",
    "language": "python",
    "license": "MIT"
}
```

### Field Descriptions

- **name** (string, required): The name of the AI library
- **description** (string, required): A brief description of what the library does and how it integrates with Valkey
- **repo** (string, required): URL to the library's source code repository
- **installation** (string, required): Installation command (e.g., `pip install`, `npm install`)
- **version** (string, required): Current version number (semantic versioning)
- **version_released** (string, required): Date when the current version was released (YYYY-MM-DD format)
- **language** (string, required): Primary programming language of the library
- **license** (string, required): Software license type

## Adding a New AI Library

1. Create a subdirectory for the language if it doesn't exist (e.g., `python/`, `javascript/`)
2. Create a JSON file named after the library (lowercase, hyphens for spaces)
3. Fill in all required fields
4. Submit a pull request

## Examples

See the existing JSON files in this directory for reference implementations.
