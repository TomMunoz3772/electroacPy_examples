#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 10:51:11 2024

@author: tom
"""

import numpy as np
import electroacPy as ep
from electroacPy import csc, csb
from electroacPy import circuit
from electroacPy import gtb

inductance = csc.electric.inductance
resistance = csc.electric.resistance
capacitance = csc.electric.capacitance
EAD = csb.electrodynamic.EADImport
cavity = csc.acoustic.cavity
port = csc.acoustic.port
radiator = csc.acoustic.radiator


#%% load radiation data
system = ep.load("06_acoustic_radiation")
frequency = system.frequency

#%% get LPM data
lpm_woofer = "../technical_data/SB SB34NRXL75-8.txt"
lpm_midrange = "../technical_data/SB MR16PNW-8.txt"
lpm_tweeter = "../technical_data/TW29RN-B.txt"

#%% create circuit from VituixCAD network
sV = csc.electric.voltageSource(1, 0, 20)

# LF filter
L1 = inductance(1, 2, 3.3e-3)
C1 = capacitance(2, 3, 33e-6)
R1 = resistance(3, 0, 6.8)

# LF driver + acoustic
LF      = EAD(2, 0, "A", "B", lpm_woofer, "v_lf")
rad_lf  = radiator("A", 0, LF.Sd)
box_lf  = cavity("B", 0, 40e-3)
prt     = port("B", "C", 35e-2, 5e-2)
rad_prt = radiator("C", 0, 2*np.pi*(5e-2)**2)

# MF filter
C2 = capacitance(1, 4, 43e-6)
L2 = inductance(4, 5, 560e-6)
L3 = inductance(5, 0, 6.6e-3)
C3 = capacitance(5, 0, 3.66e-6)
L4 = inductance(5, 6, 6.8e-3)
C4 = capacitance(6, 7, 390e-6)
R2 = resistance(7, 0, 5.6)
C5 = capacitance(5, 8, 3.3e-6)
R3 = resistance(8, 0, 6.8)
R4 = resistance(5, 9, 1.28)
R5 = resistance(9, 0, 24)

# MF driver + acoustic
MF     = EAD(0, 9, "D", "E", lpm_midrange, "v_mf")
rad_mf = radiator("D", 0, MF.Sd)
box_mf = cavity("E", 0, 5.1e-3)

# HF filter
C6 = capacitance(1, 10, 14.4e-6)
C7 = capacitance(10, 11, 126e-6)
L5 = inductance(11, 12, 0.4e-3)
R6 = resistance(12, 0, 3.3)
R7 = resistance(10, 13, 0.6)
R8 = resistance(13, 0, 11.5)

# HF driver + acoustic
HF = EAD(13, 0, "F", 0, lpm_tweeter, "v_hf")
rad_hf = radiator("F", 0, HF.Sd)

#%% Assemble circuit
# frequency = gtb.freqop.freq_log10(10, 10e3, 125)
network = circuit(frequency)
network.addComponent(L1, L2, L3, L4, L5, 
                     C1, C2, C3, C4, C5, C6, C7,
                     R1, R2, R3, R4, R5, R6, R7, R8, 
                     sV,
                     rad_lf, box_lf, prt, rad_prt,
                     rad_mf, box_mf,
                     rad_hf)
network.addBlock(LF, MF, HF)
network.run()

#%% extract data
Zin = network.getPotential(1) / -network.getFlow(1)
v_lf = network.getFlow("v_lf")
v_mf = network.getFlow("v_mf")
v_hf = network.getFlow("v_hf")
v_p  = network.getPotential("C") * rad_prt.Gs / rad_prt.Sd

# filter transfer function (to be used in a filter network)
H_lf = network.getPotential(2) / network.getPotential(1)
H_mf = network.getPotential(9) / network.getPotential(1)
H_hf = network.getPotential(13) / network.getPotential(1)

#%% plot data
gtb.plot.FRF(frequency, Zin, "abs", ylabel="Impedance modulus [Ohm]")
gtb.plot.FRF(frequency, (v_lf, v_mf, v_hf), "abs",
             legend=("LF", "MF", "HF"), title="membrane velocity",
             ylabel="Membrane velocity [m/s]")

gtb.plot.FRF(frequency, (H_lf, H_mf, H_hf, H_lf-H_mf+H_hf), "dB", 
             legend=("LF", "MF", "HF", "total"), title="filters transfer function",
             ylabel="H [dB]", ylim=(-20, 10), xlim=(10, 10e3))

gtb.plot.FRF(frequency, (H_lf, H_mf, H_hf, H_lf-H_mf+H_hf), "phase", 
             legend=("LF", "MF", "HF", "total"))

#%% Apply to previously saved data
system.filter_network("LF_xover", ref2bem=[1, 2], ref2study="free-field")
system.filter_addTransferFunction("LF_xover", "hlf", H_lf)
# system.filter_addDelay("LF_xover", "dt", 0.29e-3)

system.filter_network("MF_xover", ref2bem=3, ref2study="free-field")
system.filter_addTransferFunction("MF_xover", "hmf", -H_mf)  # "-" to reverse phase 

system.filter_network("HF_xover", ref2bem=4, ref2study="free-field")
system.filter_addTransferFunction("HF_xover", "hhf", H_hf)

system.plot_results("free-field", "polar_hor")
system.plot_results("free-field", "polar_ver")
