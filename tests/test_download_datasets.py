import logging
import pytest
import subprocess
import os
from pyinstrument import Profiler
from pyinstrument.renderers import SpeedscopeRenderer

from healthpartners_interview_data_engineer_take_home import *

# Set the logging level
logging.basicConfig(
    level=logging.INFO,  # Equivalent to log_cli_level = "INFO"
    format='%(pastime)s - %(levelness)s - %(message)s',  # Equivalent to log_cli_format
    datefmt='%Y-%m-%d %H:%M:%S',  # Equivalent to log_cli_date_format
    filename='./logs/pytest.log' # Equivalent to log_file
)

with Profiler() as profiler:
    def test_download_datasets(caplog):
        with caplog.at_level(logging.INFO):
            # Print the current working directory
            print("\nCurrent Working Directory:", os.getcwd())

            profiler = Profiler()
            profiler.start()
            datasets = download_datasets(theme="Hospitals")
            assert "Fetching" in caplog.text
            # assert len(datasets) > 0  # Ensure some datasets were downloaded.
            # Stop profiling.
            profiler.stop()

            # Print a simple console output
            print("\nProfiling Results (Console Output):")
            print(profiler.output_text(unicode=True, color=True))

            # Save results in Speedscope format

            # Create the directory if it doesn't exist
            if not os.path.exists('./performance_profiles'):
                os.makedirs('./performance_profiles')
            with open('./performance_profiles/performance_profiles.speedscope.json', 'w') as f:
                # First write to the JSON to a file
                logging.info("#1 | Saving Speedscope JSON to './performance_profiles/performance_profiles.speedscope.json'")
                f.write(profiler.output(renderer=SpeedscopeRenderer()))
            print("\nSpeedscope JSON saved to './performance_profiles/performance_profiles.speedscope.json'")

# Create the directory if it doesn't exist
if not os.path.exists('./performance_profiles'):
    os.makedirs('./performance_profiles')
with open('./performance_profiles/performance_profiles.speedscope.json', 'w') as f:
    logging.info("#2 | Saving Speedscope JSON to './performance_profiles/performance_profiles.speedscope.json'")
    f.write(profiler.output_text(SpeedscopeRenderer()))

