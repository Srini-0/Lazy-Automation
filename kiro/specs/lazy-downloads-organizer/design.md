# Design Document: Lazy Downloads Organizer

## Overview

The Lazy Downloads Organizer is a Python command-line tool that automates the organization of files in a target directory (typically ~/Downloads) by categorizing them based on file extensions and moving them into appropriate category folders. The tool is designed with simplicity, safety, and user control in mind, featuring dry-run capabilities, custom renaming patterns, and collision avoidance.

The system follows a straightforward pipeline architecture:
1. Scan the target directory for files
2. Categorize each file based on its extension
3. Create category folders as needed
4. Move (or simulate moving) files to their destinations
5. Handle collisions and renaming
6. Report results to the user

## Architecture

### High-Level Architecture

The application follows a modular, functional design with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│                    (argparse interface)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                       │
│                   (organize() function)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Scanner │    │Categorizer│   │  Mover   │
    └──────────┘    └──────────┘    └──────────┘
           │               │               │
           └───────────────┴───────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  File System    │
                  └─────────────────┘
```

### Design Principles

1. **Safety First**: Dry-run mode by default, collision avoidance, never overwrite files
2. **Simplicity**: Use Python standard library (pathlib, shutil, logging, argparse)
3. **Transparency**: Clear logging of all operations
4. **Extensibility**: Easy to add new categories or modify extension mappings
5. **Error Resilience**: Continue processing even if individual file operations fail

## Components and Interfaces

### 1. CLI Module (organizer.py - main entry point)

**Responsibilities:**
- Parse command-line arguments
- Configure logging based on verbosity
- Invoke the orchestration layer
- Handle top-level exceptions

**Interface:**
```python
def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()
    organize(args.target, args.dry_run, args.rename, args.verbose)
```

**Arguments:**
- `--target, -t`: Target directory path (default: ~/Downloads)
- `--dry-run / --no-dry-run`: Enable/disable simulation mode (default: --dry-run)
- `--rename, -r`: Rename pattern (optional, e.g., "{index}_{name}")
- `--verbose, -v`: Enable verbose logging

### 2. Scanner Module

**Responsibilities:**
- Scan the target directory for files
- Filter out directories and hidden files (optional)
- Return list of file paths

**Interface:**
```python
def scan_directory(target_dir: Path) -> List[Path]:
    """
    Scan the target directory and return a list of file paths.
    
    Args:
        target_dir: Path to the directory to scan
        
    Returns:
        List of Path objects for files in the directory
    """
```

### 3. Categorizer Module

**Responsibilities:**
- Maintain extension-to-category mapping
- Determine category for a given file
- Provide category information

**Interface:**
```python
def categorize_file(file_path: Path) -> str:
    """
    Determine the category for a file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Category name (e.g., "Images", "Videos", "Others")
    """

def get_category_mapping() -> Dict[str, List[str]]:
    """
    Return the mapping of categories to file extensions.
    
    Returns:
        Dictionary mapping category names to lists of extensions
    """
```

### 4. Renamer Module

**Responsibilities:**
- Apply rename patterns to filenames
- Handle placeholder substitution ({index}, {name}, {ext})
- Ensure valid filenames

**Interface:**
```python
def rename_file(
    original_name: str,
    pattern: str,
    index: int,
    extension: str
) -> str:
    """
    Apply a rename pattern to a filename.
    
    Args:
        original_name: Original filename without extension
        pattern: Rename pattern with placeholders
        index: Sequential index for this file
        extension: File extension (including dot)
        
    Returns:
        New filename with extension
    """
```

### 5. Mover Module

**Responsibilities:**
- Create category folders if needed
- Move files to destination
- Handle collisions by appending suffixes
- Support dry-run mode

**Interface:**
```python
def move_file(
    source: Path,
    destination_dir: Path,
    new_name: Optional[str] = None,
    dry_run: bool = True
) -> Tuple[bool, Path]:
    """
    Move a file to the destination directory, handling collisions.
    
    Args:
        source: Source file path
        destination_dir: Destination directory path
        new_name: Optional new filename (if renaming)
        dry_run: If True, simulate the move without actually doing it
        
    Returns:
        Tuple of (success: bool, final_destination: Path)
    """

