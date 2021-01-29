import pytest
import logging


@pytest.fixture(scope='module', autouse=True)
def fixture_demo():
    logging.info("\nStarting test case...")
    yield
    logging.info("\nEnd test case")
