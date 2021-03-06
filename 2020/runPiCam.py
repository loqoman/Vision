#!/usr/bin/env python3
#
# runPiCam.py runs the imaging algorithm in algo.py on a stream
# of video frames.
#

import cv2
import numpy as np
import picam
import time, datetime
import sys
import argparse
import os
import logging

# local imports
import algo
import comm
import picam
import targets
import config

class PiVideoStream:
    def __init__(self):
        
        self.commChan = None
        self.parseArgs()

        #   logger init:
        #     - we write logging info to file, for performance this should be
        #       minimized.
        #     - during debugging, set the loglevel to debug and see the 'spew'
        #       via:  "tail -f /tmp/runPiCam.log"
        if self.args.debug:
            logLevel = logging.DEBUG
        else:
            logLevel = logging.INFO
        
        logging.basicConfig(level=logLevel,
                            format="%(asctime)s %(levelname)-6s: %(message)s",
                            datefmt="%m/%d %H:%M:%S",
                            # This file is avible to write to, even when the pi is in 'read-only' mode
                            filename="/tmp/runPiCam.log",
                            filemode="a")
        logging.info("--------------------New run------------------")
        logging.info("pid: %d" % os.getpid())
        logging.info("args: " + str(self.args))
        logging.info("opencv version: {}".format(cv2.__version__))
        logging.debug("Parsed the following args:")
        logging.debug(self.args)
        
        if self.args.robot != "none":
            if self.args.robot == "roborio":
                fmt = "%Y/%m/%d %H:%M:%S"
                logging.debug(datetime.datetime.now().strftime(fmt))
                logging.debug("Connecting to robot at 10.49.15.2...")
                ip = "10.49.15.2"
            else:
                ip = self.args.robot
            logging.info("starting comm to " + ip)
            self.commChan = comm.Comm(ip)

        # parameter configuration -----
        self.config = getattr(config, self.args.config) # reads named dict
        self.picam = picam.PiCam(self.config["picam"])
        self.algoConfig = self.config["algo"]
        # Updating config with passed commands
        # XXX: Need logic to check if these values exist in the chosen config
        #      Unsure if an error will be thrown
        # Overriding config values with passed values
        if (self.args.display):
            self.algoConfig["display"] = True

        if (self.args.algo is not None):
            self.algoConfig["algo"] = self.args.algo

        # Setting mmounting intrenssics

    def parseArgs(self):
        """2
        Parse input arguments
        """
        parser = argparse.ArgumentParser(description=
                            "Capture and process picamera stream")
        parser.add_argument("--config", dest="config",
                            help="config: default,greenled,noled...",
                            default="default")
        parser.add_argument("--threads", dest="threads",
                            help="threads: (0-4) [2]",
                            default=2, type=int)
        parser.add_argument("--algo", dest="algo",
                            help="(empty, default)",)
        parser.add_argument("--display", dest="display",
                            help="display [0,1]",
                            default=0, type=int)
        # Should robot be moved to configs?
        parser.add_argument("--robot", dest="robot",
                            help="robot (localhost, roborio) [localhost]",
                            default="localhost")
        parser.add_argument("--debug", dest="debug",
                            help="debug: [0,1] ",
                            default=0)

        self.args = parser.parse_args()

    def Run(self):
        self.processVideo()

    def processVideo(self):
        """ create a camera, continually read frames and process them.
        """
        logging.info("  (single threaded)")
        self.picam.start()
        self.picam.startThread()
        logging.debug(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        logging.debug("Began processing images")
        while True:
            # The image here is directly passed to cv2.
            startTime = comm.getCurrentTime()
            self.algoConfig["state"]["TargetPNP"].timeValue = startTime # Should be the 3rd item in the list
            self.algoConfig["state"]["TargetPID"].timeValue = startTime # Should be the 3rd item in the list


            image = self.picam.imageQueue.get()
            if self.processFrame(image):
                break

    # The end/start of the line for the stack trace 
    def processFrame(self, image):
        # Cut 'target'

        # Not to be misleading here - target is the general-purpose data
        #   we will get back from processFrame. It is NOT a target object
        target, frame = algo.processFrame(image, cfg=self.algoConfig)


        # XXX: Cut
        if self.commChan:
            
            if target is not None:

                self.commChan.UpdateVisionState("Acquired")
                
                # -== PNP version ==-
                if self.algoConfig["algo"] == "pnp":
                    
                    # PNP
                    self.algoConfig["state"]["TargetPNP"].poseValue = target
                    self.algoConfig["state"]["TargetPNP"].send()
                
                # -== PID version ==-
                if self.algoConfig["algo"] == "pid":
            
                    # PID
                    self.algoConfig["state"]["TargetPID"].valuehOffSet = target
                    self.algoConfig["state"]["TargetPID"].send()

            else:

                self.commChan.UpdateVisionState("Searching")

        # XXX: End cut

    def Shutdown(self):
        self.picam.stop()
        if self.commChan:
            self.commChan.Shutdown()

def main():
    pistream = PiVideoStream()
    pistream.Run()
    pistream.Shutdown()

if __name__ == "__main__":
    main()

