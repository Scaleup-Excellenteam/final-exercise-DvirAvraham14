import os
import time
import asyncio
import subprocess
import uuid
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()

UPLOAD_DIRECTORY = os.environ.get('UPLOAD_FOLDER')
OUTPUT_DIRECTORY = os.environ.get('OUTPUT_FOLDER')


class FileHandler(FileSystemEventHandler):
    async def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path.endswith(".pptx") and file_path.startswith("pending_"):
                await process_pending_file(file_path)

async def process_pending_file(file_path):
    """
    Processes a pending file by running the "main.py" script on it asynchronously.
    Updates the file prefix and status accordingly.
    """
    file_name = os.path.basename(file_path)
    file_name_parts = file_name.split("_")
    uid = file_name_parts[-1].split(".")[0]
    print(OUTPUT_DIRECTORY)
    output_path = f"{OUTPUT_DIRECTORY}/done_{uid}.json"

    try:
        process = await asyncio.create_subprocess_exec("python3", "main.py", file_path, output_path)
        await process.communicate()

        if os.path.exists(output_path):
            new_file_path = os.path.join(UPLOAD_DIRECTORY, "done_" + '_'.join(file_name_parts[1:]))
            os.rename(file_path, new_file_path)
        else:
            print("Output file does not exist for: " + file_path)
    except subprocess.CalledProcessError as e:
        print("Error processing file: " + e.output.decode("utf-8"))


async def check_pending_files():
    """
    Checks for pending files in the uploads directory and processes them.
    """
    for file_name in os.listdir(UPLOAD_DIRECTORY):
        if file_name.startswith("pending_") and file_name.endswith(".pptx"):
            file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
            await process_pending_file(file_path)

def create_folders_if_not_exists():
    if not os.path.exists(os.environ.get('UPLOAD_FOLDER')):
        os.mkdir(os.environ.get('UPLOAD_FOLDER'))
    if not os.path.exists(os.environ.get('OUTPUT_FOLDER')):
        os.mkdir(os.environ.get('OUTPUT_FOLDER'))


async def main():
    create_folders_if_not_exists()

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, UPLOAD_DIRECTORY, recursive=False)
    observer.start()

    try:
        while True:
            await check_pending_files()
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    asyncio.run(main())
