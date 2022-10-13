# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 10:17:57 2022

@author: sarangbhagwat
"""

from biorefineries import corn
from biosteam import System
from thermosteam import Stream

def load_set_and_get_corn_upstream_sys(ID, bluestream=None, fermentation_tau=None, simulate=False, 
                                       aeration_rate=0.,
                                       upstream_feed='sucrose',
                                       upstream_feed_capacity=100., # kg/h
                                       ):
    corn.load()
    units = corn.flowsheet.unit
    streams = corn.flowsheet.stream
    V405 = units['V405']
    if bluestream:
        V405.load_broth(bluestream)
    if fermentation_tau:
        V405.load_tau(fermentation_tau)
    # tea = corn.corn_tea
    # corn.corn_tea.system.simulate()
    # tea.IRR = IRR
    V405.aeration_rate = aeration_rate
    units_till_fermentation = None
    
    
    if upstream_feed=='corn':
        streams['corn'].F_mass = upstream_feed_capacity
    
      
    elif upstream_feed=='sucrose':
        sucrose = Stream('Glucose')
        sucrose.imass['Glucose'] = upstream_feed_capacity
        V405.ins[0] = sucrose
        
    units_till_fermentation = V405.get_upstream_units()
    new_sys = System.from_units(ID=ID, units=list(units_till_fermentation)+[V405])
    if simulate:
        new_sys.simulate()
    return new_sys