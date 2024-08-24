import logging
import sys

import ijson
import requests

from src.healthpartners_interview.download_themed_csv import download_hospital_csv_file
from src.healthpartners_interview.last_run_logger import log_current_time
from src.healthpartners_interview.pydantic_models.models import Dataset, ValidationError

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

API_URL = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'

def parse_json(json_content):
    parser = ijson.parse(json_content)
    top_level_array = False
    array_stack = 0
    top_level_object = False
    object_stack = 0
    for prefix, event, value in parser:
        if event == 'start_array':
            if not top_level_array:
                top_level_array = True
                continue
            else:
                array_stack += 1
        if event == 'start_map':
            if not top_level_object:
                top_level_object = True
                builder = ijson.ObjectBuilder()
            else:
                object_stack += 1
        if event == 'end_map':
            if not top_level_object:
                raise Exception('end_map without a top level object')
            else:
                if object_stack == 0:
                    top_level_object = False
                    yield builder.value
                else:
                    object_stack -= 1
        if event == 'end_array':
            if not top_level_array:
                raise Exception('end_array without a top level array')
            else:
                if array_stack == 0:
                    top_level_array = False
                else:
                    array_stack -= 1
        builder.event(event, value)

def dataset_modified_after_last_run(dataset_obj, last_run_time):
    """Check if the dataset has been modified after the last run time."""
    modified_date = dataset_obj.get('modified')
    if not modified_date:
        logging.warning("Dataset %s has no modified date", dataset_obj.get('title', 'Unknown title'))
        return False

    modified_date = datetime.fromisoformat(modified_date)
    if modified_date > last_run_time:
        logging.info("Dataset %s has been modified since last run", dataset_obj.get('title', 'Unknown title'))
        return True
    else:
        logging.info("Dataset %s has not been modified since last run", dataset_obj.get('title', 'Unknown title'))
        return False

def validate_and_append_dataset(dataset_obj, datasets):
    """Validate dataset object and append it to the dataset list if valid."""
    try:
        dataset = Dataset(**dataset_obj)
        datasets.append(dataset)
        logging.info("Validated dataset: %s", dataset.title)
    except ValidationError as e:
        logging.error("Validation error for dataset: %s", dataset_obj.get('title', 'Unknown title'), exc_info=e)
        sys.exit(1)

def fetch_datasets(last_run_time):
    """Fetch datasets and then return a validated JSON response."""
    try:
        logging.info("🏗️ Fetching datasets...")
        response = requests.get(API_URL, stream=True)
        response.raise_for_status()


        datasets  = []
        number_of_themed_datasets = 0

        with ThreadPoolExecutor() as executor:
            for dataset_obj in parse_json(response.text):
                validate_and_append_dataset(dataset_obj, datasets)
                # If the theme is specified, filter the datasets by the theme "Hospitals"
                if dataset_obj.get('theme') == ["Hospitals"]:
                    number_of_themed_datasets += 1
                    # if dataset_modified_after_last_run(dataset_obj, last_run_time):
                    executor.submit(download_hospital_csv_file, dataset_obj)

        # Log the amount themed datasets
        logging.info("Number of themed datasets: %d", number_of_themed_datasets)
        logging.info('✅ Finished fetching datasets.')
        return datasets
    except Exception as e:
        logging.error("Failed to fetch datasets", exc_info=e)
        return None
    finally:
        # Log the time of this current completed run
        log_current_time()
