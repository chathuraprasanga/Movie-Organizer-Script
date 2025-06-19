import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List
from imdb import IMDb

ia = IMDb()

ROOT_DIR = Path(os.path.expanduser("~/Downloads/Videos"))
VIDEO_EXTS = ['.mp4', '.mkv', '.avi', '.mov']
SUB_EXTS = ['.srt', '.sub', '.idx']
FOLDER_ICON = "📁"
MOVIE_ICON = "🎮"
SUB_ICON = "🗘️"
MERGED_ICON = "📦"

moved_file_count = 0
renamed_folder_count = 0

def extract_name_and_year(name):
    name = name.replace('.', ' ').replace('-', ' ')
    match = re.search(r"(.+?)\s*\(?([12][09][0-9]{2})\)?", name)
    if match:
        return match.group(1).strip(), match.group(2)
    return None, None

def fetch_year_from_imdb(title: str):
    try:
        results = ia.search_movie(title)
        if results:
            movie = results[0]
            ia.update(movie)
            return str(movie.get('year', ''))
    except Exception as e:
        print(f"IMDb error for '{title}': {e}")
    return None

def group_loose_files_into_folders():
    global moved_file_count
    for f in list(ROOT_DIR.iterdir()):
        if f.is_file() and f.suffix.lower() in VIDEO_EXTS + SUB_EXTS:
            title, year = extract_name_and_year(f.stem)
            if not year:
                title = f.stem.replace('.', ' ').replace('-', ' ')
                year = fetch_year_from_imdb(title)
                if not year:
                    manual = input(f"Enter year for '{f.name}' (or press Enter to skip): ")
                    if manual.strip().isdigit():
                        year = manual.strip()
                    else:
                        continue
            folder_name = f"{title.strip()} ({year})"
            target_folder = ROOT_DIR / folder_name
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(f), target_folder / f.name)
            print(f"[moved]    -> {f.name} → {target_folder.name}/")
            moved_file_count += 1

def list_duplicates():
    seen = {}
    duplicates = []
    for folder in ROOT_DIR.iterdir():
        if folder.is_dir():
            name, year = extract_name_and_year(folder.name)
            if name and year:
                key = f"{name} ({year})"
                if key in seen:
                    duplicates.append((seen[key], folder, key))
                else:
                    seen[key] = folder
    return duplicates

def get_related_files(folder: Path, base: str) -> List[Path]:
    base = base.lower()
    return [f for f in folder.iterdir() if f.is_file() and base in f.stem.lower()]

def move_all_media_to_folder(folder1: Path, folder2: Path):
    global moved_file_count
    for f in folder2.iterdir():
        if f.is_file() and f.suffix.lower() in VIDEO_EXTS + SUB_EXTS:
            shutil.move(str(f), folder1 / f.name)
            moved_file_count += 1
    try:
        folder2.rmdir()
    except:
        pass

def choose_video_file(files: List[Path]) -> Path:
    folder = files[0].parent
    if os.name == 'nt':
        os.startfile(str(folder))
    elif os.name == 'posix':
        subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', str(folder)])

    print("\nFound multiple video files:")
    for i, f in enumerate(files, 1):
        print(f"[{i}] {MOVIE_ICON} {f.name}")
    choice = input("Choose the number to keep, or type 'new' to split a movie: ").strip()
    if choice.lower() == 'new':
        title = input("Enter the name of the movie you want to move: ").strip()
        year = fetch_year_from_imdb(title)
        if not year:
            year = input(f"Could not find year for '{title}'. Enter manually: ").strip()
        new_folder = ROOT_DIR / f"{title} ({year})"
        new_folder.mkdir(exist_ok=True)

        print("Select file to move into the new folder:")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {MOVIE_ICON} {f.name}")
        file_idx = input("Enter number: ").strip()
        try:
            file_to_move = files[int(file_idx) - 1]
            shutil.move(str(file_to_move), new_folder / file_to_move.name)
            print(f"[moved]    → {file_to_move.name} → {new_folder.name}/")
            renamed = new_folder / f"{new_folder.name}{file_to_move.suffix}"
            (new_folder / file_to_move.name).rename(renamed)
            print(f"[renamed]  -> {MOVIE_ICON} {file_to_move.name} → {renamed.name}")
        except:
            print("Invalid choice. Skipping.")
        return None
    try:
        idx = int(choice) - 1
        return files[idx]
    except:
        print("Invalid choice. Skipping...")
        return files[0]

