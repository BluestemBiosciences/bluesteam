# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:40:50 2022

@author: sarangbhagwat
"""
from biorefineries import corn
from biorefineries.corn._bluestea import BluesTEA
from biorefineries.corn.utils import BlueStream
import thermosteam as tmo

#%% AdipicAcid with AceticAcid as an impurity

corn.load()

stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        'Water' : 2500, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'AdipicAcid' : 2,
        'AceticAcid':1.,
        'Yeast': 1,
        'CO2': 200,
        },
        products = ['AdipicAcid'],
        impurities = ['Water', 'AceticAcid'],
        fermentation_feed_glucose_flow = 40, #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

# stream_1.stream.F_mass *= 127101/17874 # temporary fix

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='sucrose',
                 products_and_purities={'AdipicAcid':0.5,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'AdipicAcid':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

tea_1.set_upstream_feed_capacity(1109.08) # a way to update the upstream feed capacity such that the bluestream total flow is automatically updated
# note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%

#%% Ethanol with formic acid as an impurity

corn.load()

stream_2 = BlueStream(
        ID='stream_2',
        composition_dict = {
        'Water' : 2500, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'Ethanol' : 40,
        'FormicAcid':2,
        'Yeast': 1.,
        # 'CO2': 457,
        },
        products = ['Ethanol'],
        impurities = ['Water'],
        fermentation_feed_glucose_flow = 40,
        )


tea_2 = BluesTEA(
    system_ID = 'sys2',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_2,
                  upstream_feed='corn',
                 products_and_purities={'Ethanol':0.995,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'Ethanol':0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )
tea_2.set_upstream_feed_capacity(1109.08)
# note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%

#%% Ethanol with 2-methyl-1-propanol as an impurity

corn.load()

MPO = tmo.Chemical(ID='2_methyl_1_propanol', search_ID='2-methyl-1-propanol')
stream_3 = BlueStream(
        ID='stream_1',
        composition_dict = {
        'Water' : 600, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'Ethanol' : 30,
        MPO: 5.,
        'Yeast': 1.,
        # 'CO2': 457,
        },
        products = ['Ethanol'],
        impurities = ['Water', MPO.ID],
        fermentation_feed_glucose_flow = 40, #kmol/h
        )



tea_3 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_3,
                  upstream_feed='corn',
                 products_and_purities={'Ethanol':0.995,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'Ethanol':0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

tea_3.set_upstream_feed_capacity(1109.08) # a way to update the upstream feed capacity such that the bluestream total flow is automatically updated


