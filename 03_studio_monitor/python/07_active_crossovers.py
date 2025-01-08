#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 12:52:03 2024

Post-processing results with biquads.

@author: tom
"""

import numpy as np
import electroacPy as ep
from electroacPy import gtb # same as import electroacPy.general as gtb

system = ep.load("06_acoustic_radiation")

#%% LF filter
system.filter_network("LF_xover", ref2bem=[1, 2], ref2study="free-field")
system.filter_addLowPassBQ("LF_xover", "lf1", 300, 0.5)

#%% MF Filter
system.filter_network("MF_xover", ref2bem=3, ref2study="free-field")
system.filter_addHighPassBQ("MF_xover", "hp1", 300, 0.5)
system.filter_addLowPassBQ("MF_xover", "lp1", 3500, 0.5)
system.filter_addGain("MF_xover", "db", -2)
system.filter_addPhaseFlip("MF_xover", "pi")

#%% HF Filter
system.filter_network("HF_xover", ref2bem=4, ref2study="free-field")
system.filter_addHighPassBQ("HF_xover", "hp1", 3500, 0.5, dBGain=-4)


#%% plot results with filters
system.plot_results("free-field", "polar_hor")
system.plot_results("free-field", "polar_ver")


#%% Transfer functions
H_lf = system.crossover["LF_xover"].h
H_mf = system.crossover["MF_xover"].h
H_hf = system.crossover["HF_xover"].h

gtb.plot.FRF(system.frequency, (H_lf, H_mf, H_hf, H_lf+H_mf+H_hf), 
             legend=("LF", "MF", "HF", "total"), transformation="dB",
             ylim=(-30, 10), xlim=(10, 10000), figsize=(6, 3),
             xticks=(10, 20, 50, 
                     100, 200, 500, 
                     1000, 2000, 5000, 10000),
             yticks=np.arange(-30, 12, 6))


#%% extract individual radiator
p_lf   = system.get_pMic("free-field", "polar_hor", radiatingElement=1)
p_port = system.get_pMic("free-field", "polar_hor", radiatingElement=2)
p_mf   = system.get_pMic("free-field", "polar_hor", radiatingElement=3)
p_hf   = system.get_pMic("free-field", "polar_hor", radiatingElement=4)
p_tot  = system.get_pMic("free-field", "polar_hor")


gtb.plot.FRF(system.frequency, (p_lf[:, 73//2], 
                                p_port[:, 73//2],
                                p_mf[:, 73//2],
                                p_hf[:, 73//2],
                                p_tot[:, 73//2]), 
             ylabel="SPL [dB]",
             legend=("woofer", "port", "midrange", "tweeter", 
                     "total contribution"),
             xlim=(10, 10e3), ylim=(35, 80), figsize=(6, 3))

gtb.plot.FRF(system.frequency, (p_lf[:, 73//2], 
                                p_port[:, 73//2],
                                p_mf[:, 73//2],
                                p_hf[:, 73//2],
                                p_tot[:, 73//2]), 
             transformation="phase",
             legend=("woofer", "port", "midrange", "tweeter", 
                     "total contribution"),
             xlim=(10, 10e3), figsize=(6, 3))