def rename_all_files_in_folder(folder: Path):
    base_name = folder.name
    for f in folder.iterdir():
        if f.suffix.lower() in VIDEO_EXTS:
            new_name = f"{base_name}{f.suffix}"
            if f.name != new_name:
                f.rename(folder / new_name)
                print(f"[renamed]  -> {MOVIE_ICON} {f.name} → {new_name}")
        elif f.suffix.lower() in SUB_EXTS:
            new_name = f"{base_name}{f.suffix}"
            if f.name != new_name:
                f.rename(folder / new_name)
                print(f"[renamed]  -> {SUB_ICON} {f.name} → {new_name}")

def rename_and_cleanup(folder: Path, keep_file: Path):
    base_name = folder.name
    for f in folder.iterdir():
        if f == keep_file:
            new_name = f"{base_name}{f.suffix}"
            new_path = folder / new_name
            if f.name != new_name:
                f.rename(new_path)
                print(f"[renamed]  -> {MOVIE_ICON} {f.name} → {new_name}")
        elif f.suffix.lower() in SUB_EXTS:
            new_name = f"{base_name}{f.suffix}"
            new_path = folder / new_name
            if f.name != new_name:
                f.rename(new_path)
                print(f"[renamed]  -> {SUB_ICON} {f.name} → {new_name}")
        elif f.suffix.lower() in VIDEO_EXTS and f != keep_file:
            f.unlink()
        else:
            new_name = f"{base_name}{f.suffix}"
            new_path = folder / new_name
            if f.name != new_name:
                f.rename(new_path)

def rename_existing_folders():
    global renamed_folder_count
    for folder in ROOT_DIR.iterdir():
        if folder.is_dir():
            name, year = extract_name_and_year(folder.name)
            if not (name and year):
                clean_name = folder.name.replace('.', ' ').replace('-', ' ')
                guessed_year = fetch_year_from_imdb(clean_name)
                if guessed_year:
                    year = guessed_year
                    name = clean_name
                else:
                    ans = input(f"Cannot detect year for '{folder.name}'. Enter manually or press Enter to skip: ")
                    if ans.strip() == "":
                        continue
                    year = ans.strip()
                    name = clean_name

            new_name = f"{name} ({year})"
            new_path = ROOT_DIR / new_name
            if new_path != folder:
                if new_path.exists():
                    for f in folder.iterdir():
                        shutil.move(str(f), new_path / f.name)
                    shutil.rmtree(folder)
                    print(f"[merged]   -> {FOLDER_ICON} {folder.name} → {new_path.name}")
                else:
                    folder.rename(new_path)
                    print(f"[renamed]  -> {FOLDER_ICON} {folder.name} → {new_path.name}")
                    renamed_folder_count += 1

def handle_folder_merges():
    merged_count = 0
    duplicates = list_duplicates()
    for folder1, folder2, title in duplicates:
        move_all_media_to_folder(folder1, folder2)
        all_videos = [f for f in folder1.iterdir() if f.suffix.lower() in VIDEO_EXTS]
        if not all_videos:
            continue
        keep_file = choose_video_file(all_videos)
        if keep_file:
            rename_and_cleanup(folder1, keep_file)
        print(f"[merged]   -> {MERGED_ICON} {folder2.name} → {folder1.name}")
        merged_count += 1
    print(f"\n{MERGED_ICON} Merged {merged_count} duplicate folder(s).")

def resolve_multiple_videos_in_folder(folder: Path):
    videos = [f for f in folder.iterdir() if f.suffix.lower() in VIDEO_EXTS]
    if len(videos) <= 1:
        if videos:
            rename_and_cleanup(folder, videos[0])
        else:
            rename_all_files_in_folder(folder)
        return
    print(f"\n🎞️ Multiple video files detected in: {folder.name}")
    keep = choose_video_file(videos)
    if keep:
        rename_and_cleanup(folder, keep)

def handle_all_remaining_folders():
    for folder in ROOT_DIR.iterdir():
        if folder.is_dir():
            resolve_multiple_videos_in_folder(folder)

if __name__ == "__main__":
    group_loose_files_into_folders()
    rename_existing_folders()
    handle_folder_merges()
    handle_all_remaining_folders()
    print(f"\n📦 Total files moved: {moved_file_count}")
    print(f"🔁 Total folders renamed: {renamed_folder_count}")
