import math

from autoscript_sdb_microscope_client.enumerations import ImagingDevice
from autoscript_sdb_microscope_client.structures import Point

from .values import LimitValue, ListValue


class Scanning:
    def __init__(self):
        self.dwell_time = LimitValue(100e-9, limits=(0, 1))
        self.rotation = LimitValue(initial_value=0.0, limits=(0.0, 2 * math.pi))
        self.resolution = ListValue(
            "768x512",
            available_values=["768x512", "1536x1024", "3072x2048", "6144x4096"],
        )


class Beam:
    def __init__(self, microscope, device: int):
        self._microscope = microscope
        self._device = device
        self.beam_shift = LimitValue(Point(x=0, y=0))
        self.horizontal_field_width = LimitValue(500e-6, limits=(1e-9, 5e-3))
        self.scanning = Scanning()
        self.stigmator = LimitValue(Point(x=0, y=0), limits=None)
        self.working_distance = LimitValue(7e-6, limits=(1e-3, 1e-1))
        if device == ImagingDevice.ELECTRON_BEAM:
            self.high_voltage = LimitValue(30000, limits=(1000, 30000))
        elif device == ImagingDevice.ION_BEAM:
            self.high_voltage = LimitValue(30000, limits=(1000, 30000))
        if device == ImagingDevice.ELECTRON_BEAM:
            self.beam_current = LimitValue(5000, limits=(2000, 10000))
        elif device == ImagingDevice.ION_BEAM:
            self.beam_current = ListValue(
                1000e-12,
                available_values=[
                    10e-12,
                    30e-12,
                    50e-12,
                    100e-12,
                    300e-12,
                    500e-12,
                    1000e-12,
                    3000e-12,
                    7000e-12,
                ],
                select_closest=True,
            )

    def turn_off(self):
        print("Mock turning off beam")

    def turn_on(self):
        print("Mock turning on beam")


class Beams:
    def __init__(self, microscope):
        self._microscope = microscope
        self.electron_beam = Beam(microscope, ImagingDevice.ELECTRON_BEAM)
        self.ion_beam = Beam(microscope, ImagingDevice.ION_BEAM)
