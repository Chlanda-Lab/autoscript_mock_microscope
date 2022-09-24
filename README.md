# Autoscript Mock Microscope

Emulate a ThermoFisher Aquilos 1 or 2 for development.

The core of this project is the MockSdbMicroscopeClient object, which is supposed to emulate a real Aquilos.
It contains the same data structures and functions as the real SdbMicroscopeClient.
Grabbing an image returns an AdornedImage with black pixels, but somewhat correct metadata such as stage position.
Please note: it is far from complete.
If there is a function you need, feel free to either implement it yourself and create a pull request, create an issue here or drop me an email.

## Usage

You can use the MockSdbMicroscopeClient in place of the real SdbMicroscopeClient, it exposes the same API.

```
from autoscript_mock_microscope import MockSdbMicroscopeClient
microscope = MockSdbMicroscopeClient()
microscope.connect()
...
```
