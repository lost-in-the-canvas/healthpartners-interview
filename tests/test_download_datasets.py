from healthpartners_interview_data_engineer_take_home import *

def test_download_datasets(caplog):
    with caplog.at_level(logging.INFO):
        datasets = download_datasets(theme="Hospitals")
        assert "Fetching datasets..." in caplog.text
        assert "ERROR" not in caplog.text
        # assert "Downloaded" in caplog.text
        # assert len(datasets) > 0  # Ensure some datasets were downloaded