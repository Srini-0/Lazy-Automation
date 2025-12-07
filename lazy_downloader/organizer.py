"""
Lazy Downloads Organizer - Main Module

This module provides functionality to automatically organize files in a directory
by categorizing them based on file extensions and moving them into appropriate
category folders.

Author: YOUR NAME
Part of: Kiro Week 2 - Lazy Automation
"""

import argparse
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

# Category mapping: maps category names to lists of file extensions
CATEGORY_MAPPING: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx",
        ".ppt", ".pptx", ".odt", ".csv"
    ],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [
        ".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h",
        ".json", ".xml", ".yml", ".yaml", ".sh", ".rb", ".go", ".rs",
        ".ts", ".tsx", ".jsx"
    ],
}

# Default category for files that don't match any category
DEFAULT_CATEGORY = "Others"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class FileInfo:
    """Information about a file to be organized."""
    source_path: Path
    category: str
    original_name: str
    extension: str
    new_name: Optional[str] = None
    destination_path: Optional[Path] = None


@dataclass
class OrganizationResult:
    """Result of organizing files."""
    total_files: int
    files_moved: int
    files_skipped: int
    category_counts: Dict[str, int]
    errors: List[str]


# ============================================================================
# SCANNER MODULE
# ============================================================================

def scan_directory(target_dir: Path) -> List[Path]:
    """
    Scan the target directory and return a list of file paths.
    
    This function identifies all regular files (not directories) in the target
    directory. It does not recurse into subdirectories.
    
    Args:
        target_dir: Path to the directory to scan
        
    Returns:
        List of Path objects for files in the directory
        
    Example:
        >>> files = scan_directory(Path("~/Downloads"))
        >>> print(f"Found {len(files)} files")
    """
    files = []
    
    try:
        for item in target_dir.iterdir():
            # Only include regular files, skip directories
            if item.is_file():
                files.append(item)
                logging.debug(f"Found file: {item.name}")
    except PermissionError as e:
        logging.error(f"Permission denied accessing directory: {target_dir}")
        raise
    except Exception as e:
        logging.error(f"Error scanning directory {target_dir}: {e}")
        raise
    
    return files


# ============================================================================
# CATEGORIZER MODULE
# ============================================================================

def get_category_mapping() -> Dict[str, List[str]]:
    """
    Return the mapping of categories to file extensions.
    
    Returns:
        Dictionary mapping category names to lists of extensions
        
    Example:
        >>> mapping = get_category_mapping()
        >>> print(mapping["Images"])
        ['.jpg', '.jpeg', '.png', ...]
    """
    return CATEGORY_MAPPING.copy()


def categorize_file(file_path: Path) -> str:
    """
    Determine the category for a file based on its extension.
    
    The function performs case-insensitive matching of file extensions
    against the CATEGORY_MAPPING. If no match is found, returns the
    DEFAULT_CATEGORY ("Others").
    
    Args:
        file_path: Path to the file
        
    Returns:
        Category name (e.g., "Images", "Videos", "Others")
        
    Example:
        >>> category = categorize_file(Path("photo.jpg"))
        >>> print(category)  # "Images"
    """
    # Get the file extension in lowercase for case-insensitive matching
    extension = file_path.suffix.lower()
    
    # Search through all categories
    for category, extensions in CATEGORY_MAPPING.items():
        if extension in extensions:
            logging.debug(f"File {file_path.name} categorized as {category}")
            return category
    
    # If no match found, return default category
    logging.debug(f"File {file_path.name} categorized as {DEFAULT_CATEGORY}")
    return DEFAULT_CATEGORY


# ============================================================================
# MOVER MODULE
# ============================================================================

def ensure_category_folder(
    base_dir: Path,
    category: str,
    dry_run: bool = True
) -> Path:
    """
    Ensure a category folder exists (or would exist in dry-run).
    
    Creates the category folder if it doesn't exist and dry_run is False.
    In dry-run mode, just returns the path without creating it.
    
    Args:
        base_dir: Base directory containing category folders
        category: Category name
        dry_run: If True, don't actually create the folder
        
    Returns:
        Path to the category folder
        
    Example:
        >>> folder = ensure_category_folder(Path("~/Downloads"), "Images", dry_run=False)
        >>> print(folder)  # ~/Downloads/Images
    """
    category_path = base_dir / category
    
    if not dry_run and not category_path.exists():
        category_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created category folder: {category}")
    elif dry_run and not category_path.exists():
        logging.debug(f"Would create category folder: {category}")
    
    return category_path


