# 🚀 Quick Start Guide

Get started with Lazy Downloads Organizer in 60 seconds!

## Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher
```

## Step 2: Navigate to Project Directory

```bash
cd lazy_downloads_organizer
```

## Step 3: Preview What Will Happen (Safe!)

```bash
python organize.py -t ~/Downloads --dry-run
```

This shows you exactly what the tool will do **without making any changes**.

## Step 4: Review the Output

You'll see something like:

```
============================================================
Starting organization [DRY RUN]
Target directory: /Users/you/Downloads
============================================================
INFO: Found 47 files to process
INFO: [DRY RUN] Would move: photo.jpg -> ~/Downloads/Images/photo.jpg
INFO: [DRY RUN] Would move: video.mp4 -> ~/Downloads/Videos/video.mp4
...
============================================================
Organization Summary:
============================================================
  Images: 12 files
  Videos: 5 files
  Documents: 18 files
  ...
============================================================
```

## Step 5: Actually Organize Your Files

If you're happy with the preview:

```bash
python organize.py -t ~/Downloads --no-dry-run
```

## 🎉 Done!

Your Downloads folder is now organized!

---

## 💡 Pro Tips

### Organize a Different Folder
```bash
python organize.py -t /path/to/folder --no-dry-run
```

### Rename Files While Organizing
```bash
python organize.py -t ~/Downloads --no-dry-run -r "{index}_{name}"
```

This creates files like: `1_photo.jpg`, `2_document.pdf`, etc.

### See Detailed Logs
```bash
python organize.py -t ~/Downloads --dry-run -v
```

### Get Help
```bash
python organize.py --help
```

---

## 🔒 Safety First

- **Always run with `--dry-run` first** to preview changes
- The tool **never overwrites files** (adds _1, _2, etc. if needed)
- **Dry-run is the default** - you must explicitly use `--no-dry-run` to make changes

---

## 📁 What Gets Organized?

| Category | File Types |
|----------|------------|
| 📸 Images | jpg, png, gif, svg, webp, bmp |
| 🎬 Videos | mp4, avi, mkv, mov, wmv, flv |
| 📄 Documents | pdf, docx, txt, xlsx, pptx, csv |
| 🎵 Audio | mp3, wav, flac, aac, ogg |
| 📦 Archives | zip, rar, 7z, tar, gz |
| 💻 Code | py, js, html, css, java, cpp |
| 📁 Others | Everything else |

---

## ❓ Troubleshooting

**"Permission denied"**
- Make sure you have read/write access to the folder

**"Files not moving"**
- Did you use `--no-dry-run`? Dry-run is the default!

**"Command not found"**
- Make sure you're in the project directory
- Try `python3` instead of `python`

---

## 📚 Learn More

- Full documentation: See [README.md](README.md)
- Example outputs: See [examples/sample_run.txt](examples/sample_run.txt)
- Blog post: See [blog_post.md](blog_post.md)

---

**Happy organizing! 🎉**
