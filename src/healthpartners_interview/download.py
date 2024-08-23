import logging
import os

import requests
import pyinstrument
from pyinstrument import Profiler
from src.healthpartners_interview.pydantic_models.models import Dataset, ValidationError

API_URL = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'

def fetch_datasets():
    """Fetch datasets and then return a validated JSON response."""
    try:
        logging.info("🏗️ Fetching datasets...")
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        datasets = []
        for item in data:
            try:
                dataset = Dataset(**item)
                datasets.append(dataset)
                # Log validated dataset and continue to the next dataset
                logging.info("Validated dataset: %s", dataset.title)
            except ValidationError as e:
                # Log validation error and continue to the next dataset
                logging.error("Validation error for dataset: %s", item.get('title', 'Unknown title'), exc_info=e)
        logging.info('✅ Finished fetching datasets.')
        return datasets
    except Exception as e:
        logging.error("Failed to fetch datasets", exc_info=e)
        return None

def download_datasets(theme="Hospitals"):
    """Download datasets based on a specified theme."""
    try:
        with Profiler() as profiler:
            # Call the fetch_datasets function
            datasets = fetch_datasets()

        # Ensure the performance_profiles directory exists
        os.makedirs("./performance_profiles", exist_ok=True)

        # Write the profiler output to a Speedscope file
        with open("./performance_profiles/profiler_output_fetch_datasets_fn.speedscope.json", "w") as f:
            f.write(profiler.output(pyinstrument.renderers.SpeedscopeRenderer(show_all=True, timeline=True, processor_options={'show_native': True})))

        # Write the profiler output to an HTML file
        with open("./performance_profiles/profiler_output_fetch_datasets_fn.html", "w") as f:
            f.write(profiler.output_html())

        # Your existing code for downloading datasets goes here
        return []
    except Exception as e:
        logging.error("Failed to download datasets", exc_info=e)
        return []
