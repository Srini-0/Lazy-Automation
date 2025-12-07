# Implementation Plan

- [x] 1. Set up project structure and configuration
  - Create the lazy_downloader package directory
  - Create __init__.py with version info and package metadata
  - Create .kiro/config.json with project configuration
  - Create requirements.txt with pytest and hypothesis
  - Create LICENSE file with MIT License template
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.6, 10.7_

- [x] 2. Implement core data models and constants
  - Define CATEGORY_MAPPING dictionary with all file extension mappings
  - Create FileInfo dataclass for file information
  - Create OrganizationResult dataclass for operation results
  - Add type hints and docstrings
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [-] 3. Implement file scanner module
  - Create scan_directory() function to find all files in target directory
  - Filter out directories and only return regular files
  - Extract file extensions correctly
  - Add comprehensive docstrings and type hints
  - _Requirements: 1.1_

- [ ] 3.1 Write property test for file scanning
  - **Property 1: File scanning completeness**
  - **Validates: Requirements 1.1**

- [-] 4. Implement file categorizer module
  - Create get_category_mapping() function to return category mappings
  - Create categorize_file() function to determine category from extension
  - Handle case-insensitive extension matching
  - Default to "Others" category for unknown extensions
  - Add comprehensive docstrings and type hints
  - _Requirements: 1.2, 2.7_

- [ ] 4.1 Write property test for categorization
  - **Property 2: Categorization correctness**
  - **Validates: Requirements 1.2**

- [ ] 4.2 Write unit tests for category mappings
  - Test sample files from each category
  - Test unknown extensions map to "Others"
  - Test case-insensitive matching
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [-] 5. Implement file mover module
  - Create ensure_category_folder() function to create folders as needed
  - Create move_file() function with dry-run support
  - Implement collision detection and resolution with numeric suffixes
  - Ensure file extensions are always preserved
  - Add comprehensive docstrings and type hints
  - _Requirements: 1.3, 3.1, 3.2, 3.4, 8.1, 8.2, 8.3, 8.5_

- [ ] 5.1 Write property test for folder creation
  - **Property 5: Category folder creation**
  - **Validates: Requirements 3.2**

- [ ] 5.2 Write property test for folder idempotence
  - **Property 6: Folder idempotence**
  - **Validates: Requirements 3.4**

- [ ] 5.3 Write property test for collision handling
  - **Property 11: Collision detection and resolution**
  - **Validates: Requirements 5.6, 8.1, 8.2**

- [ ] 5.4 Write property test for no overwriting
  - **Property 12: No file overwriting**
  - **Validates: Requirements 8.5**

- [ ] 5.5 Write unit tests for mover module
  - Test moving single file
  - Test collision with existing file
  - Test folder creation
  - _Requirements: 1.3, 3.2, 8.2_

- [-] 6. Implement file renamer module
  - Create rename_file() function to apply rename patterns
  - Implement placeholder substitution for {index}, {name}, {ext}
  - Ensure extensions are preserved in renamed files
  - Handle edge cases (empty names, special characters)
  - Add comprehensive docstrings and type hints
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 6.1 Write property test for rename pattern application
  - **Property 9: Rename pattern application**
  - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

- [ ] 6.2 Write property test for extension preservation
  - **Property 10: Extension preservation**
  - **Validates: Requirements 5.5, 8.3**

- [ ] 6.3 Write unit tests for renamer module
  - Test each placeholder type individually
  - Test patterns with multiple placeholders
  - Test patterns with no placeholders
  - _Requirements: 5.2, 5.3, 5.4_

- [-] 7. Implement orchestrator module
  - Create organize() function to coordinate the organization process
  - Scan directory and categorize all files
  - Create category folders as needed
  - Move files to appropriate destinations
  - Apply rename patterns if specified
  - Track statistics (files moved per category)
  - Handle errors gracefully and continue processing
  - Return OrganizationResult with summary
  - Add comprehensive docstrings and type hints
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 7.4_

- [ ] 7.1 Write property test for file destination correctness
  - **Property 3: File destination correctness**
  - **Validates: Requirements 1.3**

