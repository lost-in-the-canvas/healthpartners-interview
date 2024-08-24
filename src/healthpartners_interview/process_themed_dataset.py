import logging
from datetime import datetime

import pandas as pd
import requests


def process_hospital_dataset(dataset_obj, last_run_time):
    """Process a hospital-themed dataset."""
    try:
        download_url = dataset_obj['distribution'][0]['downloadURL']
        csv_file_path = download_csv(download_url, dataset_obj['title'])
        # process_csv(csv_file_path)
    except Exception as e:
        logging.error("Failed to process dataset: %s", dataset_obj['title'], exc_info=e)


def download_csv(url, title):
    """Download CSV file from the given URL."""

    # Sanitize the title to remove special characters
    title = title.replace(':', '').replace(' ', '_')

    # Download the CSV file
    response = requests.get(url)
    response.raise_for_status()
    csv_file_path = f"./data/downloads/{title}.csv"

    # Save the CSV file to the downloads directory
    with open(csv_file_path, 'wb') as file:
        file.write(response.content)
    logging.info("Downloaded CSV: %s", csv_file_path)
    return csv_file_path


def process_csv(csv_file_path):
    """Process the CSV file to ensure column headers in parallel."""
    df = pd.read_csv(csv_file_path, low_memory=False)
    # Add logic to rename/convert/ensure column headers
    # For example, renaming columns to a standard format:
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    df.to_csv(csv_file_path, index=False)
    logging.info("Processed CSV: %s", csv_file_path)
