from .beams import *
from .gas import *
from .imaging import *
from .patterning import *
from .specimen import *

log = logging.getLogger(__name__)


class AutoFunctions:
    def __init__(self, microscope: 'MockSdbMicroscopeClient'):
        self._microscope = microscope

    def run_auto_cb(self):
        log.debug('Running mock auto-cb')


class MockSdbMicroscopeClient:
    def __init__(self):
        log.debug('Initializing MockSdbMicroscopeClient')
        self.auto_functions = AutoFunctions(self)
        self.specimen = Specimen(self)
        self.gas = Gas(self)
        self.beams = Beams(self)
        self.imaging = Imaging(self)
        self.patterning = Patterning(self)
        self._connected = False

    def connect(self, ip: Optional[str]=None, port: Optional[str]=None):
        log.debug(f'MockSdbMicroscopeClient mock-connecting to {ip}:{port}')
        self._connected = True

    def disconnect(self):
        log.debug('MockSdbMicroscopeClient mock-disconnecting')
        self._connected = False

