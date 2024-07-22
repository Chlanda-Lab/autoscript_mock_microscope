from autoscript_sdb_microscope_client.enumerations import (
    BeamType,
    PatternScanDirection,
    PatternScanType,
    PatterningState,
)
from random import randint
from typing import List


class RectanglePattern:
    def __init__(
        self,
        application_file: str,
        beam_type: int,
        center_x: float,
        center_y: float,
        depth: float,
        dwell_time: float,
        enabled: bool,
        height: float,
        rotation: float,
        scan_direction: str,
        scan_type: str,
        width: float,
    ):
        self.application_file = application_file
        self.beam_type = beam_type
        self.center_x = center_x
        self.center_y = center_y
        self.depth = depth
        self.dwell_time = dwell_time
        self.enabled = enabled
        self.height = height
        self.rotation = rotation
        self.scan_direction = scan_direction
        self.scan_type = scan_type
        self.width = width
        self.id = randint(0, 10000000)


class Patterning:
    def __init__(self, microscope):
        self._microcscope = microscope
        self._patterns: "List[RectanglePattern]" = list()
        self._default_application_file = "Si"

    def list_all_application_files(self):
        return ["Si"]

    def clear_patterns(self):
        self._patterns.clear()

    def set_default_application_file(self, application_file: str):
        if application_file not in self.list_all_application_files():
            raise ValueError(
                f'Application file "{application_file}" not available in {self.list_all_application_files()}'
            )
        self._default_application_file = application_file

    def create_rectangle(
        self,
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        depth: float,
    ) -> "RectanglePattern":
        pattern = RectanglePattern(
            application_file=self._microcscope.patterning._default_application_file,
            beam_type=BeamType.ION,
            center_x=center_x,
            center_y=center_y,
            depth=depth,
            dwell_time=100e-9,
            enabled=True,
            height=height,
            rotation=0.0,
            scan_direction=PatternScanDirection.TOP_TO_BOTTOM,
            scan_type=PatternScanType.SERPENTINE,
            width=width,
        )
        self._patterns.append(pattern)
        return pattern

    def create_cleaning_cross_section(self, *args, **kwargs) -> "RectanglePattern":
        return self.create_rectangle(*args, **kwargs)

    def run(self):
        print("Running mock-patterning")

    def start(self):
        print("Starting mock-patterning")

    def stop(self):
        print("Stopping mock-patterning")

    @property
    def state(self) -> PatterningState:
        return PatterningState.IDLE

