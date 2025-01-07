#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 09:23:53 2024

This example shows how to load LPM data and add corresponding driver object 
to the system under study

@author: tom
"""

import electroacPy as ep
import numpy as np

#%% frequency axis and system initialization
frequency = np.arange(10, 10000, 1)
system = ep.loudspeakerSystem(frequency)

#%% Woofer import
Re = 6.2        # Ohm
Le = 1.2e-3     # H
Bl = 16         # T.m
Mms = 84.9e-3   # kg
Cms = 560e-6    # m/N
Rms = 2.35      # kg/s
Sd = 508e-4     # m^2
system.lem_driver("SB34", 1, Le, Re, Cms, Mms, Rms, Bl, Sd)

#%% Midrange import
system.lem_driverImport("MR16", "../technical_data/SB MR16PNW-8.txt")

#%% Tweeter import (through T/S file)
system.lem_driverImport("TW29", "../technical_data/TW29RN-B.txt")

#%% Save data
ep.save("01_driver_import", system)
