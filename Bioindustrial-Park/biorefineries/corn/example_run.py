# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:40:50 2022

@author: sarangbhagwat
"""
from biorefineries import corn
from biorefineries.corn._bluestea import BluesTEA
from biorefineries.corn.utils import BlueStream

#%% AdipicAcid

corn.load()

stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        'Water' : 1000, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'AdipicAcid' : 20,
        'Yeast': 1,
        'CO2': 457,
        },
        products = ['AdipicAcid'],
        impurities = ['Water'],
        )

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='corn',
                 products_and_purities={'AdipicAcid':0.995,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'AdipicAcid':4.088}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )


#%% Ethanol

corn.load()

stream_2 = BlueStream(
        ID='stream_2',
        composition_dict = {
        'Water' : 1000, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'Ethanol' : 40,
        'Yeast': 1,
        'CO2': 457,
        },
        products = ['Ethanol'],
        impurities = ['Water'],
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


#%%

# #%% AdipicAcid

# corn.load()

# stream_1 = BlueStream(
#         ID='stream_1',
#         composition_dict = {
#         'Water' : 400, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
#         'AdipicAcid' : 6,
#         'Yeast': 10,
#         'CO2': 45,
#         },
#         products = ['AdipicAcid'],
#         impurities = ['Water'],
#         )

# tea_1 = BluesTEA(
#     system_ID = 'sys1',
#                 # system_ID=stream_1.ID+'_sys',
#                   bluestream=stream_1,
#                   upstream_feed='corn',
#                  products_and_purities={'AdipicAcid':0.995,}, # {'product ID': purity in weight%}
#                  products_and_market_prices={'AdipicAcid':4.088}, # {'product ID': price in $/pure-kg})
#                  current_equipment=None,
#                  fermentation_residence_time=3., # h
#                  aeration_rate=15e-3,
#                  )


# #%% Ethanol

# corn.load()

# stream_2 = BlueStream(
#         ID='stream_2',
#         composition_dict = {
#         'Water' : 400, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
#         'Ethanol' : 15,
#         'Yeast': 10,
#         'CO2': 45,
#         },
#         products = ['Ethanol'],
#         impurities = ['Water'],
#         )

# tea_2 = BluesTEA(
#     system_ID = 'sys2',
#                 # system_ID=stream_1.ID+'_sys',
#                   bluestream=stream_2,
#                   upstream_feed='corn',
#                  products_and_purities={'Ethanol':0.995,}, # {'product ID': purity in weight%}
#                  products_and_market_prices={'Ethanol':0.85}, # {'product ID': price in $/pure-kg})
#                  current_equipment=None,
#                  fermentation_residence_time=3., # h
#                  aeration_rate=15e-3,
#                  )

