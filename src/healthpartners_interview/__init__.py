import logging
import sys
from socket import fromfd
from datetime import datetime, timedelta
from src.healthpartners_interview.download import download_datasets, get_last_run_time

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('./logs/pytest.log', mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main() -> int:
    logging.info("Starting CMS data download and processing...")
    last_run_time = get_last_run_time()
    if last_run_time and datetime.now() - last_run_time < timedelta(hours=24):
        logging.debug("Last run time: %s", last_run_time)
        logging.debug("Current time: %s", datetime.now())
        logging.debug("Difference: %s", datetime.now() - last_run_time)
        logging.info("Fetch datasets skipped. Last run was less than 24 hours ago.")
        return 0
    datasets = download_datasets(theme="Hospitals")
    logging.info("Completed CMS data download and processing.")
    return 0

if __name__ == "__main__":
    main()
