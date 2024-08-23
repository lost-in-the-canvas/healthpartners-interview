import logging
from socket import fromfd

from src.healthpartners_interview.download import download_datasets

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

def main():
    logging.info("Starting CMS data download and processing...")
    datasets = download_datasets(theme="Hospitals")
    logging.info("Completed CMS data download and processing.")

if __name__ == "__main__":
    main()
