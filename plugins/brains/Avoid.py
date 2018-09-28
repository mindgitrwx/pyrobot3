# robot goes forward and then slows to a stop when it detects something

from pyrobot.brain import Brain

class Avoid(Brain):

   # Give the front two sensors, decide the next move
   def determineMove(self, front, left, right):
      if front < 0.91:
         #print "obstacle ahead, hard turn"
         return(0.4, 5.0)
      elif left < 0.9:
         #print "object detected on left, slow turn"
         return(0.5, 1.0)
      elif right < 0.9:
         #print "object detected on right, slow turn"
         return(0.1, 6.0)
      else:
         #print "clear"
         return(0.5, 5.0)

