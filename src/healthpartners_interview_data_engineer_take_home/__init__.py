# src/cms_downloader/__init__.py

from .download import *

def main():
    print("Starting CMS data download and processing...")
    datasets = download_datasets(theme="Hospitals")
    print("Completed CMS data download and processing.")

def hello() -> str:
    return "Hello from healthpartners-interview-data-engineer-take-home!"
