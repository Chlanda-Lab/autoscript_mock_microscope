
class GisPort:
    def __init__(self, microscope, name: str):
        self.name = name
        self._microscope = microscope
        self._open = False

    def open(self):
        print(f'MockSdbMicroscopeClient: opening GIS port {self.name}')
        self._open = True

    def close(self):
        print(f'MockSdbMicroscopeClient: closing GIS port {self.name}')
        self._open = False

class Gas:
    def __init__(self, microscope):
        self._microcscope = microscope
        self.gis_ports = {
                'Pt dep': GisPort(microscope, 'Pt dep')
                }

    def get_gis_port(self, name: str):
        return self.gis_ports[name]


