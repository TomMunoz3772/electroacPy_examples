#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 14:14:48 2024

This step shows how to add a free-field and a floor-bound study.

@author: tom
"""

import electroacPy as ep

#%% load data
system = ep.load("03_LEM_Recap")

#%% Define free-field study
system.study_acousticBEM("free-field", 
                         "../geo/mesh/studio_monitor_coarse.msh", 
                         ["ported_LF", "TW29", "sealed_MF"], 
                         domain="exterior")

#%% Define boundary conditions
from electroacPy.acousticSim.bem import boundaryConditions

bc = boundaryConditions()
bc.addInfiniteBoundary(normal="z", offset=-1)
system.study_acousticBEM("inf_ground", 
                        "../geo/mesh/studio_monitor_coarse.msh",
                        ["ported_LF", "TW29", "sealed_MF"], domain="exterior", 
                        boundary_conditions=bc)

#%% run boundary operators
system.run()

#%% save state
ep.save("04_BEM_setup", system)
