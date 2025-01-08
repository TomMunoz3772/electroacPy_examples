#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 19:50:25 2024

Simulation of sound transmission within a duct through a membrane.

    ---------------------------------//
    |                  (            |//
    |-->v              |            |// rigid termination
    |                  (            |//
    ---------------------------------//
 piston             membrane
 
@author: tom
"""

from electroacPy import csc
from electroacPy import circuit
from electroacPy import gtb
from numpy import arange, pi


#%% Define study parameters
frequency = arange(10, 10000, 1) 
Lp1 = 0.05
Lp2 = 0.1
rp = 0.01
Sp = pi*rp**2


#%% Initialize components
Is       = csc.electric.currentSource(1, 0, 1)
line1    = csc.acoustic.open_line_T(1, 2, 3, 0, Lp1, Sp)
membrane = csc.acoustic.membrane(3, 4, 200e-6, 3e-3, 0.12, Sp)
line2    = csc.acoustic.closed_line(4, 0, Lp2, Sp)


#%% Assemble circuit
cir = circuit(frequency)
cir.addComponent(Is, line1, membrane, line2)
cir.run()

#%% Extract potentials and currents
p_out = cir.getPotential(4)
p_in = cir.getPotential(1)
p_m  = cir.getPotential(3)
H = p_out/p_in
v_m = (p_m - p_out) * membrane.Gs


#%% Plot
gtb.plot.FRF(frequency, (p_in, p_out), "dB", legend=("p_in", "p_out"))
gtb.plot.FRF(frequency, H, "dB", ylabel="p_out / p_in")
gtb.plot.FRF(frequency, v_m, "dB", ylabel="Volume velocity [dB]")

