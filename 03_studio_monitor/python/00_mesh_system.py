#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 14:16:18 2024

Meshing in Python through simplified API.

@author: tom
"""

import electroacPy.general as gtb

#%% mesh system - default size (1kHz)
cad = gtb.meshCAD("../geo/step_export/simulation_cad.step")
cad.addSurfaceGroup("woofer", surface=[8], groupNumber=1)
cad.addSurfaceGroup("port", [10], 2)
cad.addSurfaceGroup("midrange", [9], 3)
cad.addSurfaceGroup("tweeter", [7], 4)
cad.mesh("../geo/mesh/studio_monitor_coarse")

#%% refine a mesh
lmax = 343/2.5e3/6
lmin = lmax/10
cad = gtb.meshCAD("../geo/step_export/simulation_cad.step", 
                  minSize=lmin, maxSize=lmax)
cad.addSurfaceGroup("woofer", [8], 1)
cad.addSurfaceGroup("port", [10], 2)
cad.addSurfaceGroup("midrange", [9], 3)
cad.addSurfaceGroup("tweeter", [7], 4, meshSize=343/5e3/6)
cad.addSurfaceGroup("baffle", [3], 5, meshSize=343/5e3/6)
cad.mesh("../geo/mesh/studio_monitor_refined")

