import pytest
import math
from configparser import ConfigParser

from autoscript_sdb_microscope_client.structures import (
    AdornedImage,
    GrabFrameSettings,
    Rectangle,
)

def assert_consistent_pix_size(image: AdornedImage):
    config = ConfigParser()
    config.read_string(image.metadata.metadata_as_ini)
    meta_hfw = float(config['EBeam']['HFW'])
    meta_vfw = float(config['EBeam']['VFW'])
    meta_pix_width = float(config['Scan']['PixelWidth'])
    meta_pix_height = float(config['Scan']['PixelHeight'])
    assert math.isclose(meta_vfw, meta_hfw * image.height / image.width)
    assert math.isclose(meta_hfw, meta_pix_width * image.width)
    assert math.isclose(meta_vfw, meta_pix_height * image.height)



def test_simple(microscope):
    image = microscope.imaging.grab_frame()
    assert type(image) is AdornedImage


@pytest.mark.parametrize(
    "resolution, dwell_time, hfw",
    [("768x512", 1e-9, 1e-6), ("1536x1024", 1e-8, 1e-7), ("3072x2048", 1e-7, 1e-8), ("6072x4096", 1e-6, 1e-9)],
)
def test_with_settings(microscope, resolution: str, dwell_time: float, hfw: float):
    microscope.beams.electron_beam.horizontal_field_width.value = hfw
    settings = GrabFrameSettings(
        resolution=resolution, dwell_time=dwell_time, bit_depth=8
    )
    image = microscope.imaging.grab_frame(settings)
    assert type(image) is AdornedImage
    width, height = tuple(map(int, resolution.split("x")))
    assert image.width == width
    assert image.height == height
    assert image.data.shape == (height, width)
    assert_consistent_pix_size(image)


@pytest.mark.parametrize(
    "resolution, hfw, rectangle",
    [
        ("768x512", 1e-6, Rectangle(0, 0, 0.5, 0.5)),
        ("1536x1024", 1e-7, Rectangle(0.5, 0.5, 0.5, 0.5)),
        ("3072x2048", 1e-8, Rectangle(0.5, 0, 0.5, 0.5)),
        ("6072x4096", 1e-9, Rectangle(0, 0.5, 0.5, 0.5)),
    ],
)
def test_reduced_area(microscope, resolution, hfw, rectangle):
    microscope.beams.electron_beam.horizontal_field_width.value = hfw
    settings = GrabFrameSettings(resolution=resolution, reduced_area=rectangle)
    image = microscope.imaging.grab_frame(settings)
    assert type(image) is AdornedImage
    width, height = tuple(map(int, resolution.split("x")))
    width *= rectangle.width
    height *= rectangle.height
    assert image.width == width
    assert image.height == height
    assert image.data.shape == (height, width)
    assert_consistent_pix_size(image)