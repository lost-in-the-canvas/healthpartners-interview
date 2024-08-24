import structlog
import pytest
import logging
from structlog.testing import LogCapture

# Fixture to configure structlog for testing
@pytest.fixture(autouse=True)
def fixture_configure_structlog(log_output):
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),  # For console transformed
            log_output
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,  # Disable caching for tests
    )

# Fixture to capture log transformed
@pytest.fixture
def log_output():
    return LogCapture()

# Function to be tested
def do_something():
    logger = structlog.get_logger()
    logger.info("Starting operation")
    result = 42
    logger.info("Operation completed", result=result)
    return result

# Test function
def test_do_something(log_output):
    result = do_something()

    assert result == 42
    assert len(log_output.entries) == 2

    assert log_output.entries[0]["event"] == "Starting operation"
    assert log_output.entries[0]["log_level"] == "info"

    assert log_output.entries[1]["event"] == "Operation completed"
    assert log_output.entries[1]["log_level"] == "info"
    assert log_output.entries[1]["result"] == 42

if __name__ == "__main__":
    pytest.main([__file__])
