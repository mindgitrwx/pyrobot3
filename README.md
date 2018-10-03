# Pyrobot README File
----------------

It was successfully tested on **Ubuntu 18.04**. 

Following steps are the successful case step. 


### 1. First just clone this project and change this folder name as pyrobot3 -> pyrobot `mv pyrobot3 pyrobot`

### 2. `cd /pyrobot/bin/` and `python3 pyrobot` 

### 3. Click Server: and choose PyrobotSimulator and choose Tutorial.py as a World. You should get a window showing a top view of a simulated room containing a robot and a few walls.

### 4. In the interface window, click Robot: and choose PyrobotRobot60000.py

### 5. Click Brain: and choose Avoid.py

### 6. Click Run to make the robot wander around the simulated room

# Combination of available robot

----------------

|---------------+--------------+-----------------|
| world         | robot        | plugin          |
|---------------+--------------+-----------------|
| AndrewHallway | pyrobot60000 | Subsumption.py  |
| AndrewHallway | pyrobot60000 | Slider.py       |
| AndrewHallway | pyrobot60000 | SimpleWander.py |
| AndrewHallway | pyrobot60000 | SimpleBrain.py  |
| AndrewHallway | pyrobot60000 | Subsumption     |
| AndrewHallway | pyrobot60000 | Subsumption     |
| AndrewHallway | pyrobot60000 | Subsumption     |
| AndrewHallway | pyrobot60000 | Subsumption     |
|---------------+--------------+-----------------|

<!--
   - pyrobot60000 ./plugins/worlds/Pyrobot/AndrewHallway.py 
   - pyrobot60000 ./plugins/brains/Subsumption.py 
   - pyrobot60000 ./plugins/brains/Slider.py
   - pyrobot60000 ./plugins/brains/SimpleWander.py
   - pyrobot60000 ./plugins/brains/SimpleBrain.py
   - pyrobot60000 ./plugins/brains/SimpleBrain.py
   - pyrobot60000
   - ./plugins/worlds/Pyrobot/KonaneWorld.py
   -->


