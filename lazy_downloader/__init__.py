"""
Lazy Downloads Organizer

A Python tool to automatically organize files in your Downloads folder
by categorizing them based on file extensions.

Part of Kiro Week 2: Lazy Automation
"""

__version__ = "0.1.0"
__author__ = "YOUR NAME"
__description__ = "Automatically organizes the Downloads folder by file type"

from lazy_downloader.organizer import organize, main

__all__ = ["organize", "main"]
