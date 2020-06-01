import os
import glob
import lsst.afw.image as afwImage


__all__ = ['CalibImageSource']


class CalibImageSource:
    """
    ImageSource class to pass to the cameraGeom.makeImageFromCamera
    function to make focal plane mosaics.
    """
    def __init__(self, calib_dir):
        """
        Parameters
        ----------
        calib_dir : str
            Directory containing FITS calibration products.
        """
        self.calib_dir = calib_dir
        self.files = dict()
        for item in sorted(glob.glob(
                os.path.join(calib_dir, '*-R??-S??-det???_*.fits'))):
            det_name = '_'.join(os.path.basename(item).split('-')[1:3])
            self.files[det_name] = item
        self.isTrimmed = True
        self.background = 0

    def getCcdImage(self, detector, imageFactory, binSize):
        """
        Mosaic the amplifier data from a raw file into a composed
        CCD with the prescan and overscan regions removed.

        Parameters
        ----------
        detector: lsst.afw.cameraGeom.Detector
            The Detector object for the desired CCD.
        imageFactory: lsst.afw.Image
            Image class to use to make a Image object to pass to
            the cameraGeom mosaicking code.
        binSize: int
            Not used. This is needed for interface compatibility with
            the cameraGeom code.

        Returns
        -------
        (lsst.afw.Image, )
        """
        det_name = detector.getName()
        image = imageFactory(self.files[det_name])
        return (image, )
