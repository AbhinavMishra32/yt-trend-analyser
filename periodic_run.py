import os
import datetime
import logging

# Global constants
LOG_FILE = "youtube_data.log"
LAST_RUN_TIME_FILE = "last_run_time.txt"
FETCH_INTERVAL_HOURS = 24

def setup_logging():
    """Set up logging configuration."""
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Log to file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def get_last_run_time():
    """Retrieve the last run time from a file."""
    try:
        with open(LAST_RUN_TIME_FILE, "r") as file:
            last_run_time_str = file.read()
            last_run_time = datetime.datetime.strptime(last_run_time_str, "%Y-%m-%d %H:%M:%S")
            return last_run_time
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error("Error occurred while retrieving last run time: %s", str(e))
        return None

def save_last_run_time():
    """Save the current time as the last run time."""
    try:
        current_time = datetime.datetime.now()
        with open(LAST_RUN_TIME_FILE, "w") as file:
            file.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        logger.error("Error occurred while saving last run time: %s", str(e))

def is_interval_elapsed(last_run_time, interval_hours):
    """Check if the specified interval has passed since the last run."""
    if last_run_time is None:
        return True
    current_time = datetime.datetime.now()
    time_difference = current_time - last_run_time
    return time_difference.total_seconds() >= (interval_hours * 3600)

if __name__ == "__main__":
    logger = setup_logging()
    last_run_time = get_last_run_time()
    
    if is_interval_elapsed(last_run_time, FETCH_INTERVAL_HOURS):
        logger.info("Interval has elapsed. Fetching YouTube data...")
        # Run your main script here
        # For example:
        os.system("python3 r10.py")
        save_last_run_time()
    else:
        logger.info("Interval has not elapsed since the last run. Skipping data fetching.")
