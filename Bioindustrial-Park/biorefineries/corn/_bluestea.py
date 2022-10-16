# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:38:02 2022

@author: saran
"""
from biorefineries.corn._tea import create_tea
from biorefineries.corn.load_corn import load_set_and_get_corn_upstream_sys

__all__=['BluesTEA',]

class BluesTEA():
    def __init__(self, 
            system_ID = 'sys1',
               IRR=0.15,
               duration=(2018, 2038),
               depreciation='MACRS7', income_tax=0.35,
               operating_days=330, lang_factor=4,
               construction_schedule=(0.4, 0.6), WC_over_FCI=0.05,
               labor_cost=2.3e6, fringe_benefits=0.4,
               property_tax=0.001, property_insurance=0.005,
               supplies=0.20, maintenance=0.01, administration=0.005,
               upstream_feed='sucrose', 
               # upstream_feed_price=0.287, # Singh et al. 2022
               upstream_feed_price=None,
               upstream_feed_capacity=100,# metric tonne/d
               products_and_purities={'Ethanol':0.995,}, # {'product ID': purity in weight%}
               products_and_market_prices={'Ethanol':0.84}, # {'product ID': price in $/pure-kg}
               aeration_rate=0.,
               current_equipment={'R302':('FermentationTank', 20), 
                                  '':()}, # {'unit ID':('unit type', equipment size in m^3)}
               # fermentation_specifications={'Microbe':'Yeast', 'Titer':80, # g/L
               #                              'Productivity': 1, # g/L/h
               #                              'Yield':0.8 # %theoretical
               #                              },
               fermentation_residence_time=100., # h
               bluestream=None, # broth output from fermentation, including microbe
               ):

        self.system_up_to_fermentation = system_up_to_fermentation =\
            load_set_and_get_corn_upstream_sys(ID=system_ID+'_conversion',
                                                bluestream=bluestream, 
                                                fermentation_tau=fermentation_residence_time,
                                                aeration_rate = aeration_rate,
                                                upstream_feed=upstream_feed, 
                                                upstream_feed_capacity=upstream_feed_capacity * 1000./24., # kg/h
                                                )
        self.separation_system = separation_system = self.get_system_from_APD(new_ID=system_ID+'separation')
        
        self.system = system = self.join_systems(system_up_to_fermentation, separation_system, new_ID=system_ID)
        self.separation_system = None
        self.system = system = system_up_to_fermentation
        self.tea = tea = create_tea(system, 
                   IRR=IRR,
                   duration=duration,
                   depreciation=depreciation, income_tax=income_tax,
                   operating_days=operating_days, lang_factor=lang_factor,
                   construction_schedule=construction_schedule, WC_over_FCI=WC_over_FCI,
                   labor_cost=labor_cost, fringe_benefits=fringe_benefits,
                   property_tax=property_tax, property_insurance=property_insurance,
                   supplies=supplies, maintenance=maintenance, administration=administration)
        
        self.upstream_feed = upstream_feed
        self.upstream_feed_price = upstream_feed_price
        self.products_and_purities = products_and_purities
        self.products_and_market_prices = products_and_market_prices
        self.aeration_rate = aeration_rate
        
        self.flowsheet = flowsheet = self.system.flowsheet
        self.fermentation_reactor = fermentation_reactor = flowsheet('V405')
        
        # tea_dir = self.tea.__dir__()
        # for i in tea_dir:
        #     if not i in self.__dict__.keys():
        #         self.__dict__[i] = tea.__getattribute__(i)
        
        system.simulate()
        # fermentation_reactor.effluent.price = products_and_market_prices['Ethanol'] * fermentation_reactor.effluent.imass['Ethanol']/fermentation_reactor.effluent.F_mass
        tea.solve_IRR()
        
    def get_system_from_APD(self, new_ID):
        return None
    
    def join_systems(self, sys1, sys2, new_ID):
        return sys1
    
    def save_report(self, filename):
        self.system.save_report(filename)
    