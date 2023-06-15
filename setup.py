from distutils.core import setup

setup(
    name='Autoscript mock microscope',
    version='0.1',
    description='Emulate a ThermoFisher Aquilos (2)',
    author='Moritz Wachsmuth-Melm',
    author_email='github@moritzwm.de',
    url='https://github.com/Chlanda-Lab/autoscript_mock_microscope',
    packages=['autoscript_mock_microscope'],
    install_requires=[
        'tk',
        'numpy',
        'scikit-image',
        'opencv-python-headless'
        ],
)
