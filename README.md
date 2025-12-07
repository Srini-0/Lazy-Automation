# 🗂️ Lazy Downloads Organizer

> "I hate cleaning my messy Downloads folder, so I automated it."

**Part of Kiro Week 2: Lazy Automation**

A Python command-line tool that automatically organizes your Downloads folder by categorizing files based on their extensions and moving them into appropriate category folders.

## 🎯 The Problem

We've all been there - your Downloads folder is a chaotic mess of files. PDFs mixed with images, videos buried under zip files, and that one important document you can't find anymore. Manually sorting through hundreds of files is tedious and time-consuming.

## ✨ The Solution

This tool automates the entire process! It scans your Downloads folder, categorizes files by type, creates organized folders, and moves everything to the right place - all in seconds.

## 🚀 Features

- **Automatic Categorization**: Organizes files into 7 categories
  - 📸 Images (jpg, png, gif, svg, webp, etc.)
  - 🎬 Videos (mp4, avi, mkv, mov, etc.)
  - 📄 Documents (pdf, docx, txt, xlsx, pptx, etc.)
  - 🎵 Audio (mp3, wav, flac, aac, etc.)
  - 📦 Archives (zip, rar, 7z, tar, gz, etc.)
  - 💻 Code (py, js, html, css, java, etc.)
  - 📁 Others (everything else)

- **Safe Dry-Run Mode**: Preview changes before making them
- **Smart Collision Handling**: Never overwrites files (adds _1, _2, etc.)
- **Custom Renaming**: Rename files with patterns like `{index}_{name}`
- **Verbose Logging**: See exactly what's happening
- **Error Resilient**: Continues processing even if individual files fail

## 📦 Installation

1. **Clone or download this repository**

2. **Install dependencies** (optional, only needed for testing):
```bash
pip install -r requirements.txt
```

3. **That's it!** The tool uses only Python standard library for core functionality.

## 🎮 Usage

### Basic Usage - Dry Run (Safe Preview)

```bash
# Preview what would happen (no actual changes)
python -m lazy_downloader.organizer -t ~/Downloads --dry-run
```

### Actually Organize Files

```bash
# Organize your Downloads folder
python -m lazy_downloader.organizer -t ~/Downloads --no-dry-run
```

### Organize a Different Directory

```bash
# Organize any directory
python -m lazy_downloader.organizer -t /path/to/directory --no-dry-run
```

### Rename Files While Organizing

```bash
# Rename files with pattern: 1_photo.jpg, 2_document.pdf, etc.
python -m lazy_downloader.organizer -t ~/Downloads --no-dry-run -r "{index}_{name}"
```

### Verbose Output

```bash
# See detailed logging
python -m lazy_downloader.organizer -t ~/Downloads --dry-run -v
```

## 📊 Example Output

### Before:
```
~/Downloads/
├── photo.jpg
├── video.mp4
├── document.pdf
├── song.mp3
├── archive.zip
├── script.py
├── random_file.xyz
└── another_photo.png
```

### After Running:
```
~/Downloads/
├── Images/
│   ├── photo.jpg
│   └── another_photo.png
├── Videos/
│   └── video.mp4
├── Documents/
│   └── document.pdf
├── Audio/
│   └── song.mp3
├── Archives/
│   └── archive.zip
├── Code/
│   └── script.py
└── Others/
    └── random_file.xyz
```

### Sample Dry-Run Output:
```
============================================================
Starting organization [DRY RUN]
Target directory: /Users/you/Downloads
============================================================
INFO: Found 8 files to process
INFO: [DRY RUN] Would move: photo.jpg -> /Users/you/Downloads/Images/photo.jpg
INFO: [DRY RUN] Would move: video.mp4 -> /Users/you/Downloads/Videos/video.mp4
INFO: [DRY RUN] Would move: document.pdf -> /Users/you/Downloads/Documents/document.pdf
INFO: [DRY RUN] Would move: song.mp3 -> /Users/you/Downloads/Audio/song.mp3
INFO: [DRY RUN] Would move: archive.zip -> /Users/you/Downloads/Archives/archive.zip
INFO: [DRY RUN] Would move: script.py -> /Users/you/Downloads/Code/script.py
INFO: [DRY RUN] Would move: random_file.xyz -> /Users/you/Downloads/Others/random_file.xyz
INFO: [DRY RUN] Would move: another_photo.png -> /Users/you/Downloads/Images/another_photo.png
============================================================
Organization Summary:
============================================================
  Archives: 1 files
  Audio: 1 files
  Code: 1 files
  Documents: 1 files
  Images: 2 files
  Others: 1 files
  Videos: 1 files
============================================================
Total: 8 files processed
============================================================
```

## 🛠️ Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-t`, `--target` | Target directory to organize | `~/Downloads` |
| `--dry-run` | Preview changes without making them | Enabled |
| `--no-dry-run` | Actually move files | Disabled |
| `-r`, `--rename` | Rename pattern (e.g., `{index}_{name}`) | None |
| `-v`, `--verbose` | Enable detailed logging | Disabled |
| `-h`, `--help` | Show help message | - |

### Rename Pattern Placeholders:
- `{index}` - Sequential number (1, 2, 3, ...)
- `{name}` - Original filename without extension
- `{ext}` - File extension without dot

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=lazy_downloader
```

## 🤖 Built with Kiro

This project was developed with assistance from **Kiro**, an AI-powered IDE that accelerated the development process through:
- Automated code generation with best practices
- Comprehensive testing strategy
- Documentation generation
- Error handling patterns

Kiro helped transform a simple idea into a production-ready tool in a fraction of the time!

## 📝 Project Structure

```
lazy_downloads_organizer/
├── lazy_downloader/
│   ├── __init__.py          # Package initialization
│   └── organizer.py         # Main module with all functionality
├── examples/
│   └── sample_run.txt       # Example output
├── .kiro/
│   ├── specs/               # Project specifications
│   └── config.json          # Project configuration
├── README.md                # This file
├── requirements.txt         # Python dependencies
└── LICENSE                  # MIT License
```

## 🔒 Safety Features

- **Dry-run by default**: Always preview changes first
- **No overwrites**: Automatically handles filename collisions
- **Error resilience**: Continues processing even if individual files fail
- **Detailed logging**: Know exactly what's happening

## 🐛 Troubleshooting

**Permission Errors**: Make sure you have read/write permissions for the target directory.

**Files Not Moving**: Check that you're using `--no-dry-run` flag.

**Missing Categories**: Unknown file types go to "Others" folder automatically.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built as part of Kiro Week 2: Lazy Automation challenge
- Developed with Kiro AI assistance
- Inspired by the universal frustration of messy Downloads folders

## 🚀 Future Enhancements

- Configuration file for custom categories
- Undo functionality
- Watch mode for automatic organization
- GUI interface
- Cloud storage integration
- Duplicate file detection

---

**Made with ❤️ and a healthy dose of laziness**

*Because life's too short to manually organize files!*
