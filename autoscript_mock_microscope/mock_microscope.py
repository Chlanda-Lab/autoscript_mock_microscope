from autoscript_sdb_microscope_client.structures import *
from math import radians
from .beams import *
from .imaging import *
from .gas import *
from .specimen import *
from .patterning import *

class AutoFunctions:
    def __init__(self, microscope: 'MockSdbMicroscopeClient'):
        self._microscope = microscope

    def run_auto_cb(self):
        print('Running mock auto-cb')

class MockSdbMicroscopeClient:
    def __init__(self):
        self.auto_functions = AutoFunctions(self)
        self.specimen = Specimen(self)
        self.gas = Gas(self)
        self.beams = Beams(self)
        self.imaging = Imaging(self)
        self.patterning = Patterning(self)
        self._connected = False

    def connect(self, ip=None, port=None):
        print(f'MockSdbMicroscopeClient mock-connecting to {ip}:{port}')
        self._connected = True

    def disconnect(self):
        print(f'MockSdbMicroscopeClient mock-disconnecting')
        self._connected = False

