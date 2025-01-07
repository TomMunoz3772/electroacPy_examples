#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 17:20:46 2024

@author: tom
"""

import electroacPy as ep
from electroacPy import gtb
 
#%% LEM
# frequency axis and system initialization
frequency = gtb.freqop.freq_log10(10, 1e3, 50)
monitor = ep.loudspeakerSystem(frequency)

# Load drivers
monitor.lem_driverImport("SB34", "../technical_data/SB SB34NRXL75-8.txt")
monitor.lem_driverImport("MR16", "../technical_data/SB MR16PNW-8.txt")
monitor.lem_driverImport("TW29", "../technical_data/TW29RN-B.txt", ref2bem=4)

# Define ported enclosure
monitor.lem_enclosure("ported_LF", 40e-3, 
                     Lp=35e-2, Sp=78.6e-4,
                     ref2bem=[1, 2], 
                     setDriver="SB34")

monitor.lem_enclosure("sealed_MF", 5.1e-3,
                     ref2bem=3, setDriver="MR16")


#%% BEM
# Define free-field study
monitor.study_acousticBEM("free-field", 
                         "../geo/mesh/studio_monitor_refined_netgen.med", 
                         ["ported_LF", "TW29", "sealed_MF"])

# Define Evaluations
monitor.evaluation_polarRadiation("free-field", "polar_hor", 
                                 -180, 180, 5, on_axis="x", direction="y",
                                 radius=2, offset=[0, 0, 0.193])

monitor.evaluation_polarRadiation("free-field", "polar_ver", 
                                -180, 180, 5,  "x", "z", 
                                radius=2, offset=[0, 0, 0.193])

monitor.evaluation_pressureField("free-field", "field_ver", 
                                L1=3, L2=2, step=343/2500/6, 
                                plane="xz", offset=[-1.5, 0, -1])

monitor.evaluation_pressureField("free-field", "field_hor", 
                                L1=3, L2=2, step=343/2500/6, 
                                plane="xy", offset=[-1.5, -1, 0.193])

# plot study to check that everything is OK
monitor.plot_system("free-field")

# run boundary operators
monitor.run()

# save state
# ep.save("09_Studio_Monitor", monitor)

monitor.plot_results()


