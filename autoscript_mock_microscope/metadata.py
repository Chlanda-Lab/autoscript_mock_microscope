from autoscript_sdb_microscope_client.structures import *
from autoscript_sdb_microscope_client.enumerations import ImagingDevice
from math import radians
import numpy as np
from datetime import datetime
from typing import Optional

metadata_ini_formatstring = '''\
[User]
{dt}

[System]
Type=DualBeam
EucWD=0.007

[Beam]
BeamShiftX=0
BeamShiftY=0
ScanRotation={scan_rotation}
Beam={beam_str}
Scan={scan_str}

[{beam_str}]
HFW={hfw}
VFW={vfw}
WD={wd}
ScanRotation={scan_rotation}
StageX={stagex}
StageY={stagey}
StageZ={stagez}
StageR={stager}
StageTa={staget}
StageTb=0
StigmatorX=0
StigmatorY=0
BeamShiftX=0
BeamShiftY=0
EucWD=0.007

[Scan]
Dwelltime={dwell}
PixelWidth={pix_size}
PixelHeight={pix_size}
HorFieldsize={hfw}
VerFieldsize={vfw}

[{scan_str}]
Dwell={dwell}
PixelWidth={pix_size}
PixelHeight={pix_size}
HorFieldsize={hfw}
VerFieldsize={vfw}

[Stage]
StageX={stagex}
StageY={stagey}
StageZ={stagez}
StageR={stager}
StageT={staget}
StageTb=0
WorkingDistance={wd}
StageRawX={stagex}
StageRawY={stagey}
StageRawZ={stagez}
StageRawR={stager}
StageRawT={staget}
StageRawTb=0
'''


def grab_frame_settings(microscope, settings: Optional[GrabFrameSettings]=None):
    if settings is not None:
        dwell_time = settings.dwell_time
        resolution = settings.resolution
    else:
        beam, _, _ = active_beam_and_name(microscope)
        dwell_time = beam.scanning.dwell_time.value
        resolution = beam.resolution.value
    return GrabFrameSettings(resolution=resolution, dwell_time=dwell_time)


def active_beam_and_name(microscope):
    device = microscope.imaging.get_active_device()
    beam, beam_str, scan_str = {
            ImagingDevice.ELECTRON_BEAM: (microscope.beams.electron_beam, 'EBeam', 'EScan'),
            ImagingDevice.ION_BEAM: (microscope.beams.ion_beam, 'IBeam', 'IScan'),
        }[device]
    return beam, beam_str, scan_str


def make_metadata(
        microscope,
        time: Optional[datetime]=None,
        settings: Optional[GrabFrameSettings]=None) -> AdornedImageMetadata:
    if time is None:
        time = datetime.now()
    stage_pos = microscope.specimen.stage.current_position
    beam, beam_str, scan_str = active_beam_and_name(microscope)

    settings = grab_frame_settings(microscope, settings)
    resolution_x, resolution_y = settings.resolution.split('x')
    resolution_x, resolution_y = int(resolution_x), int(resolution_y)
    hfw = beam.horizontal_field_width.value
    pix_size = hfw / resolution_x
    vfw = pix_size * resolution_y
    binary_result = AdornedImageMetadataBinaryResult(
            bits_per_pixel=settings.bit_depth,
            pixel_size=Point(x=pix_size, y=pix_size))
    return AdornedImageMetadata(
            binary_result=binary_result,
            metadata_as_ini=metadata_ini_formatstring.format(
                dt=time.strftime('Date=%m/%d/%Y\nTime=%H:%M:%S %p'),
                scan_rotation=beam.scanning.rotation.value,
                beam_str=beam_str,
                scan_str=scan_str,
                stagex=stage_pos.x,
                stagey=stage_pos.y,
                stagez=stage_pos.z,
                stager=stage_pos.r,
                staget=stage_pos.t,
                dwell=settings.dwell_time,
                hfw=hfw,
                vfw=vfw,
                pix_size=pix_size,
                wd=beam.working_distance.value,
                )
            )
