from bedrock_bio.config import config
import pytest


@pytest.fixture(autouse=True)
def reset():
    config.reset()
    yield
    config.reset()
