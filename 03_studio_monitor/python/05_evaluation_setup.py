#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 14:53:00 2024

Setup of evaluations.

@author: tom
"""

import electroacPy as ep

#%% load data
system = ep.load("04_BEM_setup")

#%% Define evaluations
system.evaluation_polarRadiation(["free-field", "inf_ground"], "polar_hor", 
                                 -180, 180, 5, on_axis="x", direction="y",
                                 radius=2, offset=[0, 0, 0.193])

system.evaluation_pressureField(["free-field", "inf_ground"], "field_ver", 
                                L1=3, L2=2, step=343/2500/6, 
                                plane="xz", offset=[-1.5, 0, -1])

system.evaluation_pressureField(["free-field", "inf_ground"], "field_hor", 
                                L1=3, L2=2, step=343/2500/6, 
                                plane="xy", offset=[-1.5, -1, 0.193])

system.evaluation_polarRadiation("free-field", "polar_ver", 
                                -180, 180, 5,  "x", "z", 
                                radius=2, offset=[0, 0, 0.193])

system.evaluation_polarRadiation("inf_ground", "polar_ver", 
                                0, 180, 5, "x", "z",
                                radius=2, offset=[0, 0, 0.193])

system.plot_system("free-field")
system.plot_system("inf_ground")

#%% run potential operators and plot results
system.run()
system.plot_results()

#%% save state
ep.save("05_evaluation_setup", system)

#%%
system.plot_results(study="inf_ground", 
                    evaluation=["field_hor", "field_ver"],
                    radiatingElement=[1, 2])