def resolve_collision(destination: Path) -> Path:
    """
    Resolve filename collision by appending numeric suffix.
    
    If the destination file exists, appends _1, _2, _3, etc. until
    a unique filename is found. Preserves the file extension.
    
    Args:
        destination: Intended destination path
        
    Returns:
        Path with unique filename
        
    Example:
        >>> path = resolve_collision(Path("~/Downloads/Images/photo.jpg"))
        >>> # If photo.jpg exists, returns photo_1.jpg
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
            logging.info(f"Collision detected, using: {new_name}")
            return new_path
        counter += 1


def move_file(
    source: Path,
    destination_dir: Path,
    new_name: Optional[str] = None,
    dry_run: bool = True
) -> Tuple[bool, Path]:
    """
    Move a file to the destination directory, handling collisions.
    
    Moves the file to the destination directory, optionally renaming it.
    Handles filename collisions by appending numeric suffixes. In dry-run
    mode, simulates the move without actually doing it.
    
    Args:
        source: Source file path
        destination_dir: Destination directory path
        new_name: Optional new filename (if renaming)
        dry_run: If True, simulate the move without actually doing it
        
    Returns:
        Tuple of (success: bool, final_destination: Path)
        
    Example:
        >>> success, dest = move_file(
        ...     Path("~/Downloads/photo.jpg"),
        ...     Path("~/Downloads/Images"),
        ...     dry_run=False
        ... )
    """
    try:
        # Determine the destination filename
        filename = new_name if new_name else source.name
        destination = destination_dir / filename
        
        # Resolve any collisions
        destination = resolve_collision(destination)
        
        if dry_run:
            logging.info(f"[DRY RUN] Would move: {source.name} -> {destination}")
            return True, destination
        else:
            # Actually move the file
            shutil.move(str(source), str(destination))
            logging.info(f"Moved: {source.name} -> {destination}")
            return True, destination
            
    except Exception as e:
        logging.error(f"Error moving {source.name}: {e}")
        return False, source


# ============================================================================
# RENAMER MODULE
# ============================================================================

def rename_file(
    original_name: str,
    pattern: str,
    index: int,
    extension: str
) -> str:
    """
    Apply a rename pattern to a filename.
    
    Replaces placeholders in the pattern:
    - {index} -> sequential number for this file
    - {name} -> original filename without extension
    - {ext} -> file extension without dot
    
    The file extension is always preserved in the final filename.
    
    Args:
        original_name: Original filename without extension
        pattern: Rename pattern with placeholders
        index: Sequential index for this file
        extension: File extension (including dot)
        
    Returns:
        New filename with extension
        
    Example:
        >>> new_name = rename_file("photo", "{index}_{name}", 5, ".jpg")
        >>> print(new_name)  # "5_photo.jpg"
    """
    result = pattern
    
    # Replace placeholders
    result = result.replace("{index}", str(index))
    result = result.replace("{name}", original_name)
    result = result.replace("{ext}", extension.lstrip('.'))
    
    # Ensure extension is included
    if not result.endswith(extension):
        result += extension
    
    logging.debug(f"Renamed: {original_name}{extension} -> {result}")
    return result


# ============================================================================
# ORCHESTRATOR MODULE
# ============================================================================

def organize(
    target_dir: str,
    dry_run: bool = True,
    rename_pattern: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, int]:
    """
    Organize files in the target directory.
    
    Scans the target directory, categorizes files by extension, creates
    category folders, and moves files to appropriate destinations. Optionally
    renames files according to a pattern. Handles errors gracefully and
    continues processing remaining files.
    
    Args:
        target_dir: Directory to organize
        dry_run: If True, simulate without making changes
        rename_pattern: Optional pattern for renaming files
        verbose: Enable verbose logging
        
    Returns:
        Dictionary mapping category names to file counts
        
    Example:
        >>> counts = organize("~/Downloads", dry_run=True)
        >>> print(f"Would organize {sum(counts.values())} files")
    """
    # Convert to Path object and expand user directory
    target_path = Path(target_dir).expanduser()
    
    # Validate target directory
    if not target_path.exists():
        logging.error(f"Target directory does not exist: {target_dir}")
        raise FileNotFoundError(f"Directory not found: {target_dir}")
    
    if not target_path.is_dir():
        logging.error(f"Target is not a directory: {target_dir}")
        raise NotADirectoryError(f"Not a directory: {target_dir}")
    
    # Log start of operation
    mode = "DRY RUN" if dry_run else "ACTUAL"
    logging.info(f"{'='*60}")
    logging.info(f"Starting organization [{mode}]")
    logging.info(f"Target directory: {target_path}")
    if rename_pattern:
        logging.info(f"Rename pattern: {rename_pattern}")
    logging.info(f"{'='*60}")
    
    # Scan directory for files
    files = scan_directory(target_path)
    logging.info(f"Found {len(files)} files to process")
    
    if len(files) == 0:
        logging.info("No files to organize")
        return {}
    
    # Track statistics
    category_counts: Dict[str, int] = {}
    category_indices: Dict[str, int] = {}  # For rename indexing
    errors: List[str] = []
    
    # Process each file
    for file_path in files:
        try:
            # Categorize the file
            category = categorize_file(file_path)
            
            # Initialize category counter if needed
            if category not in category_counts:
                category_counts[category] = 0
                category_indices[category] = 1
            
            # Ensure category folder exists
            category_folder = ensure_category_folder(
                target_path, category, dry_run
            )
            
            # Determine new filename if renaming
            new_name = None
            if rename_pattern:
                original_name = file_path.stem
                extension = file_path.suffix
                index = category_indices[category]
                new_name = rename_file(
                    original_name, rename_pattern, index, extension
                )
                category_indices[category] += 1
            
            # Move the file
            success, destination = move_file(
                file_path, category_folder, new_name, dry_run
            )
            
            if success:
                category_counts[category] += 1
            else:
                errors.append(f"Failed to move {file_path.name}")
                
        except Exception as e:
            error_msg = f"Error processing {file_path.name}: {e}"
            logging.error(error_msg)
            errors.append(error_msg)
            continue
    
    # Log summary
    logging.info(f"{'='*60}")
    logging.info("Organization Summary:")
    logging.info(f"{'='*60}")
    
    total_processed = sum(category_counts.values())
    for category, count in sorted(category_counts.items()):
        logging.info(f"  {category}: {count} files")
    
    logging.info(f"{'='*60}")
    logging.info(f"Total: {total_processed} files processed")
    
    if errors:
        logging.warning(f"Errors encountered: {len(errors)}")
        if verbose:
            for error in errors:
                logging.warning(f"  - {error}")
    
    logging.info(f"{'='*60}")
    
    return category_counts


# ============================================================================
# CLI AND LOGGING
# ============================================================================

def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging based on verbosity level.
    
    Args:
        verbose: If True, enable DEBUG level logging with timestamps
    """
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)s: %(message)s'
        )


