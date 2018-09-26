"""
A PyrobotSimulator world. A large room with two robots and
two lights.

(c) 2005, PyroRobotics.org. Licensed under the GNU GPL.
"""

from pyrobot.simulators.pysim import *

def INIT():
    # (width, height), (offset x, offset y), scale:
    #sim = TkSimulator((443,466), (22,420), 40.357554)
    sim = TkSimulator((443,466), (22,420), 10.357554)
    # x1, y1, x2, y2 in meters:
    sim.addBox(0, 0, 10, 10)

    sim.addBox(10, 10, 20, 20)
    sim.addBox(10, 20, 20, 30)
    sim.addBox(10, 30, 20, 40)
    sim.addBox(10, 40, 20, 50)
    sim.addBox(10, 50, 20, 60)
    # port, name, x, y, th, bounding Xs, bounding Ys, color
    # (optional TK color name):
    sim.addRobot(60000, TkPioneer("RedPioneer",
                                  4.99, 1.32, 6.28,
                                  ((.225, .225, -.225, -.225),
                                   (.175, -.175, -.175, .175)),
                                  "red"))

    sim.addRobot(60001, TkPioneer("BluePioneer",
                                  4.99, 1.32, 6.28,
                                  ((.225, .225, -.225, -.225),
                                   (.175, -.175, -.175, .175)),
                                  "blue"))

    # add some sensors:
    sim.robots[0].addDevice(PioneerFrontSonars())
    sim.robots[1].addDevice(PioneerFrontSonars())
    return sim
