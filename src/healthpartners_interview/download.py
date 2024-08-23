import logging
import sys

import requests
import ijson
import gzip

from src.healthpartners_interview.decorators.profiling import profile_function
from src.healthpartners_interview.pydantic_models.models import Dataset, ValidationError

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

def validate_and_append_dataset(dataset_obj, datasets):
    """Validate a dataset object and append it to the datasets list if valid."""
    try:
        dataset = Dataset(**dataset_obj)
        datasets.append(dataset)
        logging.info("Validated dataset: %s", dataset.title)
    except ValidationError as e:
        logging.error("Validation error for dataset: %s", dataset_obj.get('title', 'Unknown title'), exc_info=e)
        sys.exit(1)

def fetch_datasets():
    """Fetch datasets and then return a validated JSON response."""
    try:
        logging.info("🏗️ Fetching datasets...")
        response = requests.get(API_URL, stream=True)
        response.raise_for_status()

        datasets  = []

        for dataset_obj in parse_json(response.text):
            validate_and_append_dataset(dataset_obj, datasets)

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
        return datasets
    except Exception as e:
        logging.error("Failed to download datasets", exc_info=e)
        return []
