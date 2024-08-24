import os
import pandas as pd
import logging
from itertools import chain
from string import ascii_letters, digits
from concurrent.futures import ProcessPoolExecutor

def process_single_csv(csv_file_path):
    """Process a single CSV file to ensure column headers are in snake_case."""
    logging.debug("Beginning Processing CSV: %s", csv_file_path)
    try:
        valid_char_set = set(ascii_letters + digits + "_")

        df = pd.read_csv(csv_file_path, low_memory=False)

        # Convert column names to snake_case and remove invalid characters
        column_mapping = {
            col: "".join(
                filter(lambda char: char in valid_char_set, col.lower().replace(" ", "_"))
            )
            for col in df.columns
        }

        # Rename the columns in the DataFrame
        df = df.rename(columns=column_mapping)

        # Check if data/transformed directory exists
        if not os.path.exists(r'.\data\transformed'):
            os.makedirs(r'.\data\transformed')
        transformed_file_path = os.path.join(r'.\data\transformed', os.path.basename(csv_file_path))
        df.to_csv(transformed_file_path, index=False)
        logging.info("Transformed CSV: %s", transformed_file_path)
    except Exception as e:
        logging.error("Failed to transform CSV: %s", transformed_file_path, exc_info=e)

def process_all_csv_files():
    """Process all CSV files in the data/downloads directory using multiprocessing."""
    downloads_dir = r'.\data\downloads'
    csv_files = [os.path.join(downloads_dir, file) for file in os.listdir(downloads_dir) if file.endswith('.csv')]

    with ProcessPoolExecutor() as executor:
        executor.map(process_single_csv, csv_files)