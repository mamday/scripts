#!/usr/bin/env python

import icecube
from icecube import icetray, dataclasses, dataio, phys_services, PulseCore
from I3Tray import *

tray = I3Tray()

tray.Add('I3Reader',FilenameList=[sys.argv[1],sys.argv[2]])
#Test Module
tray.Add('PulseCore', 
         InputPulses='OfflinePulses')
#         Outputname='TestPulses')

tray.Add('I3Writer',filename=sys.argv[3])

tray.Execute()
