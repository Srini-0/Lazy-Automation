"""
Unit and property-based tests for the Lazy Downloads Organizer.

This test suite validates the correctness of file organization functionality
using both traditional unit tests and property-based tests with Hypothesis.
"""

import tempfile
import shutil
from pathlib import Path
from typing import List

import pytest
from hypothesis import given, strategies as st

from lazy_downloader.organizer import (
    categorize_file,
    get_category_mapping,
    rename_file,
    resolve_collision,
    scan_directory,
    ensure_category_folder,
)


# ============================================================================
# UNIT TESTS - Categorizer Module
# ============================================================================

class TestCategorizer:
    """Unit tests for file categorization."""
    
    def test_categorize_image_files(self):
        """Test that image files are correctly categorized."""
        assert categorize_file(Path("photo.jpg")) == "Images"
        assert categorize_file(Path("screenshot.PNG")) == "Images"
        assert categorize_file(Path("icon.svg")) == "Images"
    
    def test_categorize_video_files(self):
        """Test that video files are correctly categorized."""
        assert categorize_file(Path("movie.mp4")) == "Videos"
        assert categorize_file(Path("clip.AVI")) == "Videos"
        assert categorize_file(Path("tutorial.mkv")) == "Videos"
    
    def test_categorize_document_files(self):
        """Test that document files are correctly categorized."""
        assert categorize_file(Path("report.pdf")) == "Documents"
        assert categorize_file(Path("essay.DOCX")) == "Documents"
        assert categorize_file(Path("data.csv")) == "Documents"
    
    def test_categorize_audio_files(self):
        """Test that audio files are correctly categorized."""
        assert categorize_file(Path("song.mp3")) == "Audio"
        assert categorize_file(Path("podcast.WAV")) == "Audio"
        assert categorize_file(Path("audio.flac")) == "Audio"
    
    def test_categorize_archive_files(self):
        """Test that archive files are correctly categorized."""
        assert categorize_file(Path("backup.zip")) == "Archives"
        assert categorize_file(Path("files.RAR")) == "Archives"
        assert categorize_file(Path("archive.7z")) == "Archives"
    
    def test_categorize_code_files(self):
        """Test that code files are correctly categorized."""
        assert categorize_file(Path("script.py")) == "Code"
        assert categorize_file(Path("app.JS")) == "Code"
        assert categorize_file(Path("style.css")) == "Code"
    
    def test_categorize_unknown_files(self):
        """Test that unknown file types go to Others category."""
        assert categorize_file(Path("unknown.xyz")) == "Others"
        assert categorize_file(Path("file.abc123")) == "Others"
        assert categorize_file(Path("noextension")) == "Others"
    
    def test_case_insensitive_categorization(self):
        """Test that categorization is case-insensitive."""
        assert categorize_file(Path("file.JPG")) == "Images"
        assert categorize_file(Path("file.Jpg")) == "Images"
        assert categorize_file(Path("file.jpg")) == "Images"
    
    def test_get_category_mapping(self):
        """Test that category mapping is returned correctly."""
        mapping = get_category_mapping()
        assert "Images" in mapping
        assert "Videos" in mapping
        assert ".jpg" in mapping["Images"]
        assert ".mp4" in mapping["Videos"]


# ============================================================================
# UNIT TESTS - Renamer Module
# ============================================================================

class TestRenamer:
    """Unit tests for file renaming."""
    
    def test_rename_with_index(self):
        """Test renaming with {index} placeholder."""
        result = rename_file("photo", "{index}", 5, ".jpg")
        assert result == "5.jpg"
    
    def test_rename_with_name(self):
        """Test renaming with {name} placeholder."""
        result = rename_file("photo", "{name}", 1, ".jpg")
        assert result == "photo.jpg"
    
    def test_rename_with_ext(self):
        """Test renaming with {ext} placeholder."""
        result = rename_file("photo", "file.{ext}", 1, ".jpg")
        assert result == "file.jpg.jpg"  # Extension added at end
    
    def test_rename_with_multiple_placeholders(self):
        """Test renaming with multiple placeholders."""
        result = rename_file("vacation_photo", "{index}_{name}", 3, ".jpg")
        assert result == "3_vacation_photo.jpg"
    
    def test_rename_preserves_extension(self):
        """Test that extension is always preserved."""
        result = rename_file("file", "renamed", 1, ".txt")
        assert result.endswith(".txt")
    
    def test_rename_with_no_placeholders(self):
        """Test renaming with no placeholders."""
        result = rename_file("old", "new", 1, ".txt")
        assert result == "new.txt"


# ============================================================================
# UNIT TESTS - Scanner Module
# ============================================================================

