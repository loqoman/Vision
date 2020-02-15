# Representing configurations as 2D Python dictionaries
# vision parameter groups (aka configs)
#
# given the name of a config (eg "greenled") access via:
#
#  import config
#  cfg = getattr(config, "greenled")
#
#  (see bottom for details on parameters)
import numpy as np
import copy
import targets
# ------ Base -------

_base = {
    "picam": {
        "resolution": (640, 480), 
        "framerate": 60,
        "sensormode": 7,    # Fixes auto wb 'hidden' settings
                            
    },
    "algo": {
        # Assuming retro-reflective tape
        "hsvRange0": np.array([30,150,170]),
        "hsvRange1": np.array([90,255,255]),
        "pnpCam": "pi"
    }
}

# ------ Test config -------
# Shows most-if not all-of the possible values used in configs
testConfig = copy.deepcopy(_base)
testConfig.update({
    "name": "testConfig",
})
# Camera-Specific Settings
testConfig["picam"].update({
    "resolution": (640, 480),
    "iso": 400,
    "brightness": 0,
    "contrast": 100,
    "flip": False,
    "rotation": 0,
    "exposure_mode": "auto", #"fixedfps",
    "exposure_compensation": 0, # [-25, 25]
})
# Algo-Specific settings
# TODO: Change the outer/innter-most setting of algo 
testConfig["algo"].update({
    "algo": "empty", # Chose proper algo streaming
    "display": False,# 1 if streaming
    "hsvRangeLow": np.array([0,0,90]),
    "hsvRangeHigh": np.array([255,255,255]),
    "pnpCam": "dbcam8"
})

# ------ Testing configs -------
# Shows most-if not all-of the possible values used in configs
moduleDebuggingConfig = copy.deepcopy(_base)
moduleDebuggingConfig.update({
    "name": "Debugging Config used w/ a 2019 module",
})
# Camera-Specific Settings
moduleDebuggingConfig["picam"].update({
    "resolution": (1920, 1080),
    "framerate": 90,
    "iso": 400,
    "brightness": 40,
    "contrast": 100,
    "flip": False,
    "rotation": 0,
    "exposure_mode": "off", #"fixedfps",
    "exposure_compensation": -25, # [-25, 25]
})
# Algo-Specific settings
# TODO: Change the outer/innter-most setting of algo 
moduleDebuggingConfig["algo"].update({
    "algo": "verticies", # Chose proper algo streaming
    "display": False,# 1 if streaming
    "hsvRangeLow": np.array([40,50,90]),
    "hsvRangeHigh": np.array([90,255,255]),

    "theta" : 0, # Represents the angle of elevation

    "camIntrensics1080p": {
        "focalLength" : (1.79116329e+03,1.79568335e+03),
        "principalPoint" : (9.64697499e+02,5.94350454e+02),
        "distortionCoeffs" : np.array([  1.03245422e-01, -8.14646031e-01,  8.78989595e-04,
         5.05879957e-04,  1.43069887e+00])
    },
    "camIntrinsics640p": {
        "focalLength" : (634.89045322, 634.85728747),
        "principalPoint" : (322.55085532, 250.9350097),
        "distortionCoeffs" : np.array([ 1.14347782e-01, -1.04102188e+00,  2.73924512e-03,
        7.23847549e-04,  2.04951815e+00])
    },

    "camIntrensics720p": { #720p
    "focalLength" : (1.24108285e+03, 1.24478598e+03),
    "principalPoint" : (6.43779311e+02, 3.93884033e+02),
    "distortionCoeffs" : np.array([1.14833683e-01, -9.74930348e-01,  1.03528449e-03,
         7.31745519e-05,  1.87194365e+00])
    }


        # Alternate camera intrensics (from other team)(For a 720p frame): 
        #       disortion Coefficients:  (2.9666848459501894e-02, 7.7071617830897565e-01, 0, 
        #                                                       0, -2.7882844813877661e+00)
        # Focal Length / Principal Point:
        #       Fx = 9.7251025460519838*10^2~~ 972.51
        #       Cx = 538                  ~~ 538
        #       Fy = 9.7251025460519838*10^2 ~~ 972.51
        #       Cy = 3.5650000000000000*10^2 ~~ 356.5
})

calibConfig = copy.deepcopy(_base)
calibConfig.update({
    "name": "Config to use when calibrating the camera",
})
# Camera-Specific Settings
calibConfig["picam"].update({
    "resolution": (640, 480),
    "framerate": 90,
    "iso": 0,
    "flip": False,
    "rotation": 0,
    "exposure_mode": "auto", #"fixedfps",
    "exposure_compensation": 0, # [-25, 25]
})
# Algo-Specific settings
# TODO: Change the outer/innter-most setting of algo 
calibConfig["algo"].update({
    "algo": "calibCap", # Chose proper algo streaming
    "display": False,# 1 if streaming

})

