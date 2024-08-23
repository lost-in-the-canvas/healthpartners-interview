# custom_logger.py
import logging

class CustomHandler(logging.Handler):
    def __init__(self, log_file):
        super().__init__()
        self.file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        self.console_handler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setFormatter(self.formatter)

    def emit(self, record):
        self.console_handler.emit(record)
        self.file_handler.emit(record)

    def close(self):
        self.file_handler.close()
        self.console_handler.close()
