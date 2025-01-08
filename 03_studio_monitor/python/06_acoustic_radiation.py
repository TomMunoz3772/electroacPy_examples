#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:39:49 2024

Recap of the acoustic radiation evaluation --- free-field only.

@author: tom
"""

import electroacPy as ep

#%% load data
system = ep.load("03_LEM_Recap")

#%% Define free-field study
system.study_acousticBEM("free-field", 
                         "../geo/mesh/studio_monitor.msh",
                         ["ported_LF", "TW29", "sealed_MF"], domain="exterior")

## Free-field only
system.evaluation_polarRadiation("free-field", "polar_hor", 
                                 -180, 180, 5, "x", "y",
                                 radius=2, offset=[0, 0, 0.193])
system.evaluation_pressureField("free-field", "field_ver", 
                                3, 2, 343/2500/6, "xz", offset=[-1.5, 0, -1])
system.evaluation_pressureField("free-field", "field_hor", 
                                3, 2, 343/2500/6, "xy", 
                                offset=[-1.5, -1, 0.193])
system.evaluation_polarRadiation("free-field", "polar_ver", 
                                -180, 180, 5,  "x", "z", 
                                radius=2, offset=[0, 0, 0.193])

system.plot_system("free-field")


#%% run potential operators and plot results
system.run()
system.plot_results()

#%% save state
ep.save("06_acoustic_radiation", system)

#%% export data - uncomment the following to export data as .txt file

# system.export_directivity("directivity_export/woofer", "woofer_hor", "free-field", 
#                           "polar_hor", [1, 2], bypass_xover=True)
# system.export_directivity("directivity_export/woofer", "woofer_ver", "free-field", 
#                           "polar_ver", [1, 2], bypass_xover=True)
# system.export_impedance("impedance_export", "Z_ported_woofer", "ported_LF")

# system.export_directivity("directivity_export/midrange", "midrange_hor", "free-field", 
#                           "polar_hor", 3, bypass_xover=True)
# system.export_directivity("directivity_export/midrange", "midrange_ver", "free-field", 
#                           "polar_ver", 3, bypass_xover=True)
# system.export_impedance("impedance_export", "Z_sealed_midrange", "sealed_MF")

# system.export_directivity("directivity_export/tweeter", "tweeter_hor", "free-field", 
#                           "polar_hor", 4, bypass_xover=True)
# system.export_directivity("directivity_export/tweeter", "tweeter_ver", "free-field", 
#                           "polar_ver", 4, bypass_xover=True)
# system.export_impedance("impedance_export", "Z_tweeter", "TW29")



