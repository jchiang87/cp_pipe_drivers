import os
import glob
import lsst.afw.image as afwImage
from lsst.afw.cameraGeom import utils as cgu
import lsst.obs.lsst as obs_lsst
import lsst_camera.cp_pipe_drivers as cpd

camera = obs_lsst.LsstCamMapper().camera
det_names = ['R22_S00', 'R22_S01', 'R22_S02',
             'R22_S10', 'R22_S11', 'R22_S12',
             'R22_S20', 'R22_S21', 'R22_S22']

image_source = cpd.CalibImageSource('CALIB/bias/2019-10-18')
bias_image = cgu.makeImageFromCamera(camera, detectorNameList=det_names,
                                     imageSource=image_source,
                                     imageFactory=afwImage.ImageF)
bias_image.writeFits('BOT_R22_6813D_bias_mosaic.fits')

image_source = CalibImageSource('CALIB/dark/2019-10-18')
#image_source = cpd.CalibImageSource(
#    'calib_products/rerun/dark_calibs_nobias/dark/2019-10-18')
dark_image = cgu.makeImageFromCamera(camera, detectorNameList=det_names,
                                     imageSource=image_source,
                                     imageFactory=afwImage.ImageF)
dark_image.writeFits('BOT_R22_6813D_dark_mosaic.fits')
#dark_image.writeFits('BOT_R22_6813D_dark_mosaic_nobias.fits')
