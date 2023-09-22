import pytest

from autoscript_mock_microscope import MockSdbMicroscopeClient


@pytest.fixture
def microscope() -> MockSdbMicroscopeClient:
    microscope = MockSdbMicroscopeClient()
    microscope.connect()
    return microscope
