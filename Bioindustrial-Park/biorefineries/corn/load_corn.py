# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 10:17:57 2022

@author: sarangbhagwat
"""

from biorefineries import corn
from biosteam import System
import thermosteam as tmo
from thermosteam import Stream

def load_set_and_get_corn_upstream_sys(ID, bluestream=None, fermentation_tau=None, simulate=False, 
                                       aeration_rate=0.,
                                       upstream_feed='sucrose',
                                       upstream_feed_capacity=100., # kg/h
                                       thermo=None):
    if bluestream:
        tmo.settings.set_thermo(bluestream.stream.chemicals)
    corn.load()
    units = corn.flowsheet.unit
    streams = corn.flowsheet.stream
    V405 = units['V405']
    E401 = units['E401']
    E316 = units['E316']
    
    E401.ins[1].disconnect_source()
    E401.outs[1].disconnect_sink()
    
    E316.ins[1].disconnect_source()
    E316.outs[1].disconnect_sink()
    # import pdb
    # pdb.set_trace()
    if bluestream:
        V405.load_broth(bluestream)
        V405.outs[1].sink.outs[0].disconnect_sink()
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
        
    units_till_fermentation = [u for u in list(V405.get_upstream_units()) 
                               if len(u.ID)==4 
                               and ((int(u.ID[1])<4)
                               or (int(u.ID[1])==4 and int(u.ID[3])<5))]
    V405.simulate()
    new_sys = System.from_units(ID=ID, units=list(units_till_fermentation)+[V405, V405.outs[1].sink])
    if simulate:
        new_sys.simulate()
    return new_sys