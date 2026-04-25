from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path

TARGET_FILE_PATH = Path("signal.txt").absolute()
WATCH_DIR = TARGET_FILE_PATH.parent

class PostureUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("changed")
        print(Path(event.src_path) == TARGET_FILE_PATH)
        if not event.is_directory and Path(event.src_path) == TARGET_FILE_PATH:
            print("detect change in signal.txt, call_ai()")
            with open(TARGET_FILE_PATH, "r") as f:
                content = f.read()
                if content.split(":")[1].strip() == "ALARMING":
                    # send message to ai
                    query = 'My sitting pose is bad, please tell me to straight up my body!'
                    # call_ai(query)



if __name__ == "__main__":
    observer = Observer()
    handler = PostureUpdateHandler()
    observer.schedule(handler, WATCH_DIR, recursive=False)
    observer.start()

    while True:
        input("press enter to continue")