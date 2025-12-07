# Requirements Document

## Introduction

The Lazy Downloads Organizer is a Python-based automation tool designed to help users maintain an organized file system by automatically categorizing and moving files from a target directory (typically ~/Downloads) into appropriate category folders based on file extensions. The system provides a command-line interface with options for dry-run testing, custom file renaming patterns, and verbose logging. This project is part of Kiro Week 2: Lazy Automation initiative.

## Glossary

- **Organizer**: The Python application that scans, categorizes, and moves files
- **Target Directory**: The directory to be organized (default: ~/Downloads)
- **Category Folder**: A subdirectory created within the Target Directory to store files of a specific type (e.g., Images, Videos)
- **File Extension**: The suffix of a filename that indicates file type (e.g., .jpg, .pdf, .mp4)
- **Dry Run**: A simulation mode where the Organizer reports what actions would be taken without actually moving files
- **Rename Pattern**: A user-specified template for renaming files during organization (e.g., "{index}_{name}")
- **CLI**: Command-Line Interface for user interaction with the Organizer
- **Collision**: A situation where a file being moved would overwrite an existing file with the same name
- **Verbose Mode**: A logging mode that provides detailed information about each operation

## Requirements

### Requirement 1

**User Story:** As a user with a cluttered downloads folder, I want to automatically organize files into category folders, so that I can easily find files by type.

#### Acceptance Criteria

1. WHEN the Organizer scans the Target Directory, THE Organizer SHALL identify all files and their extensions
2. WHEN a file is identified, THE Organizer SHALL determine the appropriate category based on the file extension mapping
3. WHEN the appropriate category is determined, THE Organizer SHALL move the file to the corresponding Category Folder
4. WHEN all files are processed, THE Organizer SHALL report the number of files moved per category
5. WHERE the Target Directory is not specified, THE Organizer SHALL use the user's Downloads directory as the default Target Directory

### Requirement 2

**User Story:** As a user, I want the system to support multiple file categories, so that different file types are organized logically.

#### Acceptance Criteria

1. THE Organizer SHALL support an Images category for extensions: .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp
2. THE Organizer SHALL support a Videos category for extensions: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm
3. THE Organizer SHALL support a Documents category for extensions: .pdf, .doc, .docx, .txt, .xls, .xlsx, .ppt, .pptx, .odt, .csv
4. THE Organizer SHALL support an Audio category for extensions: .mp3, .wav, .flac, .aac, .ogg, .m4a
5. THE Organizer SHALL support an Archives category for extensions: .zip, .rar, .7z, .tar, .gz, .bz2
6. THE Organizer SHALL support a Code category for extensions: .py, .js, .html, .css, .java, .cpp, .c, .h, .json, .xml, .yml, .yaml, .sh, .rb, .go, .rs, .ts, .tsx, .jsx
7. WHEN a file extension does not match any defined category, THE Organizer SHALL place the file in an Others category

### Requirement 3

**User Story:** As a user, I want category folders to be created automatically, so that I don't have to manually set up the folder structure.

#### Acceptance Criteria

1. WHEN the Organizer processes files for a category, THE Organizer SHALL check if the Category Folder exists
2. IF a Category Folder does not exist, THEN THE Organizer SHALL create the Category Folder before moving files
3. WHEN creating Category Folders, THE Organizer SHALL use appropriate permissions for the user's file system
4. WHEN a Category Folder already exists, THE Organizer SHALL use the existing folder without modification

### Requirement 4

**User Story:** As a cautious user, I want to preview what changes will be made before actually moving files, so that I can verify the organization plan is correct.

#### Acceptance Criteria

1. WHERE the --dry-run flag is provided, THE Organizer SHALL scan and categorize files without moving them
2. WHEN running in dry-run mode, THE Organizer SHALL display the source path and destination path for each file
3. WHEN running in dry-run mode, THE Organizer SHALL report the total number of files that would be moved per category
4. WHEN running in dry-run mode, THE Organizer SHALL not create any Category Folders
5. WHEN running in dry-run mode, THE Organizer SHALL not modify the file system in any way

### Requirement 5

**User Story:** As a user who wants consistent file naming, I want to rename files during organization using a custom pattern, so that my files follow a naming convention.

#### Acceptance Criteria

1. WHERE the --rename flag is provided with a pattern, THE Organizer SHALL rename files according to the specified pattern during the move operation
2. WHEN the rename pattern contains "{index}", THE Organizer SHALL replace it with a sequential number for each file in that category
3. WHEN the rename pattern contains "{name}", THE Organizer SHALL replace it with the original filename without extension
4. WHEN the rename pattern contains "{ext}", THE Organizer SHALL replace it with the original file extension
5. WHEN renaming files, THE Organizer SHALL preserve the file extension in the final filename
6. IF a renamed file would conflict with an existing filename, THEN THE Organizer SHALL append a unique suffix (_1, _2, etc.) to avoid overwriting

