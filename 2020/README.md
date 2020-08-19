# Introduction

## Difference from 2019

* *Config Changes* - Config objects have been more forcefully implemented in `algo.py`, the objective moving forward is to have more and more data accessible through config objects.
* *Debug Messages* - The precise way debugging is going to be implemented is still in limbo.
* *Lack of 2019-specific code* - `targets.py`, `algo.py`, `rectUtil.py`, `poseEstimation.py`, and `config.py` have all been stripped of 2019-specfici code. In some cases that means removing the files, in others it means simply cutting chunks. Untill kickoff, this directory is designed to be a blank slate, improving on infrastructure from 2019.
* *Planned Threading Changes* - Theading is planned to play a larger role in this version of the codebase. Stay tuned.
* *Parsed Agument Changes* - Parsed arguments are now more tightly entertwined with configurations. When arguments are parsed the chosen `config` is updated with the parsed values. Parsed arguments supeceed `config` values. 

## Versioning

* Nb: Currently operating under opencv v3


# Documentation

## Files

### **`algo.py`**  

#### Summary 

* `algo` is the 'bread and butter' of the vision subsystem, it is where most of the important computer-vision related code goes. `algo` is one of the only places (apart from `targetUtils`) where `opencv` calls are made. 

#### Technical details of `algo`

* `algo` is a library file which defines differnet 'pipelines' for the vision subsystem. It is imported into `runpicam` and `picamstreamer`, which call `processFrame()`. `processFrame()` is responsible for looking at the passed in `config` and selecting the proper pipeline to run.
* By convention within *this* codebase (This might not be true everywhere!), a 'pipeline' is a method which follows the structure:
```
    frame & cfg -> result & outputframe
```
* Where `frame` is the raw (unmodified off of the camera) image, and `cfg` is the operating config,

### **`config.py`**  

#### Summary

* Library file which holds dictionaries reprensting different 'setups' that the vision system might be run in. For isntane, `calibConfig` is used when determining camera intrensics, while `GPConfigV1` is the config for the vision camera used on-robot.

#### Technical details of `config`

* Config is a python `dict`, which has two main sub-dictionaries: `algo` and `picam` (Not to be confused with the files of the same name, but they are related). Each sub-dict contains data used in the aforementioned parts of the vision subsystem. Generally, the `algo` sub-dict contains values used in `algo.py`, `targetUtils.py`, and `poseEstimation.py`
* Most of the values in the `picam` sub-dict deserve no special explanation. The documentation for each value can be found [here](https://picamera.readthedocs.io/en/release-1.13/api_camera.html)  They are values used in the creation of a `picam` object, speficially interacting with the `PiCamera` libary. 
* The `algo` sub-dict is not as straightforward however, each of these keys were written in as-needed, and will be explained here:
  * `algo`    - This value is matched to the list of pipeline methods in `algo.processFrame()`, use it to select the pipeline you want to run
  * `display` - Used to controll if methods in `poseEstimation` should draw on the passed frame. Drawing can be computation intensive, but invaluable when debugging 
    * Nb: This value is *forced* to `True` In picamStreamer
  * `hsvRangeLow` / `hsvRangeHigh` - Upper and lower bounds of `cv2.inRange`, implemented in the method `targetUtils.threshholdFrame()`

#### Visually

* A hirearchical view enumerating all potentional values expressed in a single `config`

```
myConfig
∟ "name" : "My Test Config!"                -- String (Describe your config! Use this key LIBERALLY!)
∟ "picam"
    ∟"resolution" : (640, 480)              -- Tuple of the form (int, int)
    ∟"iso": 400                             -- Int
    ∟"brightness": 0                        -- Signed Int
    ∟"contrast": 100                        -- Int
    ∟"flip": False                          -- Bool
    ∟"rotation": 0                          -- Int
    ∟"exposure_mode": "auto",               -- String
    ∟"exposure_compensation": 0,            -- Signed Int
∟ "algo"
    ∟"algo": "verticies"                    -- String
    ∟"display": False                       -- Bool
    ∟"hsvRangeLow": np.array([40,50,90])    -- Numpy array
    ∟"hsvRangeHigh": np.array([90,255,255]) -- Numpy array
    ∟"camIntrensics1080p"
        ∟"focalLength" : (1.81606009e+03,1.82082976e+03)        -- Tuple of the form (Float, Float)
        ∟"principalPoint" : (9.52672626e+02,5.47692316e+02)     -- Tuple of the form (Float, Float)
        ∟"distortionCoeffs" : np.array([ 1.07854440e-01, -8.34892908e-01, -1.86048786e-03, -1.26161591e-03,  1.44654595e+00])                                         -- Tuple of the form (Float, Float)
    ∟"state"
        ∟"operatingRes" : "high"            -- String
        ∟"TargetPNP" : targets.TargetPNP()  -- Targets.py Object
        ∟"TargetPID" : targets.TargetPID()  -- Targets.py Object
        ∟"startPipeTime" : -1               -- Signed Int

```

* Nb: It's important to brush up on your python dictionaries before playing around with `config.py`. asking `myConfig` for the value at key `"algo"` will return *another* dictionary, not the string "verticies". Examples of using nested dictionaries can be found scattererd throughout the codebase.

### **`cameraLatencyTest.py`** 

#### Summary

* Test script to determine how long it takes to pull frames out of the `camera` object.

### **`comm.py`**  

#### Summary

* Library file which acts as an abstraction over the `networktables` library

#### Technical details of `comm`

Coming soon!

### **`picam.py`**  

#### Summary

* Library file which acts as an abstraction over the `PiCamera` library, the reccomnded library for accessing camera data

#### Technical details of `picam.py`

Coming soon!

### **`picamStreamer.py`**  

#### Summary

* Runtime file which is primarily used for Debugging. Begins an MJPEG server which can be used to see the camera feed

### **`poseEstimation.py`**  

#### Summary

* Library File which is entirely dedicated to running a successful PnP pipeline.

#### Technical details of `poseEstimation.py`

Coming soon!

### **`runPiCam.py`**  

#### Summary

* Runtime file used in on-field operation. Ties together `config`, `algo`, `comm`, and `picam`.

#### Technical details of `runPiCam.py`

Coming soon!

### **`startVision.sh`**  

#### Summary

* Runtime file which is used by frcPiGen to start up `runPiCam`

### **`targetUtils.py`**  

#### Summary

* Library file entirely devoted to functions relating to target geometry

#### Technical details of `targetUtils.py`

### **`targets.py`**  

#### Summary

* Intermediary Library file used to provide an object-oriented framework for representing targets in networktables.

#### Technical details of `targets.py`

### **`testLatency.py`**

#### Summary

* Script used to determine the computation time of speific pipelines. 

## Runtime Structure

### Coming soon!

# Q&A

## I Want to Write Vision Code, Where do I Start?

* A good first step would be to make a `config` representing your home setup. This will allow you to get a hand on the python dictionary system.

## What Is the Minimum Amount of Work That Must be Done (software-wise) to go From One Season to the Next?

## I Don't Have Any Vision Hardware at my House, What Parts of the Codebase *Can* I Interact With? 

## How Much Computer Vision Theory Is Needed to Operate the Codebase?

