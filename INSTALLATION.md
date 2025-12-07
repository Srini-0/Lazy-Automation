# 📦 Installation & Setup Guide

Complete installation instructions for Lazy Downloads Organizer.

## Prerequisites

- **Python 3.8 or higher**
- **Operating System**: macOS, Linux, or Windows

### Check Python Version

```bash
python3 --version
# or
python --version
```

Should show Python 3.8 or higher.

## Installation Methods

### Method 1: Direct Download (Recommended)

1. **Download the project**
   ```bash
   # If you have git
   git clone [YOUR_GITHUB_REPO_URL]
   cd lazy_downloads_organizer
   
   # Or download and extract the ZIP file
   ```

2. **Verify installation**
   ```bash
   python3 organize.py --help
   ```

3. **Run the demo**
   ```bash
   python3 demo.py
   ```

That's it! No dependencies to install for basic usage.

### Method 2: With Testing Dependencies

If you want to run tests or contribute to development:

1. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## Platform-Specific Instructions

### macOS

```bash
# Python 3 is usually pre-installed
python3 --version

# If not installed, install via Homebrew
brew install python3

# Navigate to project and run
cd lazy_downloads_organizer
python3 organize.py -t ~/Downloads --dry-run
```

### Linux

```bash
# Check Python installation
python3 --version

# If not installed (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3

# If not installed (Fedora/RHEL)
sudo dnf install python3

# Navigate to project and run
cd lazy_downloads_organizer
python3 organize.py -t ~/Downloads --dry-run
```

### Windows

```bash
# Check Python installation
python --version

# If not installed, download from python.org
# https://www.python.org/downloads/

# Navigate to project and run
cd lazy_downloads_organizer
python organize.py -t %USERPROFILE%\Downloads --dry-run
```

## Verify Installation

Run these commands to verify everything works:

```bash
# 1. Check help
python3 organize.py --help

# 2. Run demo
python3 demo.py

# 3. Test on Downloads (dry-run, safe!)
python3 organize.py -t ~/Downloads --dry-run
```

## Configuration

### Default Settings

- **Target Directory**: `~/Downloads`
- **Mode**: Dry-run (safe preview)
- **Logging**: INFO level

### Customization

No configuration file needed! All options are via command-line:

```bash
# Change target directory
python3 organize.py -t /path/to/folder --dry-run

# Enable verbose logging
python3 organize.py -t ~/Downloads --dry-run -v

# Use rename pattern
python3 organize.py -t ~/Downloads --no-dry-run -r "{index}_{name}"
```

## Troubleshooting

### "python: command not found"

Try `python3` instead of `python`:
```bash
python3 organize.py --help
```

### "Permission denied"

Make sure you have read/write access to the target directory:
```bash
ls -la ~/Downloads
```

### "Module not found"

Make sure you're in the project directory:
```bash
cd lazy_downloads_organizer
python3 organize.py --help
```

### Windows Path Issues

Use Windows-style paths:
```bash
python organize.py -t C:\Users\YourName\Downloads --dry-run
```

## Uninstallation

Simply delete the project directory:
```bash
rm -rf lazy_downloads_organizer
```

No system files are modified, no registry entries, no global installations.

## Updating

To get the latest version:

```bash
cd lazy_downloads_organizer
git pull origin main
```

Or download the latest ZIP and replace your files.

## Optional: Make it Globally Accessible

### macOS/Linux

Add an alias to your shell configuration:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias organize-downloads="python3 /path/to/lazy_downloads_organizer/organize.py"

# Then use anywhere:
organize-downloads -t ~/Downloads --dry-run
```

### Create a Symlink

```bash
sudo ln -s /path/to/lazy_downloads_organizer/organize.py /usr/local/bin/organize-downloads
chmod +x /path/to/lazy_downloads_organizer/organize.py

# Then use anywhere:
organize-downloads -t ~/Downloads --dry-run
```

## Next Steps

1. ✅ **Read the Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
2. 📖 **Read the Full Documentation**: See [README.md](README.md)
3. 🎮 **Run the Demo**: `python3 demo.py`
4. 🚀 **Organize Your Downloads**: `python3 organize.py -t ~/Downloads --dry-run`

## Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the README and documentation
- **Contributions**: Pull requests welcome!

---

**Happy organizing! 🎉**
