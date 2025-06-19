# 🎬 Movie Organizer Script

A powerful Python script that helps you automatically organize, rename, and clean up your downloaded movie/video collection. It detects duplicates, prompts you to choose which files to keep, fetches missing metadata from IMDb, and standardizes folder structures.

## ✨ Features

* 📦 Merge duplicate folders with similar names.
* 🎮 Rename video and subtitle files to match folder names.
* 🗘️ Handles multiple video files in a folder with interactive selection.
* 🌐 Fetches missing movie years from IMDb.
* ✍️ Prompt user input for ambiguous movie titles.
* 📁 Groups loose files into titled folders.
* ✅ Works cross-platform (macOS, Linux, Windows).

## 🧠 Smart Scenarios Covered

1. **Messy Mixed Files** → Prompted to group, pick best quality, and rename.
2. **Duplicate Folder Names** → Merged, files consolidated.
3. **Loose Files** → Automatically grouped into folders using IMDb.
4. **Subtitle Set Handling** → Subtitles renamed and matched.
5. **Weird Folder Names** → Cleaned up with correct naming.
6. **Multiple Quality Videos** → User chooses which one to keep.
7. **Missing Year Metadata** → Fetched from IMDb or asked from user.
8. **Clean Folder With New Files** → New files merged and renamed.
9. **Folders with Subtitles Only** → Left untouched.
10. **Reruns Safe** → Skips already organized content.
11. **Wrong Match?** → Create new folder and choose what to move.

## 🛠️ Requirements

```bash
pip install IMDbPY
```

## 🚀 Usage

```bash
python main.py
```

The script will:

* Group loose video/subtitle files
* Detect and merge duplicate folders
* Ask for choices when needed (for multiple video files)
* Rename and clean all folders to a consistent structure

## 👥 Contributions

Contributions are welcome! Feel free to fork, improve, and submit pull requests:

* Feature ideas
* Bug fixes
* IMDb matching improvements
* GUI version? Go ahead!

## 🙌 Credits

Developed by **Chathura Prasanga** with love for order and clean libraries.

IMDb data powered by [IMDbPY](https://imdbpy.readthedocs.io/en/latest/).

> "A well-organized movie folder is a happy movie night."

---

Licensed under MIT.