def main() -> None:
    """
    Main entry point for the CLI.
    
    Parses command-line arguments, configures logging, validates inputs,
    and invokes the organize() function with appropriate parameters.
    """
    parser = argparse.ArgumentParser(
        description="Lazy Downloads Organizer - Automatically organize files by type",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview changes without making them)
  python -m lazy_downloader.organizer -t ~/Downloads --dry-run
  
  # Actually organize files
  python -m lazy_downloader.organizer -t ~/Downloads --no-dry-run
  
  # Organize with renaming
  python -m lazy_downloader.organizer -t ~/Downloads --no-dry-run -r "{index}_{name}"
  
  # Verbose output
  python -m lazy_downloader.organizer -t ~/Downloads --dry-run -v

Part of Kiro Week 2: Lazy Automation
        """
    )
    
    parser.add_argument(
        "-t", "--target",
        type=str,
        default="~/Downloads",
        help="Target directory to organize (default: ~/Downloads)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=True,
        help="Preview changes without making them (default)"
    )
    
    parser.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="dry_run",
        help="Actually move files (disables dry-run mode)"
    )
    
    parser.add_argument(
        "-r", "--rename",
        type=str,
        default=None,
        help='Rename pattern (e.g., "{index}_{name}"). Placeholders: {index}, {name}, {ext}'
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    try:
        # Run the organizer
        organize(
            target_dir=args.target,
            dry_run=args.dry_run,
            rename_pattern=args.rename,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        logging.info("\nOperation cancelled by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
