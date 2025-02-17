import argparse
import logging
import os
import time
import json
from watchdog.observers import Observer
from main import ImageOptimizerHandler

with open("configuration.json", "r") as config_file:
    config = json.load(config_file)

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

def stop_monitoring():
    """Stops the monitoring process."""
    logging.info("Monitoring stopped.")
    exit(0)

def main():
    parser = argparse.ArgumentParser(description="Image Optimizer CLI")
    parser.add_argument("--watch_folder", type=str, default=config["WATCH_FOLDER"], help="Folder to watch for new images")
    parser.add_argument("--optimized_folder", type=str, default=config["OPTIMIZED_FOLDER"], help="Folder to save optimized images")
    parser.add_argument("--max_width", type=int, default=config["MAX_WIDTH"], help="Maximum width of optimized images")
    parser.add_argument("--quality", type=int, default=config["QUALITY"], help="JPEG quality of optimized images")
    parser.add_argument("--stop", action="store_true", help="Stop monitoring")

    args = parser.parse_args()
    
    if args.stop:
        stop_monitoring()
    else:
        start_monitoring(args.watch_folder, args.optimized_folder, args.max_width, args.quality)

if __name__ == "__main__":
    main()
