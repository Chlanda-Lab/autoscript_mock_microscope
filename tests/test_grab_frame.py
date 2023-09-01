import pytest
import math

from autoscript_sdb_microscope_client.structures import AdornedImage, GrabFrameSettings


def test_simple(microscope):
    image = microscope.imaging.grab_frame()
    assert type(image) is AdornedImage



@pytest.mark.parametrize("resolution, dwell_time", [
    ('768x512', 1e-9),
    ('1536x1024', 1e-8),
    ('3072x2048', 1e-7),
    ('6072x4096', 1e-6)])
def test_with_settings(microscope, resolution: str, dwell_time: float):
    settings = GrabFrameSettings(resolution=resolution, dwell_time=dwell_time, bit_depth=8)
    image = microscope.imaging.grab_frame(settings)
    assert type(image) is AdornedImage
    width, height = tuple(map(int, resolution.split('x')))
    assert image.width == width
    assert image.height == height
    assert image.data.shape == (height, width)


def test_reduced_area(microscope):
    pass