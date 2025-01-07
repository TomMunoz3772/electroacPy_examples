#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 2024

@author: tom
"""

from electroacPy import gtb
from numpy import arange
from electroacPy import csc, csb, circuit

frequency = arange(10, 10e3, 1)
cir = circuit(frequency)


#%% Source + crossovers
Vs  = csc.electric.voltageSource(1, 0, 2.83)
lp1 = csb.electric.lowpass_butter(1, 2, order=3, fc=300, Re=8)
hp1 = csb.electric.highpass_butter(1, 3, order=3, fc=300, Re=4)


#%% Electric load
Re8 = csc.electric.resistance(2, 0, 8)
Re4 = csc.electric.resistance(3, 0, 4)


#%% setup and run 
cir.addBlock(lp1, hp1)
cir.addComponent(Vs, Re8, Re4)
cir.run()


#%% extract FRF
H_lp = cir.getPotential(2) / cir.getPotential(1)  
H_hp = cir.getPotential(3) / cir.getPotential(1) 

gtb.plot.FRF(frequency, (H_lp, H_hp, H_lp+H_hp), "dB",
             legend=("H_lp", "H_hp", "sum"),
             ylim=(-20, 3), figsize=(6, 3))
