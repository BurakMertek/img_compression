import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from configuration import *

os.makedirs(OPTIMIZED_FOLDER, exist_ok=True)

class ImageOptimizerHandler (FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".jpeg", ".png", ".jpg"):
            self.optimize_event(event.src_path)

    def optimize_event(self, file_path):
        try:
            with Image.open(file_path) as img:
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_size = (MAX_WIDTH,  int(img.height*ratio))
                    img = img.resize(new_size, Image.ANTIALIAS)
                
                optimized_path = os.path.join(OPTIMIZED_FOLDER, os.path.basename(file_path))

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    temp_path = optimized_path.rsplit(".",1)[0] + ".jpg"

                img.save(optimized_path, "JPEG", quality=QUALITY)
                optimized_size = os.path.getsize(temp_path)

                print(f"Optimized: {file_path}=>{optimized_path}")

               # if optimized_size< original_size:


        except Exception as e:
            print(f"error processing {file_path}: {e}")



if __name__ == "__main__":
    event_handler= ImageOptimizerHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive= False)
    observer.start()
    print(f"monitoring folder: {WATCH_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



