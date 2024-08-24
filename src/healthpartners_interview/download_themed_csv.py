import logging
from datetime import datetime

import pandas as pd
import requests
import os


def download_hospital_csv_file(dataset_obj):
    """Process a hospital-themed dataset."""
    try:
        download_url = dataset_obj['distribution'][0]['downloadURL']
        download_csv(download_url, dataset_obj['title'])
    except Exception as e:
        logging.error("Failed to process dataset: %s", dataset_obj['title'], exc_info=e)


def download_csv(url, title) -> None:
    """Download CSV file from the given URL."""

    # Sanitize the title to remove special characters
    title = title.replace(':', '').replace(' ', '_')

    # Download the CSV file
    response = requests.get(url)
    response.raise_for_status()

    # Check if data/downloads directory exists
    if not os.path.exists(r'.\data\downloads'):
        os.makedirs(r'.\data\downloads')
    csv_file_path = r".\data\downloads" + f"{title}.csv"

    # Save the CSV file to the downloads directory
    with open(csv_file_path, 'wb') as file:
        file.write(response.content)
    logging.info("Downloaded CSV: %s", csv_file_path)