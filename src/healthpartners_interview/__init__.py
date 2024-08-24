import logging
from datetime import datetime

from datetime import timedelta
from src.healthpartners_interview.download_datasets import fetch_datasets
from src.healthpartners_interview.last_run_logger import setup_database, get_last_run_time, log_current_time
from healthpartners_interview.process_datasets import process_all_csv_files

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(r'.\logs\pytest.log', mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main() -> int:
    logging.info("Starting CMS data download and processing...")
    setup_database()
    last_run_time = get_last_run_time()

    # Log the last run time, current time, and the difference
    logging.debug("Last run time: %s", last_run_time)
    logging.debug("Current time: %s", datetime.now())
    logging.debug("Difference: %s", datetime.now() - last_run_time)

    if last_run_time and datetime.now() - last_run_time < timedelta(hours=24):
        logging.info("Fetch datasets skipped. Last run was less than 24 hours ago.")
        return 0

    fetch_datasets(last_run_time=last_run_time)
    process_all_csv_files()
    logging.info("Completed CMS data download and processing.")
    return 0

if __name__ == "__main__":
    main()
