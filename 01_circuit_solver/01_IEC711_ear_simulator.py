#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 11:26:59 2024

Simulation of a IEC711 ear simulator.

@author: tom
"""

from electroacPy import gtb
from numpy import arange
from electroacPy.circuitSolver.solver import circuit
from electroacPy.circuitSolver.components.electric import (resistance,
                                                           inductance,
                                                           capacitance,
                                                           voltageSource)

#%% component values
Ps = 1
Ma4 = 82.9
Ca4 = 0.943e-12
Ra5 = 50.6e6
Ma5 = 9.4e3
Ca5 = 1.9e-12
Ma6 = 130.3
Ca6 = 1.479e-12
Ra7 = 31.1e6
Ma7 = 983.8
Ca7 = 2.1e-12
Ma8 = 133.4
Ca8 = 1.517e-12


#%% define circuit elements
p1 = voltageSource(1, 0, Ps)
MA4 = inductance(1, 2, Ma4)
CA4 = capacitance(2, 0, Ca4)

RA5 = resistance(2, 3, Ra5)
MA5 = inductance(3, 4, Ma5)
CA5 = capacitance(4, 0, Ca5)

MA6 = inductance(2, 5, Ma6)
CA6 = capacitance(5, 0, Ca6)

RA7 = resistance(5, 6, Ra7)
MA7 = inductance(6, 7, Ma7)
CA7 = capacitance(7, 0, Ca7)

MA8 = inductance(5, 8, Ma8)
CA8 = capacitance(8, 0, Ca8)

# microphone
# CMIC = capacitance(8, 9, 0.62e-13)
# RMIC = resistance(9, 10, 119e6)
# MMIC = inductance(10, 0, 710)


#%% Build circuit
freq = arange(100, 20e3, 0.5)
iec711 = circuit(freq)
iec711.addComponent(p1, MA4, CA4, 
                    RA5, MA5, CA5,
                    MA6, CA6, 
                    RA7, MA7, CA7, 
                    MA8, CA8)
iec711.run()


#%% Plot
p8 = iec711.getPotential(8)
i8 = p8 * CA8.Gs
i1 =  iec711.getFlow(1)

gtb.plot.FRF(freq, p8/i1, "dB", title="Transfer impedance")
gtb.plot.FRF(freq, i8/i1, "dB", title="Volume velocity gain")





