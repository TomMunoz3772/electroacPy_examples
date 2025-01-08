#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 13:45:49 2024

This example shows how to link drivers to enclosure for simulating in sealed 
and ported configurations.

@author: tom
"""

import electroacPy as ep

#%% Load previous state
system = ep.load("01_driver_import")

#%% Define ported enclosure
system.lem_enclosure("ported_LF", 40e-3, 
                     Lp=35e-2, Sp=78.6e-4, Qab=120, Qal=30,
                     ref2bem=[1, 2], 
                     setDriver="SB34", Nd=1,
                     wiring="parallel")

system.lem_enclosure("sealed_MF", 5.1e-3,
                     ref2bem=3, setDriver="MR16")

#%% plot data
system.enclosure["ported_LF"].plotZe()
system.enclosure["ported_LF"].plotXVA()

#%% save current data
ep.save("02_enclosure", system)







