import logging
import sys

import requests
import ijson
import gzip

from src.healthpartners_interview.decorators.profiling import profile_function
from src.healthpartners_interview.pydantic_models.models import Dataset, ValidationError

API_URL = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'

def fetch_datasets():
    """Fetch datasets and then return a validated JSON response."""
    try:
        logging.info("🏗️ Fetching datasets...")
        response = requests.get(API_URL, stream=True)
        response.raise_for_status()

        datasets = []
        parser = ijson.parse(response.text, multiple_values=True)

        current_item = {}
        for prefix, event, value in parser:
            if prefix == '' and event == 'start_array':
                continue
            elif prefix == '' and event == 'end_array':
                break
            elif event == 'start_map':
                current_item = {}
            elif event == 'end_map':
                try:
                    dataset = Dataset(**current_item)
                    datasets.append(dataset)
                    logging.info("Validated dataset: %s", dataset.title)

                    # Here you can perform any actions you want with the validated dataset
                    print(f"Processed dataset: {dataset.title}")

                # End the program if there is a validation error
                except ValidationError as e:
                    logging.error("Validation error for dataset: %s", current_item.get('title', 'Unknown title'), exc_info=e)
                    sys.exit(1)

                # Clear the current_item for the next dataset
                current_item = {}
            elif '.' not in prefix:  # This is a top-level key
                current_item[prefix] = value

        logging.info('✅ Finished fetching datasets.')
        return datasets
    except Exception as e:
        logging.error("Failed to fetch datasets", exc_info=e)
        return None


@profile_function()
def download_datasets(theme="Hospitals"):
    """Download datasets based on a specified theme."""
    try:
        datasets = fetch_datasets()

        # Your existing code for downloading datasets goes here
        return []
    except Exception as e:
        logging.error("Failed to download datasets", exc_info=e)
        return []