class TestScanner:
    """Unit tests for directory scanning."""
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = scan_directory(Path(tmpdir))
            assert len(files) == 0
    
    def test_scan_directory_with_files(self):
        """Test scanning a directory with files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test files
            (tmppath / "file1.txt").touch()
            (tmppath / "file2.jpg").touch()
            (tmppath / "file3.pdf").touch()
            
            files = scan_directory(tmppath)
            assert len(files) == 3
            assert all(f.is_file() for f in files)
    
    def test_scan_ignores_subdirectories(self):
        """Test that scanning ignores subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create files and subdirectory
            (tmppath / "file1.txt").touch()
            (tmppath / "subdir").mkdir()
            (tmppath / "subdir" / "file2.txt").touch()
            
            files = scan_directory(tmppath)
            assert len(files) == 1  # Only file1.txt, not subdir or file2.txt


# ============================================================================
# UNIT TESTS - Mover Module
# ============================================================================

class TestMover:
    """Unit tests for file moving operations."""
    
    def test_ensure_category_folder_creates_folder(self):
        """Test that category folder is created when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            category_path = ensure_category_folder(tmppath, "Images", dry_run=False)
            
            assert category_path.exists()
            assert category_path.is_dir()
            assert category_path.name == "Images"
    
    def test_ensure_category_folder_dry_run(self):
        """Test that dry-run doesn't create folders."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            category_path = ensure_category_folder(tmppath, "Images", dry_run=True)
            
            assert not category_path.exists()
            assert category_path.name == "Images"
    
    def test_resolve_collision_no_conflict(self):
        """Test collision resolution when no conflict exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "file.txt"
            result = resolve_collision(dest)
            assert result == dest
    
    def test_resolve_collision_with_conflict(self):
        """Test collision resolution when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create existing file
            existing = tmppath / "file.txt"
            existing.touch()
            
            # Resolve collision
            result = resolve_collision(existing)
            assert result != existing
            assert result.stem == "file_1"
            assert result.suffix == ".txt"
    
    def test_resolve_collision_multiple_conflicts(self):
        """Test collision resolution with multiple existing files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create multiple existing files
            (tmppath / "file.txt").touch()
            (tmppath / "file_1.txt").touch()
            (tmppath / "file_2.txt").touch()
            
            # Resolve collision
            result = resolve_collision(tmppath / "file.txt")
            assert result.stem == "file_3"
            assert result.suffix == ".txt"


# ============================================================================
# PROPERTY-BASED TESTS
# ============================================================================

class TestProperties:
    """Property-based tests using Hypothesis."""
    
    # Feature: lazy-downloads-organizer, Property 2: Categorization correctness
    @given(st.sampled_from([".jpg", ".mp4", ".pdf", ".mp3", ".zip", ".py"]))
    def test_known_extensions_categorize_correctly(self, extension: str):
        """For any known extension, categorization should return a valid category."""
        file_path = Path(f"test{extension}")
        category = categorize_file(file_path)
        
        # Should not be "Others" for known extensions
        assert category != "Others"
        
        # Should be one of the defined categories
        mapping = get_category_mapping()
        assert category in mapping.keys()
    
    # Feature: lazy-downloads-organizer, Property 10: Extension preservation
    @given(
        original_name=st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_characters="/\\")),
        pattern=st.sampled_from(["{index}", "{name}", "{index}_{name}"]),
        index=st.integers(min_value=1, max_value=100),
        extension=st.sampled_from([".jpg", ".txt", ".pdf", ".mp3"])
    )
    def test_rename_preserves_extension(self, original_name: str, pattern: str, 
                                       index: int, extension: str):
        """For any rename operation, the file extension should be preserved."""
        result = rename_file(original_name, pattern, index, extension)
        assert result.endswith(extension)
    
    # Feature: lazy-downloads-organizer, Property 1: File scanning completeness
    @given(st.integers(min_value=0, max_value=10))
    def test_scan_finds_all_files(self, num_files: int):
        """For any directory, scanning should find all regular files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create random number of files
            for i in range(num_files):
                (tmppath / f"file{i}.txt").touch()
            
            files = scan_directory(tmppath)
            assert len(files) == num_files


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_organization_workflow(self):
        """Test the complete organization workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test files
            (tmppath / "photo.jpg").touch()
            (tmppath / "video.mp4").touch()
            (tmppath / "document.pdf").touch()
            
            # Scan and categorize
            files = scan_directory(tmppath)
            assert len(files) == 3
            
            # Categorize each file
            categories = [categorize_file(f) for f in files]
            assert "Images" in categories
            assert "Videos" in categories
            assert "Documents" in categories


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
