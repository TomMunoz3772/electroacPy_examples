#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 13:58:03 2024

@author: tom
"""

import electroacPy as ep
import electroacPy.general as gtb


#%% frequency axis and system initialization
frequency = gtb.freqop.freq_log10(10, 10e3, 125)
system = ep.loudspeakerSystem(frequency)

#%% Load drivers
system.lem_driverImport("SB34", "../technical_data/SB SB34NRXL75-8.txt")
system.lem_driverImport("MR16", "../technical_data/SB MR16PNW-8.txt")
system.lem_driverImport("TW29", "../technical_data/TW29RN-B.txt", ref2bem=4)

#%% Define ported enclosure
system.lem_enclosure("ported_LF", 40e-3, 
                     Lp=35e-2, Sp=78.6e-4, Qab=120, Qal=30,
                     ref2bem=[1, 2], 
                     setDriver="SB34", Nd=1,
                     wiring="parallel")

system.lem_enclosure("sealed_MF", 5.1e-3,
                     ref2bem=3, setDriver="MR16")

#%% save state
ep.save("03_LEM_Recap", system)
