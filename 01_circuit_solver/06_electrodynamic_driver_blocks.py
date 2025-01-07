#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 16:08:40 2024

Simulation of drivers in infinite baffle.

1. Single drive unit
2. Parallel drive units
3. Series drive units

@author: tom
"""

from electroacPy import gtb
from electroacPy import csc, csb, circuit
from numpy import arange, sqrt


#%% Initialization of circuits
frequency = arange(10, 10e3, 1)
single   = circuit(frequency)
parallel = circuit(frequency)
series   = circuit(frequency)


#%% driver parameters
Re  = 6
Le  = 0.2e-3
Cms = 1.35e-3
Mms = 17.9e-3
Rms = 0.9
Bl  = 7.8
Sd  = 158e-4


#%% Estimate input voltage to get 1W of power
U_single   = sqrt(Re)
U_parallel = sqrt(Re/2)
U_series   = sqrt(Re*2)

#%% 1. single driver
Vs    = csc.electric.voltageSource(1, 0, U_single)
ead_1 = csb.electrodynamic.EAD(1, 0, 2, 0, Le, Re, Cms, Mms, Rms, Bl, Sd, v_probe="v")
rad_1 = csc.acoustic.radiator(2, 0, Sd)
single.addBlock(ead_1)
single.addComponent(Vs, rad_1)

#%% 2. parallel drivers
Vs    = csc.electric.voltageSource(1, 0, U_parallel)
ead_1 = csb.electrodynamic.EAD(1, 0, 2, 0, Le, Re, Cms, Mms, Rms, Bl, Sd, v_probe="v")
rad_1 = csc.acoustic.radiator(2, 0, Sd)
ead_2 = csb.electrodynamic.EAD(1, 0, 3, 0, Le, Re, Cms, Mms, Rms, Bl, Sd)
rad_2 = csc.acoustic.radiator(3, 0, Sd)
parallel.addBlock(ead_1, ead_2)
parallel.addComponent(Vs, rad_1, rad_2)


#%% 3. Series drivers
Vs    = csc.electric.voltageSource(1, 0, U_series)
ead_1 = csb.electrodynamic.EAD(1, 2, 3, 0, Le, Re, Cms, Mms, Rms, Bl, Sd, v_probe="v")
rad_1 = csc.acoustic.radiator(3, 0, Sd)
ead_2 = csb.electrodynamic.EAD(2, 0, 4, 0, Le, Re, Cms, Mms, Rms, Bl, Sd)
rad_2 =  csc.acoustic.radiator(4, 0, Sd)
series.addBlock(ead_1, ead_2)
series.addComponent(Vs, rad_1, rad_2)


#%% run simulations
single.run()
parallel.run()
series.run()


#%% plot driver velocities
Z_single   = -single.getPotential(1) / single.getFlow(1)
Z_parallel = -parallel.getPotential(1) / parallel.getFlow(1)
Z_series   = -series.getPotential(1) / series.getFlow(1)

v_single   = single.getFlow("v")   * 1e3   
v_parallel = parallel.getFlow("v") * 1e3
v_series   = series.getFlow("v")   * 1e3

gtb.plot.FRF(frequency, (Z_single, Z_parallel, Z_series), "abs",
             legend=("single", "parallel", "series"),
             ylabel="Impedance [Ohm]", figsize=(6, 3))

gtb.plot.FRF(frequency, (v_single, v_parallel, v_series), "abs",
             legend=("single", "parallel", "series"),
             ylabel="Velocity [mm/s]", figsize=(6, 3))


