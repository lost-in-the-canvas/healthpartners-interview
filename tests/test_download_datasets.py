import os
import logging
from pyinstrument import Profiler
from pyinstrument.renderers import SpeedscopeRenderer
from healthpartners_interview_data_engineering_take_home_project import download_datasets
from healthpartners_interview_data_engineering_take_home_project.custom_logger import CustomHandler

# Set up logging
log_file_path = './logs/pytest.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Add the custom handler
custom_handler = CustomHandler(log_file_path)
logger.addHandler(custom_handler)

with Profiler() as profiler:
    def test_download_datasets(caplog):
        with caplog.at_level(logging.DEBUG):
            logging.debug("Debug test")

            profiler.start()
            datasets = download_datasets(theme="Hospitals")
            assert "Fetching" in caplog.text
            profiler.stop()

            print("\nProfiling Results (Console Output):")
            print(profiler.output_text(unicode=True, color=True))

            # Create the directory if it doesn't exist
            if not os.path.exists('./performance_profiles'):
                os.makedirs('./performance_profiles')
            with open('./performance_profiles/performance_profiles.speedscope.json', 'w') as f:
                logging.info("#1 | Saving Speedscope JSON to './performance_profiles/performance_profiles.speedscope.json'")
                f.write(profiler.output(renderer=SpeedscopeRenderer()))
            print("\nSpeedscope JSON saved to './performance_profiles/performance_profiles.speedscope.json'")
