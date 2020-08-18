## Applications

* `runPiCam.py` - primary entrypoint when running in competition 
  (no server currently).  To get the highest framerate, we run 
  the frame-capture in a separate thread from the algorithm.

## Library

* `algo.py` - collection of various vision pipelines
* `picam.py` - thin vaneer atop PiCamera, support for threaded streaming
* `comm.py` - manage communication with robot via networktables
* `targets.py` - abstraction for target nettab representation
* `poseEstimation.py` - 
* `targetUtils.py` - 


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

* `algo.py` - Library file which holds `opencv` call
* `cameraLatencyTest.py` - Test script to determine how long it takes to pull frames out of the `camera` object
* `comm.py` - Library file which acts as an abstractino over the `networktables` library
* `config.py` - Library file which holds dictionaries reprensting different 'setups' that the vision system might be run in. For isntane, `calibConfig` is used when determining camera intrensics, while `GPConfigV1` is the config for the vision camera used on-robot.
* `picam.py` - Library file which acts as an abstraction over the `PiCamera` library, the reccomnded library for accessing camera data
* `picamStreamer` - Runtime file which is primarily used for Debugging. Begins an MJPEG server which can be used to see the camera feed.
* `poseEstimation.py` - Library File which is entirely dedicated to running a successful PnP pipeline.
* `runPiCam.py` - Runtime file used in on-field operation. Ties together `config`, `algo`, `comm`, and `picam`.
* `startVision.sh` - Runtime file which is used by the OS to start up `runPiCam`
* `steamTests` - GET RID OF THIS FILE 
* `targetUtils` - Library file entirely devoted to functions relating to target geometry.
* `targets.py` - Intermediary Library file used to provide an object-oriented framework for representing targets in networktables.
* `testLatency` - Script used to determine the computation time of speific pipelines. 


## Runtime Structure

# Institutional Questions

## I Want to Write Vision Code, Where do I Start?

* A good first step would be to make a `config` representing your home setup. This will allow you to get a hand on the python dictionary 

## What Is the Minimum Amount of Work That Must be Done (software-wise) to go From 2020->2021?
