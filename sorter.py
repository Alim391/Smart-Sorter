import os
import shutil

TARGET_DIR = "/Users/alim/Downloads"

EXTENSIONS_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".json"],
    "Media": [".mp4", ".mov", ".mp3", ".wav"],
}

def sort_files():
    if not os.path.exists(TARGET_DIR):
        print(f"Ошибка: папка {TARGET_DIR} не найдена.")
        return

    items = os.listdir(TARGET_DIR)
    
    moved_count = 0

    for item in items:
        item_path = os.path.join(TARGET_DIR, item)

        if os.path.isdir(item_path):
            continue

        _, ext = os.path.splitext(item)
        ext = ext.lower()

        if not ext:
            continue

        target_folder = None
        for category, exts in EXTENSIONS_MAP.items():
            if ext in exts:
                target_folder = category
                break

        if target_folder:
            folder_path = os.path.join(TARGET_DIR, target_folder)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            destination_path = os.path.join(folder_path, item)
            
            shutil.move(item_path, destination_path)
            print(f"[Moved] {item} -> {target_folder}/")
            moved_count += 1

    print(f"\nСортировка завершена! Перемещено файлов: {moved_count}")

if __name__ == "__main__":
    sort_files()