
import os
import shutil
from pathlib import Path

# Find Organizer_Test beside this Python file
PROJECT_FOLDER = Path(__file__).resolve().parent
TARGET_FOLDER = PROJECT_FOLDER / "Organizer_Test"

EXTENSION_MAP = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
}

moved_count = 0
skipped_count = 0
error_count = 0

if not TARGET_FOLDER.is_dir():
    print(f"Test folder not found: {TARGET_FOLDER}")
else:
    print("=" * 45)
    print("       DESKTOP FILE ORGANIZER")
    print("=" * 45)
    print(f"Target folder: {TARGET_FOLDER}\n")

    files = list(os.scandir(TARGET_FOLDER))

    for entry in files:
        if not entry.is_file():
            continue

        source = Path(entry.path)
        category = EXTENSION_MAP.get(source.suffix.lower())

        if category is None:
            print(f"Skipped (unknown type): {source.name}")
            skipped_count += 1
            continue

        destination_folder = TARGET_FOLDER / category

        try:
            destination_folder.mkdir(exist_ok=True)
            destination = destination_folder / source.name

            if destination.exists():
                print(f"Skipped (name already exists): {source.name}")
                skipped_count += 1
                continue

            shutil.move(str(source), str(destination))
            print(f"Moved: {source.name} -> {category}/")
            moved_count += 1

        except (PermissionError, FileExistsError, OSError) as error:
            print(f"Could not move {source.name}: {error}")
            error_count += 1

    print("\n" + "=" * 45)
    print("EXECUTION SUMMARY")
    print("=" * 45)
    print(f"Files relocated: {moved_count}")
    print(f"Files skipped:   {skipped_count}")
    print(f"Errors:          {error_count}")
    print("Organizer finished.")
