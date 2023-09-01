import logging
from typing import Optional

import numpy as np
from autoscript_sdb_microscope_client.enumerations import ImagingDevice
from autoscript_sdb_microscope_client.structures import GrabFrameSettings, AdornedImage
from skimage import draw

from .metadata import make_metadata, grab_frame_settings

log = logging.getLogger(__name__)


class ImageView:
    def __init__(self, microscope, device: int):
        self._microscope = microscope
        self._device = device
        self._last_image = None

    def grab_frame(self, settings: Optional[GrabFrameSettings] = None):
        log.debug(f"grab_frame: {settings}")
        settings = grab_frame_settings(self._microscope, settings)
        resolution_x, resolution_y = settings.resolution.split("x")
        resolution_x, resolution_y = int(resolution_x), int(resolution_y)
        log.debug(f"grab_frame: resolution = {resolution_y}, {resolution_x}")
        meta = make_metadata(self._microscope, settings=settings)
        dtype = np.uint8 if settings.bit_depth == 8 else np.uint16
        # Generate image data
        data = np.ones((resolution_y, resolution_x), dtype=dtype) * 255
        rect_coords = draw.rectangle(
            (resolution_y // 10, resolution_x // 10),
            (resolution_y // 10 * 9, resolution_x // 10 * 9),
        )
        data[tuple(rect_coords)] = 0
        # Get reduced are, if applicable
        if settings.reduced_area is not None:
            rect = settings.reduced_area
            ymin, xmin = np.ceil(np.multiply(data.shape, (rect.top, rect.left))).astype(
                int
            )
            ymax, xmax = np.floor(
                np.multiply(
                    data.shape, (rect.top + rect.height, rect.left + rect.width)
                )
            ).astype(int)
            log.debug(
                f"reduced area: {settings.reduced_area} -> {ymin}:{ymax}, {xmin}:{xmax}"
            )
            data = data[ymin:ymax, xmin:xmax].copy()
        # Store and return
        self._last_image = AdornedImage(data=data, metadata=meta)
        return self._last_image

    def get_image(self):
        log.debug(f"get_image: {self._last_image}")
        return self._last_image


class Imaging:
    def __init__(self, microscope):
        self.microscope = microscope
        self._views = {
            1: ImageView(microscope, ImagingDevice.ELECTRON_BEAM),
            2: ImageView(microscope, ImagingDevice.ION_BEAM),
            3: ImageView(microscope, ImagingDevice.ELECTRON_BEAM),
            4: ImageView(microscope, ImagingDevice.CCD_CAMERA),
        }
        self._active_view = 1

    def set_active_view(self, view: int):
        self._active_view = view

    def get_active_view(self):
        return self._active_view

    def get_active_device(self):
        return self._views[self.get_active_view()]._device

    def set_active_device(self, device: int):
        self._views[self.get_active_view()]._device = device

    def _active_image_view(self):
        return self._views[self.get_active_view()]

    def grab_frame(self, settings: Optional[GrabFrameSettings] = None):
        return self._active_image_view().grab_frame(settings)

    def get_image(self):
        return self._active_image_view().get_image()
