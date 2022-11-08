# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""TankPurchaseCostAlgorithm
"""
import biosteam as bst
import thermosteam as tmo
import flexsolve as flx
from biosteam.units.decorators import cost, copy_algorithm
from biosteam.units.design_tools import CEPCI_by_year, cylinder_diameter_from_volume, cylinder_area
from biosteam import tank_factory
import numpy as np

ParallelRxn = tmo.reaction.ParallelReaction

__all__ = (
    'GrainHandling',
    'HammerMill', 
    'CornStorage',
    'CleaningSystem',
    'MilledCornSurgeTank',
    'MilledCornHopper',
    'MilledCornWeighTank',
    'LimeHopper',
    'AmmoniaTank',
    'AlphaAmylaseTank',
    'SlurryMixTank',
    'Liquefaction',
    'JetCooker',
    'CookedSlurrySurgeTank',
    'GlucoAmylaseTank',
    'SulfuricAcidTank',
    'Saccharification',
    'YeastTank',
    'WetDDGSConveyor',
    'Liquefaction',
    'SimultaneousSaccharificationFermentation', 'SSF',
    'DDGSHandling',
    'DDGSCentrifuge',
    'PlantAir_CIP_WasteWater_Facilities',
)

CE2007 = CEPCI_by_year[2007]

CAS_water = '7732-18-5'
# Material factors. Applicable to some units only.
MF38 = 0.38 
MF90 = 0.90
MF52 = 0.52

@cost('Flow rate', units='kg/hr', CE=CE2007, cost=MF38 * 120800, S=46350.72, kW=97, n=0.6)
class GrainHandling(bst.Unit): pass

CornStorage = tank_factory('CornStorage', 
    CE=CE2007, cost=MF38 * 979300., S=185400, tau=259.2, n=1.0, V_wf=0.9, V_max=3e5, 
    V_units='m3'
)

@cost('Flow rate', units='kg/hr', CE=CE2007, cost=60300., S=45350., n=0.6, ub=7.2e5)
class CleaningSystem(bst.Splitter): pass
    

@cost('Flow rate', units='kg/hr', CE=CE2007, cost=MF38 * 98200., S=46211.33, n=0.6, ub=720000., kW=314.237)
class HammerMill(bst.Unit): pass


MilledCornSurgeTank = tank_factory('MilledCornSurgeTank', 
    CE=CE2007, cost=MF38 * 32500., S=76.90, tau=2.0, n=0.6, V_wf=0.9, V_max=200., V_units='m3'
)

MilledCornHopper = tank_factory('MilledCornHopper', 
    CE=CE2007, cost=50700., S=100.93, tau=2.0, n=0.6, V_wf=0.9, V_max=1e3, V_units='m3'
)

MilledCornWeighTank = tank_factory('MilledCornWeighTank',
    CE=CE2007, cost=MF38 * 43600., S=76.90, tau=2.0, n=0.6, V_wf=0.9, V_max=20e3, V_units='m3'
)

LimeHopper = tank_factory('LimeHopper', 
    CE=CE2007, cost=9100., S=4.02, tau=46.3, n=0.6, V_wf=0.75, V_max=100., V_units='m3'
)

AmmoniaTank = tank_factory('AmmoniaTank', 
    CE=CE2007, cost=MF38 * 28400., S=8.77, tau=100., n=0.6, V_wf=0.90, V_max=100., V_units='m3'
)

AlphaAmylaseTank = tank_factory('AlphaAmylaseTank', 
    CE=CE2007, cost=49700., S=12.77, tau=336., n=0.6, V_wf=0.90, V_max=100., V_units='m3'
)

SlurryMixTank = tank_factory('SlurryMixTank', mixing=True,
    CE=CE2007, cost=133300., S=45.29, tau=0.25, n=0.6, V_wf=0.65, V_max=80., kW_per_m3=1.1607597, V_units='m3',
)


@cost('Flow rate', units='kg/hr', CE=CE2007, cost=14000, n=0.6, S=150347)
class JetCooker(bst.Unit):
    """
    ins : stream sequence
    
        [0] Feed
        
        [1] Steam
    
    outs : stream
        Mixed product.
    
    """
    _N_outs = 1
    _N_ins = 2
    _N_heat_utilities = 0
    
    def __init__(self, ID="", ins=None, outs=(), thermo=None, T=483.15):
        super().__init__(ID, ins, outs, thermo)
        self.T = T
    
    @staticmethod
    def _T_objective_function(steam_mol, T, steam, effluent, feed):
        steam.imol[CAS_water] = abs(steam_mol)
        effluent.mol[:] = steam.mol + feed.mol
        effluent.H = feed.H + steam.H
        return effluent.T - T
    
    def _run(self):
        feed, steam = self._ins
        steam_mol = feed.F_mol / 100.
        effluent, = self.outs
        effluent.T = self.T
        steam_mol = flx.aitken_secant(self._T_objective_function,
                                      steam_mol, 1/8 * steam_mol + 1., 
                                      1e-4, 1e-4,
                                      args=(self.T, steam, effluent, feed),
                                      checkroot=False)
        effluent.P = steam.P / 2.

CookedSlurrySurgeTank = tank_factory('CookedSlurrySurgeTank',
    CE=CE2007, cost=MF90 * 173700., S=14.16, tau=0.25, n=0.6, V_wf=0.90, V_max=100., V_units='m3',
)

GlucoAmylaseTank = tank_factory('AlphaAmylaseTank', 
    CE=CE2007, cost=84200., S=17.57, tau=336., n=0.6, V_wf=0.90, V_max=100., V_units='m3'
)

SulfuricAcidTank = tank_factory('AlphaAmylaseTank', 
    CE=CE2007, cost=MF38 * 19300., S=18.87, tau=336., n=0.6, V_wf=0.90, V_max=283.17, V_units='m3'
)

Saccharification = tank_factory('AlphaAmylaseTank', kW_per_m3=0.036, mixing=True,
    CE=CE2007, cost=MF90 * 102700., S=52.10, tau=1./3., n=0.6, V_wf=0.90, V_min=20., V_max=610., V_units='m3'
)

YeastTank = tank_factory('YeastTank', kW_per_m3=0.5,
    CE=CE2007, cost=114700., S=2.97, tau=40., n=0.6, V_wf=0.90, V_max=80., V_units='m3'
)


AirCompresser = tank_factory('AirCompresser', 
                             # kW_per_m3=0.5,
    CE=CE2007, cost=114700., S=2.97, tau=3., n=0.6, V_wf=0.90, V_max=80., V_units='m3'
)


@cost('Flow rate', S=24158., n=0.6, units='kg/hr', CE=CE2007, kW=13.1, cost=55700.)
class WetDDGSConveyor(bst.Unit): pass

LiquefactionTank = tank_factory('LiquefactionTank', 
    CE=CE2007, cost=160900., S=141.3, tau=0.9, n=0.6, V_wf=0.90, V_max=500., kW_per_m3=0.6,
    mixing=True,
)

class Liquefaction(LiquefactionTank):
    """
    Create a Liquefaction unit operation that models the conversion
    for Starch to Glucose oligomers.
    
    Parameters
    ----------
    ins : stream
        Inlet fluid.
    outs : stream
        Outlet fluid.
    yield_: float
        Yield of starch to glucose as a fraction of the theoretical yield.
    
    Notes
    -----
    The conversion of Starch to Glucose oligomers is modeled according to the
    following stoichiometry:
        
    Starch + H2O -> Glucose
    
    Where starch is a chemical with formula C6H10O5 that represents linked 
    glucose monomers (dehydrated from linkage).
    
    The dextrose equivalent, and for that manner the degree of polymerization,
    is not taken into account in this unit. However, the conversion is equivalent
    to the conversion of starch to fermentable saccharides, which is what matters
    downstream.
    
    References
    ----------
    TODO
    
    """
    def __init__(self, *args, yield_=1.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.reaction = tmo.reaction.Reaction('Starch + H2O -> Glucose', 'Starch', yield_)
        
    @property
    def yield_(self):
        return self.reaction.X
    @yield_.setter
    def yield_(self, X):
        self.reaction.X = X

    def _run(self):
        effluent, = self.outs
        effluent.mix_from(self.ins)
        self.reaction(effluent)
        
# @cost('Reactor volume', 'Spargers', CE=521.9, cost=84400,
#       S=1.71e+03, n=0.5, BM=2.3, N='Number of reactors')
# @cost('Reactor volume', 'Reactors', CE=521.9, cost=844000,
#       S=3785, n=0.5, BM=2.3, N='Number of reactors')
class SimultaneousSaccharificationFermentation(bst.BatchBioreactor):
    """
    Create a SimultaneousSaccharificationFermentation unit operation that 
    models the simultaneous saccharification and fermentation in the conventional
    dry-grind ethanol process.
    
    Parameters
    ----------
    ins : streams
        Inlet fluids.
    outs : stream
        Outlet fluid.
    yield_: float
        Yield of glucose to ethanol as a fraction of the theoretical yield.
    
    Notes
    -----
    This unit operation doesn't actually model the saccharification process.
    The reactor is modeled by the stoichiometric conversion of glucose to
    ethanol by mol:
        
    .. math:: 
        Glucose -> 2Ethanol + 2CO_2
    
    Yeast is assumed to be produced from any remaining glucose:
        Glucose -> 6Yeast + 2.34H2O
    
    A compound with name 'Yeast' must be present. Note that only glucose is 
    taken into account for conversion. Cleaning and unloading time,
    `tau_0`, fraction of working volume, `V_wf`, and number of reactors,
    `N_reactors`, are attributes that can be changed. Cost of a reactor
    is based on the NREL batch fermentation tank cost assuming volumetric
    scaling with a 6/10th exponent [1]_. 
    
    References
    ----------
    .. [1] D. Humbird, R. Davis, L. Tao, C. Kinchin, D. Hsu, and A. Aden
        National. Renewable Energy Laboratory Golden, Colorado. P. Schoen,
        J. Lukas, B. Olthof, M. Worley, D. Sexton, and D. Dudgeon. Harris Group
        Inc. Seattle, Washington and Atlanta, Georgia. Process Design and Economics
        for Biochemical Conversion of Lignocellulosic Biomass to Ethanol Dilute-Acid
        Pretreatment and Enzymatic Hydrolysis of Corn Stover. May 2011. Technical
        Report NREL/TP-5100-47764
    
    
    """
    _N_ins = 6
    _N_outs = 2
    
    def __init__(self, ID='', ins=None, outs=(), thermo=None, *, 
                 tau=60.,  N=None, V=None, T=305.15, P=101325., Nmin=2, Nmax=36,
                 yield_=0.95, V_wf=0.83, 
                 aeration_rate=25e-3, # mol/L/h
                 aeration_time=60., # h
                 update_fermentation_performance_based_on_aeration=False,
                 ):
        bst.BatchBioreactor.__init__(self, ID, ins, outs, thermo,
            tau=tau, N=N, V=V, T=T, P=P, Nmin=Nmin, Nmax=Nmax
        )
        self.reactions = ParallelRxn([tmo.Rxn('Glucose -> 2Ethanol + 2CO2',  'Glucose', yield_),
                                     tmo.Rxn('Glucose -> 6Yeast + 2.34H2O',  'Glucose', 1.0-yield_),]) # 7.254 Yeast + 0.174 DAP + 15.63 CSL 
        
        self.reaction = self.reactions[0]
        self.growth = self.reactions[1]
        self.glucose_oxidation = tmo.Rxn('Glucose -> 6CO2 + 6H2O',  'Glucose', 1.0-1e-5) 
        self.V_wf = V_wf
        self.aeration_rate = aeration_rate
        self.aeration_time = aeration_time
        self.update_fermentation_performance_based_on_aeration = update_fermentation_performance_based_on_aeration
        
        self._units['Aeration rate'] = 'mol/L/h'
        
        self.broth_to_load = None
    
    def load_tau(self, tau):
        self.tau = tau
        
    def load_broth(self, bluestream):
        self.broth_to_load = bluestream.stream
        
    def _run(self):
        aeration_rate = self.aeration_rate
        if self.update_fermentation_performance_based_on_aeration:
            self.growth.X, self.reaction.X = self.get_yields_from_aeration_rate(aeration_rate)
        feed, yeast, csl, dap, air, water = self.ins
        self.air = air
        vent, effluent = self.outs
        
        if not self.broth_to_load:
            effluent.mix_from(self.ins[:-1])
            # import pdb
            # pdb.set_trace()
            try:
                air.imol['O2'] = 6.56
                air.imol['N2'] = 28.2
            except:
                air.imol['g','O2'] = 6.56
                air.imol['g','N2'] = 28.2
            air.F_mol = aeration_rate*self.tau*effluent.F_vol*5.29878 * self.aeration_time/self.tau
            self.reactions(effluent)
            # self.growth(effluent)
            # import pdb
            # pdb.set_trace()
            # print(effluent.imol['Glucose'])
            self.glucose_oxidation(effluent)
            effluent.imass['Yeast'] += effluent.imass['NH3']
            effluent.imol['NH3'] = 0.
        
        else:
            effluent.copy_like(self.broth_to_load)
            self.ins[5].imol['Water'] = max(0, sum([i.imol['Water'] for i in self.outs])-sum([i.imol['Water'] for i in self.ins]))
            
        vent.empty()
        vent.receive_vent(effluent)
        
        # vent.receive_vent(air)
        vent.imol['O2'] += air.imol['O2']
        vent.imol['N2'] += air.imol['N2']
        
        effluent.imol['O2'] = 0.
        effluent.imol['N2'] = 0.
        effluent.imol['CO2'] = 0.
        
        dap.imol['DAP'] = 0.012*effluent.imol['Yeast']
        csl.imol['CSL'] = (0.158/0.0725)*effluent.imol['Yeast'] - dap.imol['DAP']*2.
        
        vent.imol['CO2'] += csl.imol['CSL']
        
    @property
    def Hnet(self):
        X = self.reaction.X
        glucose = self.ins[0].imol['Glucose']
        return self.reaction.dH * glucose + self.growth.dH * (1 - X) + self.H_out - self.H_in
    
    def _design(self):
        bst.BatchBioreactor._design(self)    
        Design = self.design_results
        Design['Aeration rate'] = self.aeration_rate
        
    def _cost(self):
        bst.BatchBioreactor._cost(self)
        # self.power_utility(self.get_power())
        self.power_utility.consumption += self.get_power()
    @property
    def yield_(self):
        return self.reaction.X
    @yield_.setter
    def yield_(self, yield_):
        self.reaction.X = yield_
        
    def get_yields_from_aeration_rate(self, aer_rate):
        yeast_yield = 0.27762 + ((aer_rate-0.050)/(0.004-0.050))*(0.1105-0.27762)
        etoh_yield = 0.237 + ((aer_rate-0.050)/(0.004-0.050))*(0.43-0.237)
        return yeast_yield/0.82709, etoh_yield/0.51143
    
    def get_power(self):
        aeration_rate = self.aeration_rate
        aeration_time = self.aeration_time
        tau = self.tau
        air_imass_O2 = self.air.imass['O2']
        effective_aeration_rate = aeration_rate*(aeration_time/tau)
        if effective_aeration_rate>=10e-3:
            return (1.9 + 0.2*(effective_aeration_rate-10e-3))*air_imass_O2 # ~1.9-2.1 kWh/kg-O2 from Humbird et al. 2017
        else:
            cost_at_10_mmol_per_L_per_h = 1.9*air_imass_O2 
            return cost_at_10_mmol_per_L_per_h * (1. - (10e-3-effective_aeration_rate)/10e-3) # linear interpolation; 0 to 1.9 kWh/kg-O2
    
SSF = SimultaneousSaccharificationFermentation

@copy_algorithm(bst.SolidLiquidsSplitCentrifuge, run=False)
class DDGSCentrifuge(bst.Splitter): pass
    

@cost('Flow rate', units='kg/hr', CE=CE2007, cost=122800, S=15303.5346, kW=37.3, n=0.6)
class DDGSHandling(bst.Unit): pass


class PlantAir_CIP_WasteWater_Facilities(bst.Facility):
    network_priority = 0
    
    def __init__(self, ID, corn):
        self.corn = corn
        super().__init__(ID)
        
    def _run(self):
        pass
        
    def _cost(self):
        C = self.baseline_purchase_costs
        C['Facilities'] = 6e5 * (self.corn.F_mass / 46211.6723)**0.6