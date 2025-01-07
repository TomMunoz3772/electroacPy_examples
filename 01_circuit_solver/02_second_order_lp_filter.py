#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 11:26:59 2024

Second order low-pass filter.

     1  i        2    
     o-->---L----o----o--- Vout
     |           |    |
    Vin          C    R
     |           |    |
     o-----------o----o
     0

@author: tom
"""

from electroacPy import gtb
from numpy import pi, arange
from electroacPy import csc
from electroacPy import circuit


frequency = arange(10, 10e3, 1)
LP = circuit(frequency)

#%% Definition of components and cut-off frequency
# Low pass for a loudspeaker with nominal impedance of 8 Ohm
f0 = 1000
w0 = 2*pi*f0
Re = 8
L  = Re / w0
C  = 1 / w0 / Re

#%% Create network
Vs = csc.electric.voltageSource(1, 0, 2.83)
L1 = csc.electric.inductance(1, 2, 2*L)
C1 = csc.electric.capacitance(2, 0, 0.5*C)
R  = csc.electric.resistance(2, 0, Re)

LP.addComponent(Vs, L1, C1, R)
LP.run()

#%% Plot data
H = LP.getPotential(2) / LP.getPotential(1)

gtb.plot.FRF(frequency, H, "dB", ylim=(-20, 3),
             title="Transfer function",
             ylabel="P_out / P_in [dB]")



