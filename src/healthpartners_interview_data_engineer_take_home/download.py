import logging
import requests
from pydantic_models.models import Dataset, ValidationError

API_URL = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'

# Set the logging level
logging.basicConfig(
    level=logging.INFO,  # Equivalent to log_cli_level = "INFO"
    format='%(pastime)s - %(levelness)s - %(message)s',  # Equivalent to log_cli_format
    datefmt='%Y-%m-%d %H:%M:%S',  # Equivalent to log_cli_date_format
    filename='./logs/pytest.log' # Equivalent to log_file
)

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
                # Log the valdiated dataset and continue to the next dataset
                logging.info("Validated dataset: %s", dataset.title)
            except ValidationError as e:
                # Log the validation error and continue to the next dataset
                logging.error("Validation error for dataset: %s", item.get('title', 'Unknown title'), exc_info=e)
        logging.info('✅ Finished fetching datasets.')
        return datasets
    except Exception as e:
        logging.error("Failed to fetch datasets", exc_info=e)
        return None

def download_datasets(theme="Hospitals"):
    """Download datasets based on a specified theme."""
    try:
        datasets = fetch_datasets()
        if datasets is None:
            return []

        # Your existing code for downloading datasets goes here
        return []
    except Exception as e:
        logging.error("Failed to download datasets", exc_info=e)
        return []
