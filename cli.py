import argparse
import logging
import os
import time
from watchdog.observers import Observer
from main import ImageOptimizerHandler

def start_monitoring(watch_folder, optimized_folder, max_width, quality):
    """Starts the image optimization monitoring process."""
    os.makedirs(optimized_folder, exist_ok=True)
    
    logging.info(f"Starting folder monitoring: {watch_folder}")
    event_handler = ImageOptimizerHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping folder monitoring due to keyboard interrupt.")
        observer.stop()
    observer.join()

def main():
    parser = argparse.ArgumentParser(description="Image Optimizer CLI")
    parser.add_argument("--watch_folder", type=str, default="./watch_folder", help="Folder to watch for new images")
    parser.add_argument("--optimized_folder", type=str, default="./optimized_folder", help="Folder to save optimized images")
    parser.add_argument("--max_width", type=int, default=800, help="Maximum width of optimized images")
    parser.add_argument("--quality", type=int, default=70, help="JPEG quality of optimized images")
    
    args = parser.parse_args()
    

    start_monitoring(args.watch_folder, args.optimized_folder, args.max_width, args.quality)
    
if __name__ == "__main__":
    main()