# ------ Deployment configs -------

GPConfigV1 = copy.deepcopy(_base)
GPConfigV1.update({
    "name": "gpConfig",
})
# Camera-Specific Settings
GPConfigV1["picam"].update({
    "resolution": (1920, 1080), # cv2.resize() later
    "framerate": 30, # TODO: Come back to
    "iso": 400,
    "brightness": 40,
    "contrast": 100,
    "flip": False,
    "rotation": 0,
    "exposure_mode": "off", #"fixedfps",
    "exposure_compensation": -25, # [-25, 25]
})
# Algo-Specific settings
# Generally, these are going to be numbers/flags/constants used in cv2 function calls
GPConfigV1["algo"].update({
    "algo": "empty",    # Chose proper algo streaming
                        # Closed loop pnp here
                        # TODO: Chamge this back later
    "display": False,   # 1 if streaming
    "hsvRangeLow": np.array([40,50,90]),
    "hsvRangeHigh": np.array([255,255,255]),

    "camIntrensics1080p": {
        "focalLength" : (1.79116329e+03,1.79568335e+03),
        "principalPoint" : (9.64697499e+02,5.94350454e+02),
        "distortionCoeffs" : np.array([  1.03245422e-01, -8.14646031e-01,  8.78989595e-04,
         5.05879957e-04,  1.43069887e+00])
    },

})

# create a sub-dict under 'algo' representing the current state of the run.
# NOTE: the 'state' dict is not under 'picam', simply because picam shouldnt care what the current state is. It should be read once when communicating the 
GPConfigV1["algo"].update({
    "state": {
        "operatingRes" : "high", # Determines weather or not we run cv2.resize the image before processing
        "TargetPNP" : targets.TargetPNP(), # Target objects 
        "TargetPID" : targets.TargetPID(),
        "opeartingPipe" : "pnp", # Will corresspond to pipelines in algo.processframe()
        "startPipeTime" : -1,
        #"mountingIntrensics" : -1,
        #"turretAngle" : -1,

    }
})

default = moduleDebuggingConfig
# picam parameters ---------------------------------------------
# see: https://picamera.readthedocs.io/en/release-1.13/api_camera.html
#
#  analog_gain: read-only after setting exposure/iso
#  annotate_*
#  awb_gains:  red-blue balance depends upon awb_mode != "off"
#              range: 0-8, typically: .9-1.9
#  awb_mode: ("auto") ["off", "auto", "cloudy", ...' (white balance)
#  brightness: (50) [0-100]
#  clock_mode
#  closed: read-only
#  color_effects: (None) or (u,v) between 0-255
#  contrast: (0) [-100, 100]
#  crop: (see zoom)
#  digital_gain: read-only after setting exposure/iso
#  drc_strength (off) [off, low, medium, high] (dynamic range compression)
#  exposure_compensation (0) [-25, 25]
#  exposure_mode (auto) [off, auto, ..., fixedfps, ...]
#       off is special: disabled auto-gain-control fixing values for 
#       digital_gain and analog_gain.  These are set indirectly via
#       iso call which should be made (and allowed to settle) before
#       setting the mode to off.
#  exposure_speed: read-only microseconds, relates to shutter-speed
#                   note this value tends to drift torwards a few values
#  flash_mode:
#  frame:
#  framerate: pertains to video-port captures. Coupled with resolution
#       determines the mode that the camera operates in. 
#       see also sensor_mode
#  framerate_range:
#  hflip, vflip:  (False)
#  image_denoise: (True)
#  image_effect: (none) [none,negative,blur,...,posterize...]
#  iso (light sensitivity): sets analog_gain and digital_gain
#       (0) [0,100,200,320,400,500,640,800] (0 is auto)
#   certain exposure_modes override iso (esp "off") 
#  led (False)
#  meter_mode: (average) [average,spot,backlit,matrix]
#  preview...
#  raw_format: deprecated
#  recording: read-only
#  resolution: (X,Y), 'XxY', etc
#  revision: read-only  [ov5647, imx219]  means V1 or V2 cam module
#  saturation: (0) [-100, 100]
#  sensor_mode: (0) [0-7]  (0 computes based on framerate & res, 7 is fastest)
#  sharpness: (0) [-100,100]
#  shutter_speed: (0) microsecs (set with framerate, overlap exposure_speed)
#  still_stats
#  timestamp
#  vflip, hflip: (False)
#  video_denoise: (True)
#  video_stabilization: (False)
#  zoom: (0,0,1,1)

# algo parameters ---------------------------------------------

