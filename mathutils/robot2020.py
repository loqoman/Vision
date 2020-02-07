from robot import *
from vec import *

class Robot2020(Robot):
    """
    # Vision's goal is to identify landmarks as seen by the camera (ie in 
    # camera space) then to convey the location of the landmark to the robot 
    # code expressed in field coords. It's possible that the camera will be 
    # mounted atop a moving turret.
    #
    # hence: we want camera-to-turret-to-robot-to-field transformation!
    #
    # summary:  
    #   cameraToMount (take origin of camera into mount space )
    #       we may mount on turret or on robot
    #   turretToRobot  (take origin of turret into robot space)
    #   robotToField   (take origin of robot into field space)
    #   cameraToField (take origin of camera into field space)
    #
    #  camera coordinates (ie: looking out the camera, cf poseEstimation.py)
    #    x is right, y is down, z it into the screen
    #       
    #  cameraToMount:  assume that the camera is mounted on turret, C below.
    #  If we decide that we want a fixed camera, we can skip to the next step.
    #  
    # 
    #            , - ~ ~ 
    #     , '               ' ,
    #   ,           x           ,
    #  ,            |      -z    ,
    # ,             |       |     ,
    # ,     y-------o       C--x  ,   # at C, y is towards viewer
    # ,                           ,
    #  ,                         ,
    #   ,                       ,
    #     ,                  , '
    #       ' - , _ _ _ ,  '
    #
    # see: https://www.mecademic.com/resources/Euler-angles/Euler-angles
    # tinkertoy trick: 
    #     * place coords on paper matching target config
    #     * camFlips: find the two rotations needed to cause coords to match camera
    #       (90, -90, 0, "rxyz")
    >>> TiltAngle = 45 # extreme example
    >>> camTilt = Affine3.fromRotation(TiltAngle, [1, 0, 0]) # tilt round camera x
    >>> camFlips = Affine3.fromEulerAngles(90, -90, 0, "rxyz") 
    >>> camRot = Affine3.concatenate(camFlips, camTilt)
    >>> camRotQ = camRot.asQuaternion() # acquire compact rep
    >>> camRotQ.equals([0.27059805, 0.65328148, -0.65328148, -0.27059805])
    True
    >>> camOffset = Affine3.fromTranslation(0, -12, 8)
    >>> d = camFlips.transformBases() # x, y, z axes in camera
    >>> np.allclose([[0,-1,0], [0,0,1], [-1,0,0]], d) # axes in camera mountspace
    True
    >>> camToMount = Affine3.concatenate(camOffset, camRot)
    >>> o = camToMount.transformPoints([[0,0,0]])
    >>> np.allclose(o[0], [0, -12, 8])
    True
    >>> mountToCamera = camToMount.asInverse()
    >>> o = mountToCamera.transformPoints([[0,-12,8]]) 
    >>> np.allclose(o[0], [0,0,0]) # verifies this is camspace origin
    True
    >>>
    >>> camTgt = [0, 0, -120] # target is center of camera 12 ft away
    >>> tgt = camToMount.transformVectors([camTgt])
    >>> np.allclose(120, Vec3.length(tgt[0]))
    True

    # 
    # Robot coords (z is up)    
    #                           
    #           y               
    #       .___|___.          
    # Back  |   |   |  Front      
    #    x---T  o-----x      turret points opposite robot front, aim-angle
    #       ||______|        varies according to targeting requirements
    #        y             
    #

    >>> t2rRot = Affine3.fromRotation(180, [0,0,1])
    >>> t2rOffset = Affine3.fromTranslation(-15, -5, 0) # turret origin offset from robot origin
    >>> turretToRobot = Affine3.concatenate(t2rOffset, t2rRot)
    >>> dirs = turretToRobot.transformBases()
    >>> np.allclose(dirs, [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    True
    >>> pts = turretToRobot.transformPoints([[0, 0, 0]])
    >>> np.allclose(pts[0], [-15, -5, 0])
    True

    #
    # field coords (z is up)
    # field is approx x: [0, 52*12], y: [-26*12, 26*12] (z is up)
    #
    #                       y
    #                 ._____|____. 
    #  Blue Alliance  |     |    |  Red Alliance
    #                 |     o-----x
    #                 |__________| 
    #
    # Test
    # 1. place robot on the field at a heading of -20 degrees, at 150, 150, 
    #     robot center is 8 inches off the ground
    >>> robotToField = Affine3.fromTranslation(150, 150, 8).rotate(-20, [0, 0, 1])
    >>> pts = robotToField.transformPoints([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    >>> np.allclose(pts[0], [150, 150, 8])
    True

    # 2. verify field orientation of robot x axis
    >>> ndirs = robotToField.transformVectors([[1, 0, 0]])
    >>> angle = math.degrees(math.atan2(ndirs[0][1], ndirs[0][0]))
    >>> np.allclose(angle, -20)
    True

    >>> r = Robot2020()
    >>> o = camOffset.decompose()[3]  # fourth field of decomposition
    >>> off = "%f %f %f " % (o[0], o[1], o[2])
    >>> r.setCameraPose(off + str(camRotQ))
    >>> r.updateRobotPose("150 150 20", 0)

    """

    def __init__(self):
        super().__init__()
    

if __name__ == "__main__":
    import doctest
    import math
    import numpy as np
    doctest.testmod()