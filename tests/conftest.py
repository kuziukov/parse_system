import logging

import pytest as pytest
from src.config import Config, get_config

log = logging.getLogger(__name__)


@pytest.fixture
def config() -> Config:
    config = get_config()
    return config
