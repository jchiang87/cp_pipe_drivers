import sys
from collections import defaultdict
import numpy as np
import pandas as pd
import lsst.daf.persistence as dp
import lsst.afw.image as afwImage
import lsst.geom
import lsst.afw.math as afwMath


__all__ = ['get_raw_amp_stats']


def get_overscan_stats(image, amp_info):
    """
    Compute the mean and standard deviation of the serial overscan
    pixels for an amp.  Corrections are made for non-standard overscan
    sizes.

    Parameters
    ----------
    image: lsst.afw.image.Image
        The full imaging section of the amplifier.
    amp_info: lsst.afw.cameraGeom.AmpInfoRecord
        Object containing the amplifier pixel geometry.

    Returns
    -------
    (float, float): Tuple of the (mean, stdev) of the overscan pixel values.
    """
    oscan_corners = amp_info.getRawHorizontalOverscanBBox().getCorners()
    image_corners = image.getBBox().getCorners()
    # Create a bounding box using the upper left corner of the full
    # segment to guard against non-standard overscan region sizes.
    bbox = lsst.geom.Box2I(oscan_corners[0], image_corners[2])
    oscan = image.Factory(image, bbox)
    stats = afwMath.makeStatistics(oscan, afwMath.MEAN | afwMath.STDEV)
    return stats.getValue(afwMath.MEAN), stats.getValue(afwMath.STDEV)


def get_raw_amp_stats(butler, dataId, nsigma=5):
    """
    run, expId, raftName, detectorName, channel, seqfile, expTime,
    imageType, testType
    """
    header_keys = dict(expTime='EXPTIME', imageType='IMGTYPE',
                       testType='TESTTYPE', mjd_obs='MJD-OBS')
    data = defaultdict(list)
    datarefs = butler.subset('raw_amp', dataId=dataId)
    namps = len(datarefs)
    for i, dataref in enumerate(datarefs):
        print(i, namps)
        sys.stdout.flush()
        md = dataref.get('raw_md')
        amp_exp = dataref.get('raw_amp')
        det = amp_exp.getDetector()
        channel = dataref.dataId['channel']
        amp_info = list(det)[channel-1]
        oscan_mean, oscan_stdev \
            = get_overscan_stats(amp_exp.getImage(), amp_info)
        threshold = oscan_mean + nsigma*oscan_stdev
        image = amp_exp.getImage().Factory(amp_exp.getImage(),
                                           amp_info.getRawDataBBox())
        index = np.where(image.array < threshold)
        mean = np.mean(image.array[index])
        stdev = np.std(image.array[index])
        data['mean'].append(mean)
        data['stdev'].append(stdev)
        for key, value in dataref.dataId.items():
            data[key].append(value)
        data['seqfile'].append(md.get('SEQFILE'))
        for key, header_key in header_keys.items():
            if key not in dataref.dataId:
                data[key].append(md.get(header_key))
    return pd.DataFrame(data=data)
