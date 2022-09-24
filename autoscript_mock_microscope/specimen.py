from math import radians
from autoscript_sdb_microscope_client.structures import StagePosition
from autoscript_sdb_microscope_client.enumerations import CoordinateSystem

class Stage:
    @property
    def current_position(self):
        return self._current_position
    @current_position.setter
    def current_position(self, new_pos: StagePosition):
        self._current_position = new_pos

    def __init__(self, microscope):
        self._microcscope = microscope
        self._current_position = StagePosition(x=10e-6, y=10e-6, z=7e-6, r=radians(77), t=radians(45))
        self._coordinate_system = CoordinateSystem.SPECIMEN

    def absolute_move(self, stage_position: StagePosition):
        self.current_position = stage_position

    def relative_move(self, stage_position: StagePosition):
        self.current_position = StagePosition(
                self.current_position.x + stage_position.x,
                self.current_position.y + stage_position.y,
                self.current_position.z + stage_position.z,
                self.current_position.r + stage_position.r,
                self.current_position.t + stage_position.t)
    
    def set_default_coordinate_system(self, coordinate_system: CoordinateSystem):
        self._coordinate_system = coordinate_system


class Specimen:
    def __init__(self, microscope):
        self._microcscope = microscope
        self.stage = Stage(microscope)


