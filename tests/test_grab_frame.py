import pytest
import math

from autoscript_sdb_microscope_client.structures import (
    AdornedImage,
    GrabFrameSettings,
    Rectangle,
)


def test_simple(microscope):
    image = microscope.imaging.grab_frame()
    assert type(image) is AdornedImage


@pytest.mark.parametrize(
    "resolution, dwell_time",
    [("768x512", 1e-9), ("1536x1024", 1e-8), ("3072x2048", 1e-7), ("6072x4096", 1e-6)],
)
def test_with_settings(microscope, resolution: str, dwell_time: float):
    settings = GrabFrameSettings(
        resolution=resolution, dwell_time=dwell_time, bit_depth=8
    )
    image = microscope.imaging.grab_frame(settings)
    assert type(image) is AdornedImage
    width, height = tuple(map(int, resolution.split("x")))
    assert image.width == width
    assert image.height == height
    assert image.data.shape == (height, width)


@pytest.mark.parametrize(
    "resolution, rectangle",
    [
        ("768x512", Rectangle(0, 0, 0.5, 0.5)),
        ("1536x1024", Rectangle(0.5, 0.5, 0.5, 0.5)),
        ("3072x2048", Rectangle(0.5, 0, 0.5, 0.5)),
        ("6072x4096", Rectangle(0, 0.5, 0.5, 0.5)),
    ],
)
def test_reduced_area(microscope, resolution, rectangle):
    settings = GrabFrameSettings(resolution=resolution, reduced_area=rectangle)
    image = microscope.imaging.grab_frame(settings)
    assert type(image) is AdornedImage
    width, height = tuple(map(int, resolution.split("x")))
    width *= rectangle.width
    height *= rectangle.height
    assert image.width == width
    assert image.height == height
    assert image.data.shape == (height, width)
