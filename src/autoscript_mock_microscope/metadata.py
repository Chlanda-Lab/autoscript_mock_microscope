from datetime import datetime
from typing import Optional

from autoscript_sdb_microscope_client.enumerations import ImagingDevice
from autoscript_sdb_microscope_client.structures import (
    AdornedImageMetadata,
    AdornedImageMetadataBinaryResult,
    GrabFrameSettings,
    Point,
    Rectangle,
)

metadata_ini_formatstring = """\
[User]
{dt}

[System]
Type=DualBeam
EucWD=0.007

[Beam]
HV={hv}
BeamShiftX=0
BeamShiftY=0
ScanRotation={scan_rotation}
Beam={beam_str}
Scan={scan_str}

[{beam_str}]
HFW={hfw}
VFW={vfw}
WD={wd}
HV={hv}
BeamCurrent={beam_current}
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
PixelWidth={pix_width}
PixelHeight={pix_height}
HorFieldsize={hfw}
VerFieldsize={vfw}
Average=0
Integrate=0

[{scan_str}]
Dwell={dwell}
PixelWidth={pix_width}
PixelHeight={pix_height}
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

[Image]
Average=0
Integrate=0
ResolutionX={resolution_x}
ResolutionY={resolution_y}
"""


def grab_frame_settings(
    microscope, settings: Optional[GrabFrameSettings] = None
) -> GrabFrameSettings:
    if settings is None:
        new_settings = GrabFrameSettings()
    else:
        new_settings = GrabFrameSettings(
            resolution=settings.resolution,
            dwell_time=settings.dwell_time,
            bit_depth=settings.bit_depth,
            reduced_area=settings.reduced_area,
        )
    beam, _, _ = active_beam_and_name(microscope)
    if new_settings.dwell_time is None:
        new_settings.dwell_time = beam.scanning.dwell_time.value
    if new_settings.resolution is None:
        new_settings.resolution = beam.scanning.resolution.value
    if new_settings.reduced_area is None:
        new_settings.reduced_area = Rectangle(left=0, top=0, width=1, height=1)
    return new_settings


def active_beam_and_name(microscope):
    device = microscope.imaging.get_active_device()
    beam, beam_str, scan_str = {
        ImagingDevice.ELECTRON_BEAM: (microscope.beams.electron_beam, "EBeam", "EScan"),
        ImagingDevice.ION_BEAM: (microscope.beams.ion_beam, "IBeam", "IScan"),
    }[device]
    return beam, beam_str, scan_str


def make_metadata(
    microscope,
    time: Optional[datetime] = None,
    settings: Optional[GrabFrameSettings] = None,
) -> AdornedImageMetadata:
    if time is None:
        time = datetime.now()
    stage_pos = microscope.specimen.stage.current_position
    beam, beam_str, scan_str = active_beam_and_name(microscope)

    settings = grab_frame_settings(microscope, settings)
    resolution_x, resolution_y = settings.resolution.split("x")
    resolution_x, resolution_y = int(resolution_x), int(resolution_y)
    full_hfw = beam.horizontal_field_width.value 
    full_vfw = full_hfw * resolution_y / resolution_x
    hfw = full_hfw * settings.reduced_area.width
    vfw = full_vfw * settings.reduced_area.height
    pix_width = full_hfw / resolution_x
    pix_height = full_vfw / resolution_y
    binary_result = AdornedImageMetadataBinaryResult(
        bits_per_pixel=settings.bit_depth, pixel_size=Point(x=pix_width, y=pix_height)
    )
    return AdornedImageMetadata(
        binary_result=binary_result,
        metadata_as_ini=metadata_ini_formatstring.format(
            dt=time.strftime("Date=%m/%d/%Y\nTime=%H:%M:%S %p"),
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
            pix_width=pix_width,
            pix_height=pix_height,
            wd=beam.working_distance.value,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
            hv=beam.high_voltage.value,
            beam_current=beam.beam_current.value,
        ),
    )
