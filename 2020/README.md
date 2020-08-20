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

## Library Modules

### **`algo.py`**  

#### Summary 

* `algo` is the 'bread and butter' of the vision subsystem, it is where most of the important computer-vision related code goes. `algo` is one of the only places (apart from `targetUtils`) where `opencv` calls are made. 

#### Technical details of `algo`

* `algo` is a library file which defines differnet 'pipelines' for the vision subsystem. It is imported into `runpicam` and `picamstreamer`, which call `processFrame()`. `processFrame()` is responsible for looking at the passed in `config` and selecting the proper pipeline to run.
* By convention within *this* codebase (This might not be true everywhere!), a 'pipeline' is a method which follows the structure:
```
    frame & cfg -> result & outputframe
```
* Where `frame` is the raw (unmodified off of the camera) image, and `cfg` is the operating config at the `'algo'` level.
* In a similar method to [GRIP](https://docs.limelightvision.io/en/latest/grip_software.html), the intention is that pipelines described in `algo.py` will be an custom selection of functions defined `targetUtils.py`, allowing the user to create specific pipelines based on general-purpose functions.

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
  * `camIntrensics` - Sub-Dict which holds [camera intrensics](https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html) (Chiefly `focalLength` and `principalPoint`) values. Note that a given set of camera intrensics corresponds to a unique **camera and operating resolution**. 
    * `poseEstimation` searches for the sub-dict under the key 'camIntrensics', however other configs have amera intresnsics ucnder a differnet key, this can be useful for storing calibration data of a backup camera.
      * In the case of `moduleDebuggingConfig`, three cameras were calibrated (one primary and two backup), and physically marked as cameras 'A', 'B', and 'C'. Even through the code never looks for these values, their intrensics were recoded in the config for future use.
* Finally, the `state` sub-sub-dict was added near the tail-end of the 2020 season to allow for easier access of `target` objects, and the potential to change operating mode on the fly.
  * In the 2020 season, there was a planned pipeilne which would feature the camera 'switching' operating resolutions. The camera would run a non-pnp, low resolution 'inital search' of a frame to determine (rougly) where the points of interest were for a pnp computation, then the full-resolution imagine would be searched for the points of interest, but only where the low-resolution image ballparked the points. This strategy was never implemented.

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
    ∟"camIntrensics"
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

### **`comm.py`**  

#### Summary

* Library file which acts as an abstraction over the `networktables` library. `comm` is responsible for creating and sending messages over the connection the vision system has with the robot over [networktables](https://robotpy.readthedocs.io/projects/pynetworktables/en/stable/).


#### Technical details of `comm`

* The `comm` module has a global variable (`theComm`) which points to a single instance of the `comm` class. The most common functions used within the `comm` modules are those at the top, which all reference `theComm`. By and large, the `Target` class has the most interaction with methods inside `comm`. The `comm` module itself is used only in `runpicam` to send the status of the vision system.
  * Nb: For `Target.send()` to work, a `comm` object *does* have to be created
* By design, `runpicam` interacts with (sets the value of ) `target` objects, which all methods inside `comm` 

### **`picam.py`**  

#### Summary

* Library file which acts as an abstraction over the `PiCamera` library, the reccomnded library for accessing camera data. `picam` is an abtraction over several modules in the [`picamera`](https://github.com/waveform80/picamera) library.

#### Technical details of `picam.py`

* `picam` is the one-stop-shop for dealing with any settings related to the picamera. The PiCam object is passed config at the "picam" level on creation, which is iterated over to find any settigns related to the camera. 
* Of note is the `sensormode` paramater, which can result in several headaches if not set properly. Through experimentation, `sensormode` overrides white balence and exposure settings which causes the camera to appear over-saturated or under-saturated based on the proximity of an object (When an object was brought very close to the camera, it would change exposure settings, which would persist when the object was removed from the cameras field of view). In-depth documentation of camera settings can be found [here](https://picamera.readthedocs.io/en/release-1.13/api_camera.html).

### **`targetUtils.py`**  

#### Summary

* `targetUtils` holds all the functions which deal with target geometry and the majority of `opencv` calls. 

#### Technical details of `targetUtils.py`

* The type of function that belongs in `targetUtils` is less rigid than `algo`. By convention, if there is a function which relates to target extraction, isolation, or sorting, then it belongs in `targetUtils`. All the functions in `targetUtils` have access to the "algo" level of config, so items such as hsv ranges can be made avabile.   
* Each (major) function in `targetUtils` has an assoicaited [doctest](https://docs.python.org/3.5/library/doctest.html), which can load data from the `data/` folder one, be it acutal images (with `cv2.imread()`), or just a list of points. A good example of this is the `target2pnp8points()` function, with can 'Sort the target's points into a 'pnp format' as defined in poseEstimation.py'. The doctest uses the half-hexagon points in `pnpDebugFrame1.png`. The output can be roughly correlated to the source image to make sure the sorting was done properly. Additionally, a doctest can be used to load and draw over an image for graphical feedback.
  * Note that most of the doctests arn't full blown unit tests, as some of the doctests don't have 'fail' conditions, rather just output the result of the function through logging. Python doctests support a failure mode (with syntax similar to an `assert()`) ensuring the doctest output matches the expected output.


### **`poseEstimation.py`**  

#### Summary

* Library File which is entirely dedicated to running a successful PnP pipeline.

#### Technical details of `poseEstimation.py`

Coming soon!

### **`picamStreamer.py`**  

#### Summary

* Runtime file which is primarily used for Debugging. Begins an MJPEG server which can be used to see the camera feed

### **`targets.py`**  

#### Summary

* Intermediary Library file used to provide an object-oriented framework for representing targets in networktables.

#### Technical details of `targets.py`

## Runtime Files

### **`runPiCam.py`**  

#### Summary

* Runtime file used in on-field operation. Ties together `config`, `algo`, `comm`, and `picam`.

#### Technical details of `runPiCam.py`

Coming soon!

### **`startVision.sh`**  

#### Summary

* Runtime file which is used by frcPiGen to start up `runPiCam`

## Debugging Scripts

* Using pre-captured frames, one can do 'offline' work with the vision code without the need for physical hardware. 

### **`cameraLatencyTest.py`** 

#### Summary

* Test script to determine how long it takes to pull frames out of the `camera` object.

### **`testLatency.py`**

#### Summary

* Script used to determine the computation time of speific pipelines. 

## Runtime Structure

### Logging

### `FRCVision`

### Coming soon!

# Q&A

## I Want to Write Vision Code, Where do I Start?

* A good first step would be to make a `config` representing your home setup. This will allow you to get a hand on the python dictionary system.

## What Is the Minimum Amount of Work That Must be Done (software-wise) to go From One Season to the Next?

## I Don't Have Any Vision Hardware at my House, What Parts of the Codebase *Can* I Interact With? 

## How Much Computer Vision Theory Is Needed to Operate the Codebase?

