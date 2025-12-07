# 🎉 Welcome to Lazy Downloads Organizer!

**"I hate cleaning my messy Downloads folder, so I automated it."**

## ⚡ 3-Step Quick Start

### Step 1: Run the Demo (30 seconds)
```bash
python3 demo.py
```
This shows you how the tool works in a safe test environment.

### Step 2: Preview Your Downloads (30 seconds)
```bash
python3 organize.py -t ~/Downloads --dry-run
```
This shows you what WOULD happen (no actual changes).

### Step 3: Organize Your Downloads (5 seconds)
```bash
python3 organize.py -t ~/Downloads --no-dry-run
```
This actually organizes your files!

## ✅ That's It!

Your Downloads folder is now organized into categories:
- 📸 Images
- 🎬 Videos  
- 📄 Documents
- 🎵 Audio
- 📦 Archives
- 💻 Code
- 📁 Others

## 📚 Want to Learn More?

### Quick References
- **[QUICKSTART.md](QUICKSTART.md)** - 60-second guide
- **[README.md](README.md)** - Complete documentation
- **[FEATURES.md](FEATURES.md)** - All features explained

### Full Documentation
- **[INDEX.md](INDEX.md)** - Complete documentation index
- **[INSTALLATION.md](INSTALLATION.md)** - Setup guide
- **[blog_post.md](blog_post.md)** - Detailed article

## 🎮 Try These Commands

```bash
# Organize a different folder
python3 organize.py -t /path/to/folder --no-dry-run

# Rename files while organizing
python3 organize.py -t ~/Downloads --no-dry-run -r "{index}_{name}"

# See detailed logs
python3 organize.py -t ~/Downloads --dry-run -v

# Get help
python3 organize.py --help
```

## 🛡️ Safety Features

- ✅ **Dry-run by default** - Always preview first
- ✅ **Never overwrites files** - Adds _1, _2, etc. if needed
- ✅ **Error resilient** - Continues even if some files fail
- ✅ **Detailed logging** - Know exactly what's happening

## 💡 Pro Tips

1. **Always run --dry-run first** to preview changes
2. **Use -v for verbose** to see detailed logs
3. **Check examples/sample_run.txt** to see what output looks like
4. **Read FEATURES.md** to discover all capabilities

## 🆘 Need Help?

1. Run `python3 organize.py --help`
2. Check [QUICKSTART.md](QUICKSTART.md)
3. Read [INSTALLATION.md](INSTALLATION.md)
4. See [examples/sample_run.txt](examples/sample_run.txt)

## 🎯 What This Tool Does

**Before:**
```
~/Downloads/
├── photo.jpg
├── video.mp4
├── document.pdf
├── song.mp3
├── archive.zip
├── script.py
└── random.xyz
```

**After:**
```
~/Downloads/
├── Images/
│   └── photo.jpg
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
    └── random.xyz
```

## 🚀 Ready? Let's Go!

```bash
# 1. See it in action
python3 demo.py

# 2. Preview your Downloads
python3 organize.py -t ~/Downloads --dry-run

# 3. Organize for real!
python3 organize.py -t ~/Downloads --no-dry-run
```

---

**Built with ❤️ and a healthy dose of laziness**

*Part of Kiro Week 2: Lazy Automation*

**Questions?** Check [INDEX.md](INDEX.md) for all documentation!
