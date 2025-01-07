#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 2024

Simulation of a loudspeaker drive unit in free-air.
@author: tom
"""

from electroacPy import gtb
import numpy as np
from electroacPy import circuit
from electroacPy import csc


#%% define components
U   = csc.electric.voltageSource(1, 0, 1)
Re  = csc.electric.resistance(1, 2, 6)
Le  = csc.electric.inductance(2, 3, 0.2e-3)
Bli = csc.coupler.CCVS(3, 4, 5, 6, 7.8)
Blv = csc.coupler.CCVS(6, 0, 4, 0, -7.8)
Cms = csc.electric.capacitance(5, 7, 1.35e-3)
Mms = csc.electric.inductance(7, 8, 17.9e-3)
Rms = csc.electric.resistance(8, 0, 0.9)


#%% setup and run circuit
frequency = np.arange(10, 10000, 1)
driver = circuit(frequency)
driver.addComponent(U, Re, Le, Bli, Blv, Cms, Mms, Rms)
driver.run()


#%% extract and plot results
Ze = - driver.getPotential(1) / driver.getFlow(1)
v  = driver.getPotential(8) * Rms.Gs
            

gtb.plot.FRF(frequency, Ze, "abs", ylabel="Impedance [Ohm]", figsize=(6, 3))
gtb.plot.FRF(frequency, Ze, "phase", ylabel="Impedance [rad]", figsize=(6, 3))
gtb.plot.FRF(frequency, v*1e3, "abs", ylabel="Velocity [mm/s]", figsize=(6, 3))
