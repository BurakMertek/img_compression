import os
import time
import logging
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

with open("config.json", "r") as config_file:
    config = json.load(config_file)

WATCH_FOLDER = config["WATCH_FOLDER"]
OPTIMIZED_FOLDER = config["OPTIMIZED_FOLDER"]
MAX_WIDTH = config["MAX_WIDTH"]
QUALITY = config["QUALITY"]


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
                original_size = os.path.getsize(file_path)
                logging.debug(f"Original size: {original_size} bytes")  
            
            
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_size = (MAX_WIDTH, int(img.height * ratio))
                    logging.debug(f"resizing image to: {new_size}")
                    img = img.resize(new_size, Image.ANTIALIAS)

            # Convert PNG to JPEG for better compression
                optimized_path = os.path.join(OPTIMIZED_FOLDER, os.path.basename(file_path))
                temp_path = optimized_path + "_temp.jpg"  

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    logging.debug(f"converted image to RGB mode")

            
                img.save(temp_path, "JPEG", quality=QUALITY)

                optimized_size = os.path.getsize(temp_path)
                loggin.debug(f"optimized size: {optimized_size} bytes")

            
                if optimized_size < original_size:
                    os.rename(temp_path, optimized_path)
                    logging.info(f"Optimized and saved: {file_path} -> {optimized_path} (Reduced size: {original_size} -> {optimized_size} bytes)")
                else:
                    os.remove(temp_path)
                    logging.info(f"Skipped optimization for {file_path} (Optimized file was larger)")

        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")

    logging.basicConfig(
        filename = "image_optimizer.log",
        level=logging.DEBUG,
        format="%(asctime)s-%(levelname)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info(f"Optimized: {file_path} -> {optimized_path} (Reduced size: {original_size} -> {optimized_size} bytes)")


if __name__ == "__main__":

    logging.info(f"starting folder monitoring: {WATCH_FOLDER}")
    event_handler= ImageOptimizerHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive= False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info(f"stopping folder monitoring due to keyboard interrupt.")
        observer.stop()
    observer.join()



