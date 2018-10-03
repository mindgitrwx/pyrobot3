# A bare brain

from pyrobot.brain import Brain

from pyrobot.brain.fuzzy import *
from pyrobot.brain.behaviors import *
from pyrobot.brain.behaviors.core import *  # Stop

import math
from random import random

class Avoid(Behavior):
   # Only method you have to define is the step method:

   def setup(self):
      self.Effects('translate', .1)
      self.Effects('rotate', .1)
      self.lasttime = time.mktime(time.localtime())
      self.count = 0
      # create any vars you need here
      pass

   def step(self):
      #self.robot.move(0, -.2) # negative is to the right!
      pass

   def update(self):
      if self.count == 50:
          currtime = time.time()
          self.count = 0
          self.lasttime =  time.time()
      else:
          self.count += 1
      close_dist, angle = min( [(s.distance(), s.angle(unit="radians")) for s in self.robot.range["front-all"]])
      max_sensitive = self.robot.range.getMaxvalue() * 0.8
      self.IF(Fuzzy(0.1, max_sensitive) << close_dist, 'translate', 0.0, "TooClose")
      self.IF(Fuzzy(0.1, max_sensitive) >> close_dist, 'translate', 0.3, "Ok")
      #  self.IF(Fuzzy(0.1, max_sensitive) << close_dist, 'rotate', self.direction(angle), "TooClose")
# -------------------------------------------------------
# This is the interface for calling from the gui engine.
# Takes one param (the robot), and returns a Brain object:
# -------------------------------------------------------
class state1 (State):
    def setup(self):
        self.add(Avoid(1))
        print(("initialized state", self.name))

    def onActivate(self):
        self.count = 0

    def update(self):
        print("State 1")
        if self.count == 0:
            self.goto("state2")
        else:
            self.count += 1

class state2 (State):
    def setup(self):
        self.add(StopBehavior(1))
        print(("initialized state", self.name))

    def update(self):
        print("State 2")
        self.goto("TurnAround")

class TurnAround(State):
    def update(self):
        if min([s.distance() for s in self.robot.range["front-all"]]) < 1.0:
            self.move(0, .2)
        else:
            self.goto("state1")


def INIT(engine):
    SimpleBrain = BehaviorBasedBrain({'translate' : engine.robot.translate, \
                                'rotate' : engine.robot.rotate, \
                                'update' : engine.robot.update }, engine)

    # add a few states:
    SimpleBrain.add(state1()) # non active
    SimpleBrain.add(state2()) # non active
    SimpleBrain.add(TurnAround()) # non active

    # activate a state:
    SimpleBrain.activate('state1') # could have made it active in constructor


    return SimpleBrain


#  # A bare brain

#  from pyrobot.brain import Brain

#  class SimpleBrain(Brain):
   #  # Only method you have to define is the step method:

   #  def setup(self):
      #  # create any vars you need here
      #  pass

   #  def step(self):
      #  #self.robot.move(0, -.2) # negative is to the right!
      #  pass

#  # -------------------------------------------------------
#  # This is the interface for calling from the gui engine.
#  # Takes one param (the robot), and returns a Brain object:
#  # -------------------------------------------------------

#  def INIT(engine):
   #  return SimpleBrain("SimpleBrain", engine)


