#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:04:21 2026
Parses through a created arbitrary waveform file for the RIGOL DG1022 and checks its length

@author: max
"""

from rdflib import Graph

g = Graph()

g.parse("random_laser.raf", format="xml") 

print(f"Graph has {len(g)} statements.")
