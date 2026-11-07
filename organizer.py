
import os
import shutil
from pathlib import Path

EXTENSION_MAP = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".pptx": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",

    ".mp4": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",

    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".json": "Code",
}

def unique_destination(folder, filename):
    destination = folder / filename
    counter = 1

    while destination.exists():
        destination = folder / (
            f"{Path(filename).stem}_{counter}"
            f"{Path(filename).suffix}"
        )
        counter += 1

    return destination


def organize_files(folder_path, dry_run=True):
    folder = Path(folder_path).expanduser().resolve()

    if not folder.is_dir():
        print("Error: Folder does not exist.")
        return

    moved = 0
    skipped = 0
    errors = 0
    category_counts = {}

    print("\n========== FILE ORGANIZER ==========")
    print(f"Target folder: {folder}")
    print(f"Mode: {'PREVIEW' if dry_run else 'MOVE'}")
    print("====================================")

    try:
        with os.scandir(folder) as entries:
            files = [entry for entry in entries
                     if entry.is_file(follow_symlinks=False)]
    except (PermissionError, OSError) as error:
        print(f"Cannot scan folder: {error}")
        return

    for entry in files:
        source = Path(entry.path)

        # Never move the running script itself.
        if source == Path(__file__).resolve():
            skipped += 1
            continue

        category = EXTENSION_MAP.get(
            source.suffix.lower(), "Others"
        )
        target_folder = folder / category

        try:
            destination = unique_destination(
                target_folder, source.name
            )

            if dry_run:
                print(f"[PREVIEW] {source.name} -> "
                      f"{category}/{destination.name}")
            else:
                target_folder.mkdir(
                    parents=True, exist_ok=True
                )

                # Recheck to reduce filename collisions.
                destination = unique_destination(
                    target_folder, source.name
                )

                shutil.move(str(source), str(destination))
                print(f"[MOVED] {source.name} -> "
                      f"{category}/{destination.name}")

            moved += 1
            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

        except (PermissionError, FileExistsError, OSError) as error:
            errors += 1
            print(f"[ERROR] {source.name}: {error}")

    print("\n========== EXECUTION SUMMARY ==========")
    print(f"Files {'previewed' if dry_run else 'moved'}: {moved}")
    print(f"Files skipped: {skipped}")
    print(f"Errors: {errors}")

    for category, count in sorted(category_counts.items()):
        print(f"{category}: {count}")

    print("=======================================")


def main():
    print("AUTOMATED FILE ORGANIZER & CLEANUP UTILITY")

    folder_path = input(
        "\nEnter folder path to organize: "
    ).strip().strip('"')

    if not folder_path:
        print("Error: Please provide a folder path.")
        return

    print("\n1. Preview changes (recommended)")
    print("2. Organize files")

    choice = input("Select option (1/2): ").strip()

    if choice == "1":
        organize_files(folder_path, dry_run=True)
    elif choice == "2":
        confirm = input(
            "Files will be moved. Type YES to continue: "
        ).strip()

        if confirm == "YES":
            organize_files(folder_path, dry_run=False)
        else:
            print("Operation cancelled.")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
