"""
Module to compute amp-wise mean and stdev statistics.
"""
import sys
from collections import defaultdict
import numpy as np
import pandas as pd
import lsst.daf.persistence as dp
import lsst.afw.image as afwImage
import lsst.geom
import lsst.afw.math as afwMath


__all__ = ['get_stats', 'OverscanHandler', 'get_raw_amp_stats']


def get_stats(image, nsigma=10):
    """
    Parameters
    ----------
    image: lsst.afw.image.Image
        Image object for which to compute the clipped mean and clipped
        stdev.
    nsigma: int [10]
        Value to use for sigma clipping.

    Returns
    -------
    (float, float): Tuple of the (mean, stdev) of the pixel values.
    """
    stat_ctrl = afwMath.StatisticsControl(numSigmaClip=nsigma)
    flags = afwMath.MEANCLIP | afwMath.STDEVCLIP
    stats = afwMath.makeStatistics(image, flags=flags, sctrl=stat_ctrl)
    return stats.getValue(afwMath.MEANCLIP), stats.getValue(afwMath.STDEVCLIP)


class OverscanHandler:
    def __init__(self, image, amp_info):
        """
        Parameters
        ----------
        image: lsst.afw.image.Image
            The full imaging section of the amplifier.
        amp_info: lsst.afw.cameraGeom.AmpInfoRecord
            Object containing the amplifier pixel geometry.
        """
        self.image = image
        self.amp_info = amp_info
        oscan_corners = amp_info.getRawHorizontalOverscanBBox().getCorners()
        image_corners = image.getBBox().getCorners()
        # Create a bounding box using the upper left corner of the full
        # segment to guard against non-standard overscan region sizes.
        bbox = lsst.geom.Box2I(oscan_corners[0], image_corners[2])
        self.oscan = image.Factory(image, bbox)

    def get_stats(self, nsigma=10):
        """
        Return the clipped mean and clipped stdev of the serial
        overscan pixels.
        """
        return get_stats(self.oscan, nsigma=nsigma)

    def row_medians(self):
        """
        Return an array of row medians.
        """
        return np.median(self.oscan.array, axis=1)

    def overscan_corrected_image(self):
        """
        Return the overscan-corrected imaging section for the amp.
        """
        # Make a deep copy to modify and return, excluding the
        # overscan pixels.
        my_image = self.image.Factory(self.image,
                                      self.amp_info.getRawDataBBox(),
                                      deep=True)
        ny, nx = my_image.array.shape
        for row, value in zip(range(ny), self.row_medians()):
            my_image.array[row, :] -= value
        return my_image


def get_raw_amp_stats(butler, dataId, nsigma=10, subtract_oscan=True):
    """
    Parameters
    ----------
    butler: lsst.daf.persistence.Butler
        The data butler for the desired repo.
    dataId: dict
        Dictionary identifying the subset of data to process.
    nsigma: float [10]
        Value to use for sigma-clipping.
    subtract_oscan: bool [True]
        Flag to perform (row-wise) overscan correction.

    Returns
    -------
    pandas.DataFrame with columns for run, expId, raftName,
    detectorName, channel, seqfile, expTime, imageType, testType,
    imaging section mean, imaging section stdev.
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
        oscan_handler = OverscanHandler(amp_exp.getImage(), amp_info)
        oscan_mean, oscan_stdev = oscan_handler.get_stats(nsigma=nsigma)
        if subtract_oscan:
            image = oscan_handler.overscan_corrected_image()
        else:
            image = amp_exp.getImage().Factory(amp_exp.getImage(),
                                               amp_info.getRawDataBBox())
        mean, stdev = get_stats(image, nsigma=nsigma)
        data['mean'].append(mean)
        data['stdev'].append(stdev)
        for key, value in dataref.dataId.items():
            data[key].append(value)
        data['seqfile'].append(md.get('SEQFILE'))
        for key, header_key in header_keys.items():
            if key not in dataref.dataId:
                data[key].append(md.get(header_key))
    return pd.DataFrame(data=data)
