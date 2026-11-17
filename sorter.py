import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TARGET_DIR = "/Users/alim/Downloads"  # Укажите вашу папку

EXTENSIONS_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".json"],
    "Media": [".mp4", ".mov", ".mp3", ".wav"],
}

def move_file(file_path):
    time.sleep(1)
    
    if not os.path.exists(file_path):
        return

    if os.path.isdir(file_path):
        return

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if not ext:
        return

    target_folder = None
    for category, exts in EXTENSIONS_MAP.items():
        if ext in exts:
            target_folder = category
            break

    if target_folder:
        folder_path = os.path.join(TARGET_DIR, target_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name = os.path.basename(file_path)
        destination_path = os.path.join(folder_path, file_name)

        try:
            shutil.move(file_path, destination_path)
            print(f"[Moved] {file_name} -> {target_folder}/")
        except Exception as e:
            print(f"Ошибка при перемещении {file_name}: {e}")

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            move_file(event.src_path)

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR):
        print(f"Ошибка: папка {TARGET_DIR} не найдена.")
        exit(1)

    print(f"Запущен фоновый мониторинг папки: {TARGET_DIR}")
    print("Для остановки нажмите Ctrl + C\n")

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=TARGET_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nМониторинг остановлен.")
    
    observer.join()