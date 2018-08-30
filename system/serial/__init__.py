#!/usr/bin/env python 
#portable serial port access with python
#this is a wrapper module for different platform implementations
#
# (C)2001-2002 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

import sys, os, string
VERSION = str.split("$Revision: 1.1 $")[1]     #extract CVS version

#chose an implementation, depending on os
if os.name == 'posix':
    from pyrobot.system.serial.serialposix import *
elif os.name == 'java':
    from pyrobot.system.serial.serialjava import *
else:
    raise Exception("Sorry no implementation for your platform available.")

#no "mac" implementation. someone want's to write it? i have no access to a mac.
