import logging
from typing import List, Optional

import requests
from pydantic import BaseModel, EmailStr, Field, ValidationError

API_URL = 'https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Pydantic models
class ContactPoint(BaseModel):
    type: str = Field(..., alias='@type')
    fn: str
    hasEmail: Optional[str] = EmailStr


class Publisher(BaseModel):
    type: str = Field(..., alias='@type')
    name: str


class DistributionItem(BaseModel):
    type: str = Field(..., alias='@type')
    downloadURL: str
    mediaType: str


class Dataset(BaseModel):
    accessLevel: str
    landingPage: str
    bureauCode: List[str]
    issued: str
    type: str = Field(..., alias='@type')
    modified: str
    released: str
    keyword: List[str]
    contactPoint: ContactPoint
    publisher: Publisher
    identifier: str
    description: str
    title: str
    programCode: List[str]
    distribution: List[DistributionItem]
    theme: List[str]

def fetch_datasets():
    """Fetch datasets and then return a validated JSON response."""
    try:
        logger.info("🏗️ Fetching datasets...")
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        datasets = []
        for item in data:
            try:
                dataset = Dataset(**item)
                datasets.append(dataset)
            except ValidationError as e:
                logger.error(f"Validation error for dataset: {item.get('title', 'Unknown title')}")
                logger.error(f"Error details: {e}")
                # You can add more detailed error logging here if needed
        logger.info('✅ Finished fetching datasets.')
        return datasets
    except Exception as e:
        logger.error(f"Failed to fetch datasets: {e}")
        return None

def download_datasets(theme="Hospitals"):
    """Download datasets based on a specified theme."""
    try:
        datasets = fetch_datasets()
        if datasets is None:
            return []

        # try:
        #     theme_datasets = [ds for ds in datasets if theme.lower() in ds['theme'].lower()]
        #
        #     os.makedirs('data', exist_ok=True)
        #     with ThreadPoolExecutor() as executor:
        #         for dataset in theme_datasets:
        #             executor.submit(download_file, dataset['download_url'], f"data/{dataset['title']}.csv")
        #
        #     return theme_datasets
        # except Exception as e:
        #     logger.error(f"Error processing datasets: {e}")
        #     return []
        return []
    except Exception as e:
        logger.error(f"Failed to download datasets: {e}")
        return []