def ensure_category_folder(
    base_dir: Path,
    category: str,
    dry_run: bool = True
) -> Path:
    """
    Ensure a category folder exists (or would exist in dry-run).
    
    Args:
        base_dir: Base directory containing category folders
        category: Category name
        dry_run: If True, don't actually create the folder
        
    Returns:
        Path to the category folder
    """
```

### 6. Orchestrator Module

**Responsibilities:**
- Coordinate the overall organization process
- Maintain statistics (files moved per category)
- Handle errors gracefully
- Report results

**Interface:**
```python
def organize(
    target_dir: str,
    dry_run: bool = True,
    rename_pattern: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, int]:
    """
    Organize files in the target directory.
    
    Args:
        target_dir: Directory to organize
        dry_run: If True, simulate without making changes
        rename_pattern: Optional pattern for renaming files
        verbose: Enable verbose logging
        
    Returns:
        Dictionary mapping category names to file counts
    """
```

## Data Models

### File Information

```python
@dataclass
class FileInfo:
    """Information about a file to be organized."""
    source_path: Path
    category: str
    original_name: str
    extension: str
    new_name: Optional[str] = None
    destination_path: Optional[Path] = None
```

### Organization Result

```python
@dataclass
class OrganizationResult:
    """Result of organizing files."""
    total_files: int
    files_moved: int
    files_skipped: int
    category_counts: Dict[str, int]
    errors: List[str]
```

### Category Mapping

The category mapping is a constant dictionary:

```python
CATEGORY_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", 
                  ".ppt", ".pptx", ".odt", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h",
             ".json", ".xml", ".yml", ".yaml", ".sh", ".rb", ".go", ".rs",
             ".ts", ".tsx", ".jsx"],
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: File scanning completeness
*For any* directory with files, scanning should identify all regular files (non-directories) with their correct extensions.
**Validates: Requirements 1.1**

### Property 2: Categorization correctness
*For any* file with a recognized extension, the categorizer should map it to the correct category according to the CATEGORY_MAPPING.
**Validates: Requirements 1.2**

### Property 3: File destination correctness
*For any* file that is organized, it should end up in the category folder corresponding to its extension.
**Validates: Requirements 1.3**

### Property 4: Count accuracy
*For any* organization operation, the reported count of files moved per category should equal the actual number of files in each category folder.
**Validates: Requirements 1.4**

### Property 5: Category folder creation
*For any* category that has files to organize, if the category folder doesn't exist, it should be created before moving files.
**Validates: Requirements 3.2**

### Property 6: Folder idempotence
*For any* category folder that already exists, organizing files should not modify the folder itself (only add files to it).
**Validates: Requirements 3.4**

### Property 7: Dry-run immutability
*For any* directory, running in dry-run mode should not change any file locations or create any folders.
**Validates: Requirements 4.1, 4.4, 4.5**

### Property 8: Dry-run count accuracy
*For any* directory, the counts reported in dry-run mode should match the counts that would result from actual execution.
**Validates: Requirements 4.3**


### Property 9: Rename pattern application
*For any* file and valid rename pattern, the renamed file should have all placeholders ({index}, {name}, {ext}) correctly substituted.
**Validates: Requirements 5.1, 5.2, 5.3, 5.4**

### Property 10: Extension preservation
*For any* file operation (move or rename), the file extension should be preserved in the final filename.
**Validates: Requirements 5.5, 8.3**

### Property 11: Collision detection and resolution
*For any* file being moved to a destination where a file with the same name exists, a unique suffix should be appended to avoid overwriting.
**Validates: Requirements 5.6, 8.1, 8.2**

### Property 12: No file overwriting
*For any* organization operation, no existing files should be overwritten or deleted.
**Validates: Requirements 8.5**

## Error Handling

The system implements graceful error handling at multiple levels:

### File Operation Errors

**Strategy**: Continue processing remaining files when individual operations fail

- **File access errors**: Log error with file path and continue
- **Permission errors**: Log error and skip file
- **Invalid paths**: Validate paths before operations, log errors
- **Disk space errors**: Catch and report, halt operation

### Input Validation Errors

