#!/usr/bin/env python3
"""
Demo script to show Lazy Downloads Organizer in action.

This creates a temporary directory with sample files and demonstrates
the organization process.
"""

import tempfile
import shutil
from pathlib import Path
from lazy_downloader.organizer import organize

def create_demo_files(demo_dir: Path):
    """Create sample files for demonstration."""
    files = [
        "vacation_photo.jpg",
        "screenshot.png",
        "tutorial_video.mp4",
        "meeting_notes.pdf",
        "report.docx",
        "podcast.mp3",
        "backup.zip",
        "script.py",
        "data.csv",
        "unknown_file.xyz"
    ]
    
    for filename in files:
        (demo_dir / filename).touch()
    
    print(f"✅ Created {len(files)} demo files in {demo_dir}\n")

def main():
    """Run the demonstration."""
    print("=" * 60)
    print("LAZY DOWNLOADS ORGANIZER - DEMO")
    print("=" * 60)
    print()
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        demo_path = Path(tmpdir)
        
        # Create demo files
        create_demo_files(demo_path)
        
        # Show files before organization
        print("📁 Files BEFORE organization:")
        print("-" * 60)
        for file in sorted(demo_path.iterdir()):
            if file.is_file():
                print(f"  {file.name}")
        print()
        
        # Run organization in dry-run mode
        print("🔍 Running DRY RUN (preview mode)...")
        print("=" * 60)
        organize(str(demo_path), dry_run=True, verbose=False)
        print()
        
        # Run actual organization
        print("🚀 Running ACTUAL organization...")
        print("=" * 60)
        organize(str(demo_path), dry_run=False, verbose=False)
        print()
        
        # Show structure after organization
        print("📁 Structure AFTER organization:")
        print("-" * 60)
        for item in sorted(demo_path.iterdir()):
            if item.is_dir():
                print(f"  📂 {item.name}/")
                for file in sorted(item.iterdir()):
                    print(f"      {file.name}")
        print()
        
        print("=" * 60)
        print("✅ Demo complete!")
        print("=" * 60)
        print()
        print("💡 To organize your actual Downloads folder:")
        print("   python3 organize.py -t ~/Downloads --dry-run")
        print("   python3 organize.py -t ~/Downloads --no-dry-run")
        print()

if __name__ == "__main__":
    main()
