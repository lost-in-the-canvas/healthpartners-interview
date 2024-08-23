import logging
import requests
from pydantic_models.models import Dataset, ValidationError

API_URL = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

log = logging.getLogger(__name__)

def fetch_datasets():
    """Fetch datasets and then return a validated JSON response."""
    try:
        log.info("🏗️ Fetching datasets...")
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        datasets = []
        for item in data:
            try:
                dataset = Dataset(**item)
                datasets.append(dataset)
            except ValidationError as e:
                log.error("Validation error for dataset: %s", item.get('title', 'Unknown title'), exc_info=e)
        log.info('✅ Finished fetching datasets.')
        return datasets
    except Exception as e:
        log.error("Failed to fetch datasets", exc_info=e)
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
        log.error("Failed to download datasets", exc_info=e)
        return []