**Strategy**: Fail fast with clear error messages

- **Invalid target directory**: Check existence before scanning
- **Invalid rename pattern**: Validate pattern syntax
- **Invalid arguments**: argparse handles with usage message

### Error Logging

All errors are logged with:
- Timestamp
- Error type
- File path (if applicable)
- Error message
- Stack trace (in verbose mode)


## Testing Strategy

The Lazy Downloads Organizer will employ a dual testing approach combining unit tests and property-based tests to ensure comprehensive coverage and correctness.

### Unit Testing

Unit tests will verify specific examples, edge cases, and integration points:

**Scanner Module Tests:**
- Test scanning empty directory
- Test scanning directory with mixed files and subdirectories
- Test handling of hidden files
- Test handling of symbolic links

**Categorizer Module Tests:**
- Test each category mapping with sample extensions
- Test unknown extensions map to "Others"
- Test case-insensitive extension matching

**Renamer Module Tests:**
- Test each placeholder type ({index}, {name}, {ext})
- Test patterns with multiple placeholders
- Test patterns with no placeholders
- Test edge cases (empty names, special characters)

**Mover Module Tests:**
- Test moving single file
- Test collision handling with existing files
- Test folder creation
- Test dry-run mode doesn't modify filesystem

**Integration Tests:**
- Test complete organization workflow
- Test with various CLI argument combinations
- Test error recovery scenarios

### Property-Based Testing

Property-based tests will verify universal properties across many randomly generated inputs using the **Hypothesis** library for Python.

**Configuration:**
- Each property test will run a minimum of 100 iterations
- Tests will use Hypothesis strategies to generate diverse test data
- Each test will be tagged with a comment referencing the design document property

**Property Test Implementation:**

Each correctness property from the design document will be implemented as a single property-based test:

1. **Property 1: File scanning completeness** - Generate random directory structures, verify all files found
2. **Property 2: Categorization correctness** - Generate random filenames with known extensions, verify correct categories
3. **Property 3: File destination correctness** - Generate random files, organize them, verify locations
4. **Property 4: Count accuracy** - Generate random file sets, verify reported counts match actual
5. **Property 5: Category folder creation** - Generate random categories, verify folders created as needed
6. **Property 6: Folder idempotence** - Run organization twice, verify folders unchanged
7. **Property 7: Dry-run immutability** - Generate random files, run dry-run, verify no changes
8. **Property 8: Dry-run count accuracy** - Compare dry-run counts with actual execution counts
9. **Property 9: Rename pattern application** - Generate random patterns and files, verify substitution
10. **Property 10: Extension preservation** - Generate random operations, verify extensions preserved
11. **Property 11: Collision detection and resolution** - Create collisions, verify suffixes added
12. **Property 12: No file overwriting** - Generate random operations, verify no overwrites

**Test Tagging Format:**
```python
# Feature: lazy-downloads-organizer, Property 1: File scanning completeness
@given(...)
def test_file_scanning_completeness(...):
    ...
```


## Implementation Details

### Technology Stack

- **Language**: Python 3.8+
- **Standard Libraries**: 
  - `pathlib` - Modern path handling
  - `shutil` - File operations
  - `argparse` - CLI argument parsing
  - `logging` - Structured logging
  - `dataclasses` - Data models
  - `typing` - Type hints
- **Testing**: 
  - `pytest` - Test framework
  - `hypothesis` - Property-based testing
- **No external dependencies** for core functionality

### File Organization

```
lazy_downloads_organizer/
├── lazy_downloader/
│   ├── __init__.py           # Package initialization, version info
│   └── organizer.py          # Main module with all functionality
├── examples/
│   └── sample_run.txt        # Example output
├── .kiro/
│   └── config.json           # Project configuration
├── README.md                 # User documentation
├── requirements.txt          # Python dependencies (pytest, hypothesis)
├── LICENSE                   # MIT License
└── blog_post.md             # Blog post for AWS Builder Center
```

### Module Structure (organizer.py)

The organizer.py module will contain all functionality in a single, well-organized file:

1. **Imports and Constants** - Category mapping, type hints
2. **Data Models** - FileInfo, OrganizationResult dataclasses
3. **Scanner Functions** - scan_directory()
4. **Categorizer Functions** - categorize_file(), get_category_mapping()
5. **Renamer Functions** - rename_file()
6. **Mover Functions** - move_file(), ensure_category_folder()
7. **Orchestrator Functions** - organize()
8. **CLI Functions** - setup_logging(), main()
9. **Entry Point** - if __name__ == "__main__"

### Logging Configuration

```python
# Normal mode: INFO level
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# Verbose mode: DEBUG level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Collision Handling Algorithm

```python
def resolve_collision(destination: Path) -> Path:
    """
    If destination exists, append _1, _2, etc. until unique.
    
    Example: photo.jpg -> photo_1.jpg -> photo_2.jpg
    """
    if not destination.exists():
        return destination
    
    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1
    
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1
```

### Rename Pattern Processing

```python
def apply_rename_pattern(
    pattern: str,
    original_name: str,
    index: int,
    extension: str
) -> str:
    """
    Replace placeholders in pattern:
    - {index} -> sequential number
    - {name} -> original filename without extension
    - {ext} -> file extension without dot
    
    Example: "{index}_{name}" + "photo.jpg" + index=5
             -> "5_photo.jpg"
    """
    result = pattern
    result = result.replace("{index}", str(index))
    result = result.replace("{name}", original_name)
    result = result.replace("{ext}", extension.lstrip('.'))
    return result + extension
```


## Project Deliverables

### Core Application Files

1. **lazy_downloader/organizer.py** - Complete implementation with:
   - All functions documented with docstrings
   - Type hints for all parameters and returns
   - Inline comments for complex logic
   - Comprehensive error handling

2. **lazy_downloader/__init__.py** - Package initialization:
   - Version information
   - Package-level imports
   - Metadata

### Documentation Files

1. **README.md** - User-facing documentation:
   - Project overview and motivation
   - Feature list
   - Installation instructions
   - Usage examples with code blocks
   - Before/After scenarios
   - Troubleshooting section
   - Acknowledgment of Kiro usage

2. **examples/sample_run.txt** - Example output:
   - Mock dry-run output showing 8-10 file moves
   - Demonstration of log format
   - Summary statistics

3. **blog_post.md** - AWS Builder Center blog post:
   - Title: "I hate sorting my Downloads folder, so I automated it using Python + Kiro"
   - Sections: Introduction, Problem, Solution, Kiro's Role, Code Snippets, Results, Future Work
   - Screenshot placeholders
   - GitHub repository link placeholder

### Configuration Files

1. **.kiro/config.json** - Project metadata:
   - Project name and version
   - Description
   - Entry point
   - Commands (run, test)
   - Author and tags

2. **requirements.txt** - Python dependencies:
   - pytest (for testing)
   - hypothesis (for property-based testing)
   - Core functionality uses only standard library

3. **LICENSE** - MIT License template

## Development Workflow

### Phase 1: Core Implementation
1. Implement data models and constants
2. Implement scanner module
3. Implement categorizer module
4. Implement mover module (with dry-run support)
5. Implement orchestrator

### Phase 2: CLI and Renaming
1. Implement renamer module
2. Implement CLI with argparse
3. Implement logging configuration
4. Add collision handling

### Phase 3: Testing
1. Write unit tests for each module
2. Write property-based tests for correctness properties
3. Write integration tests
4. Test on real Downloads folder

### Phase 4: Documentation
1. Add docstrings and comments
2. Write README with examples
3. Create sample output
4. Write blog post

### Phase 5: Polish
1. Add error handling improvements
2. Optimize performance if needed
3. Final testing and validation

## Future Enhancements

Potential improvements for future versions:

1. **Configuration File**: Support for custom category mappings via config file
2. **Undo Functionality**: Keep a log of moves to enable reversal
3. **Watch Mode**: Automatically organize new files as they appear
4. **GUI**: Simple graphical interface for non-technical users
5. **Cloud Integration**: Support for organizing cloud storage (Dropbox, Google Drive)
6. **Smart Categorization**: ML-based categorization beyond just extensions
7. **Duplicate Detection**: Identify and handle duplicate files
8. **Archive Extraction**: Optionally extract and organize archive contents