### Requirement 6

**User Story:** As a user, I want a simple command-line interface, so that I can easily run the organizer with different options.

#### Acceptance Criteria

1. THE Organizer SHALL provide a CLI using argparse for command-line argument parsing
2. THE Organizer SHALL accept a --target or -t flag with a directory path for the Target Directory
3. THE Organizer SHALL accept a --dry-run / --no-dry-run flag to enable or disable simulation mode
4. THE Organizer SHALL accept a --rename or -r flag with a pattern string for file renaming
5. THE Organizer SHALL accept a --verbose or -v flag to enable detailed logging output
6. WHEN the CLI is invoked with --help, THE Organizer SHALL display usage information and available options
7. WHEN the CLI is invoked with invalid arguments, THE Organizer SHALL display an error message and usage information

### Requirement 7

**User Story:** As a user, I want clear feedback during the organization process, so that I understand what the tool is doing.

#### Acceptance Criteria

1. WHEN the Organizer starts, THE Organizer SHALL display the Target Directory being processed
2. WHEN the Organizer moves a file, THE Organizer SHALL log the action with source and destination paths
3. WHEN the Organizer completes, THE Organizer SHALL display a summary showing the count of files moved per category
4. IF an error occurs during file operations, THEN THE Organizer SHALL display a descriptive error message and continue processing remaining files
5. WHEN running in dry-run mode, THE Organizer SHALL clearly indicate that no actual changes are being made
6. WHERE the --verbose flag is provided, THE Organizer SHALL display detailed information about each operation

### Requirement 8

**User Story:** As a user, I want filename collisions to be handled automatically, so that I never lose data due to overwriting.

#### Acceptance Criteria

1. WHEN moving a file to a destination where a file with the same name exists, THE Organizer SHALL detect the collision
2. WHEN a collision is detected, THE Organizer SHALL append a numeric suffix (_1, _2, _3, etc.) to the filename
3. WHEN appending a suffix, THE Organizer SHALL preserve the file extension
4. WHEN a collision occurs, THE Organizer SHALL log the collision and the resolution
5. THE Organizer SHALL never overwrite an existing file without user intervention

### Requirement 9

**User Story:** As a developer or user reading the code, I want comprehensive documentation, so that I can understand and modify the tool easily.

#### Acceptance Criteria

1. THE Organizer SHALL include docstrings for all modules, classes, and functions following Python conventions
2. THE Organizer SHALL include inline comments explaining complex logic or important decisions
3. THE Organizer SHALL provide a README.md file with installation instructions, usage examples, and feature descriptions
4. THE Organizer SHALL include type hints for function parameters and return values where applicable
5. THE Organizer SHALL document all command-line arguments and their effects in both the code and README

### Requirement 10

**User Story:** As a user, I want the project to have a clean structure, so that I can navigate and maintain the codebase easily.

#### Acceptance Criteria

1. THE Organizer SHALL organize code into a lazy_downloader package directory
2. THE Organizer SHALL include an organizer.py module containing the core organization logic
3. THE Organizer SHALL include an __init__.py file to make lazy_downloader a proper Python package
4. THE Organizer SHALL include a requirements.txt file listing all Python dependencies
5. THE Organizer SHALL include a README.md file at the project root
6. THE Organizer SHALL include a .kiro/config.json file for project configuration
7. THE Organizer SHALL include a LICENSE file with MIT License template

### Requirement 11

**User Story:** As a user learning about the tool, I want example outputs, so that I can understand what to expect before running it.

#### Acceptance Criteria

1. THE Organizer SHALL include an examples directory in the project structure
2. THE Organizer SHALL provide a sample_run.txt file showing mock dry-run output
3. WHEN the sample output is displayed, THE Organizer SHALL show 8-10 planned file moves
4. THE Organizer SHALL demonstrate the log format in the sample output
5. THE Organizer SHALL include examples of different file types being categorized

### Requirement 12

**User Story:** As a content creator, I want a blog post template, so that I can share my automation project with others.

#### Acceptance Criteria

1. THE Organizer SHALL include a blog post document for AWS Builder Center
2. THE Organizer SHALL include sections for: introduction, problem statement, solution description, Kiro usage, code snippets, results, and future improvements
3. THE Organizer SHALL include placeholders for screenshots (Before, Dry Run, After)
4. THE Organizer SHALL include step-by-step instructions for running the tool
5. THE Organizer SHALL include a placeholder for GitHub repository link