- [ ] 7.2 Write property test for count accuracy
  - **Property 4: Count accuracy**
  - **Validates: Requirements 1.4**

- [ ] 8. Implement dry-run mode support
  - Ensure dry-run flag is respected throughout the codebase
  - Verify no file system modifications occur in dry-run mode
  - Display planned actions with source and destination paths
  - Report accurate counts of what would be moved
  - Add clear indicators that dry-run mode is active
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 7.5_

- [ ] 8.1 Write property test for dry-run immutability
  - **Property 7: Dry-run immutability**
  - **Validates: Requirements 4.1, 4.4, 4.5**

- [ ] 8.2 Write property test for dry-run count accuracy
  - **Property 8: Dry-run count accuracy**
  - **Validates: Requirements 4.3**

- [ ] 8.3 Write unit tests for dry-run mode
  - Test that no folders are created
  - Test that no files are moved
  - Test that output shows planned actions
  - _Requirements: 4.2, 4.4, 4.5_

- [-] 9. Implement CLI with argparse
  - Create argument parser with all required flags
  - Add --target/-t flag for directory path (default: ~/Downloads)
  - Add --dry-run/--no-dry-run flag (default: --dry-run)
  - Add --rename/-r flag for rename pattern
  - Add --verbose/-v flag for detailed logging
  - Add --help documentation for all arguments
  - Validate arguments and provide clear error messages
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_

- [ ] 10. Implement logging and user feedback
  - Create setup_logging() function to configure logging based on verbosity
  - Log target directory at start
  - Log each file move with source and destination
  - Display summary with counts per category
  - Log errors with descriptive messages
  - Clearly indicate dry-run mode when active
  - Add verbose mode for detailed operation logging
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ] 11. Implement main entry point
  - Create main() function to tie everything together
  - Parse CLI arguments
  - Configure logging
  - Validate target directory exists
  - Call organize() with appropriate parameters
  - Display final summary
  - Handle top-level exceptions gracefully
  - Add if __name__ == "__main__" block
  - _Requirements: 1.5, 6.1, 7.1, 7.3_

- [ ] 11.1 Write integration tests
  - Test complete workflow with various file types
  - Test with different CLI argument combinations
  - Test error recovery scenarios
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 12. Add comprehensive documentation
  - Add module-level docstring to organizer.py
  - Add docstrings to all functions with parameters and return values
  - Add inline comments for complex logic
  - Include type hints for all function signatures
  - Document collision handling algorithm
  - Document rename pattern processing
  - _Requirements: 9.1, 9.2, 9.4, 9.5_

- [ ] 13. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Create README documentation
  - Write project title and overview
  - Explain the problem and motivation
  - List all features
  - Provide installation instructions
  - Include usage examples with code blocks
  - Show example commands for dry-run and actual execution
  - Include before/after scenarios
  - Add troubleshooting section
  - Mention Kiro usage in development
  - Add MIT License section
  - _Requirements: 9.3, 10.5_

- [ ] 15. Create example output file
  - Create examples/sample_run.txt
  - Include mock dry-run output with 8-10 planned moves
  - Demonstrate log format with timestamps
  - Show summary statistics
  - Include examples of different file types
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 16. Create blog post for AWS Builder Center
  - Write title: "I hate sorting my Downloads folder, so I automated it using Python + Kiro"
  - Write introduction explaining the problem and frustration
  - Describe what the script does
  - Explain how Kiro accelerated development
  - Include code snippets from the implementation
  - Add screenshot placeholders (Before, Dry Run, After)
  - Provide step-by-step instructions for running the tool
  - Discuss results and time saved
  - Suggest future improvements
  - Add GitHub repository link placeholder
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 17. Final validation and polish
  - Test on a real Downloads folder with diverse files
  - Verify all CLI arguments work correctly
  - Verify dry-run mode is safe
  - Verify collision handling works
  - Verify rename patterns work
  - Check all documentation is accurate
  - Ensure code follows Python best practices
  - _Requirements: 1.1, 1.2, 1.3, 4.1, 5.1, 8.1_
