# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:40:50 2022

@author: sarangbhagwat
"""
from bluesteam.biorefineries import generic
from bluesteam.biorefineries.generic._bluestea import BluesTEA
from bluesteam.biorefineries.generic.utils import BlueStream, has_required_properties
import thermosteam as tmo

#%% Some exmamples calls for has_required_properties
MPO = tmo.Chemical(ID='2_methyl_1_propanol', search_ID='2-methyl-1-propanol')
print(has_required_properties(MPO))

print(has_required_properties('lactic acid'))

print(has_required_properties('LacticAcid'))

print(has_required_properties('Water'))

print(has_required_properties('Cysteine'))

print(has_required_properties('PhosphopyruvicAcid'))

#%% AdipicAcid with Ethanol as an impurity

# MPO = tmo.Chemical(ID='2_methyl_1_propanol', search_ID='2-methyl-1-propanol')
stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        'Water' : 3200, # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'AdipicAcid' : 90,
        'Ethanol':120.,
        'Yeast': 1,
        'CO2': 200,
        },
        products = ['AdipicAcid',],
        impurities = ['Water', 
                      'Ethanol',
                       # MPO.ID,
                      ],
        fermentation_feed_glucose_flow = 40, #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='corn',
                  upstream_feed_capacity=1000,
                 products_and_purities={'AdipicAcid':0.5, 'Ethanol':0.9}, # {'product ID': purity in weight%}
                 products_and_market_prices={'AdipicAcid':1.75, 'Ethanol':0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Ethanol with formic acid as an impurity

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
        impurities = ['Water', 'FormicAcid'],
        fermentation_feed_glucose_flow = 40,
        )


tea_2 = BluesTEA(
    system_ID = 'sys2',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_2,
                  upstream_feed='corn',
                  upstream_feed_capacity=1000,
                 products_and_purities={'Ethanol':0.995,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'Ethanol':0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Ethanol with 2-methyl-1-propanol as an impurity

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
                  upstream_feed_capacity=1000,
                 products_and_purities={'Ethanol':0.995,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'Ethanol':0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )



#%% 3-HP

LacticAcid = tmo.Chemical('LacticAcid')
HP = tmo.Chemical(ID='HP', search_ID='3-hydroxypropionic acid')
HP.copy_models_from(LacticAcid, names = ['V', 'Hvap', 'Psat', 'mu', 'kappa'])
HP.Tm = 15 + 273.15 # CAS says < 25 C
HP.Tb = 179.75 + 273.15 # CAS
HP.Hf = LacticAcid.Hf
HP.Pc = LacticAcid.Pc
# HP.copy_models_from(tmo.Chemical('Water'), ['sigma'])
stream_3 = BlueStream(
        ID='stream_1',
        composition_dict = {
        "water": 6327.836228915082,
        HP: 508.28819656562774,
        'AceticAcid': 20.,
        "Yeast": 20,
        },
        products = [HP.ID],
        impurities = ['Water', 'AceticAcid'],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h
        )



tea_3 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_3,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={HP.ID:0.995,}, # {'product ID': purity in weight%}
                 products_and_market_prices={HP.ID:0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )


#%% EthylAcrylate

stream_3 = BlueStream(
        ID='stream_1',
        composition_dict = {
       "water": 6807.94562345661,
        "EthylAcrylate": 254.1440982828153,
        "Yeast": 20,
        "LacticAcid": 8.942380056435137,
        "AceticAcid": 5.395930114365206,
        "CO2": 254.05172796831934
        },
        products = ["EthylAcrylate"],
        impurities = ['Water', 'LacticAcid', 'AceticAcid', 
                      # 'PyrophosphoricAcid',
                      ],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h
        )


tea_3 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_3,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={"EthylAcrylate":0.5,}, # {'product ID': purity in weight%}
                 products_and_market_prices={"EthylAcrylate":0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% EthylAcetate

stream_3 = BlueStream(
        ID='stream_1',
        composition_dict = {
       "water": 6807.94562345661,
        "EthylAcetate": 254.1440982828153,
        "Yeast": 20,
        "LacticAcid": 8.942380056435137,
        "AceticAcid": 5.395930114365206,
        "CO2": 254.05172796831934
        },
        products = ["EthylAcetate"],
        impurities = ['Water', 'LacticAcid', 'AceticAcid', 
                      # 'PyrophosphoricAcid',
                      ],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h
        )


tea_3 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_3,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={"EthylAcetate":0.5,}, # {'product ID': purity in weight%}
                 products_and_market_prices={"EthylAcetate":0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Butanol
from bluesteam.biorefineries import generic
from bluesteam.biorefineries.generic._bluestea import BluesTEA
from bluesteam.biorefineries.generic.utils import BlueStream, has_required_properties
import thermosteam as tmo

stream_3 = BlueStream(
        ID='stream_1',
        composition_dict = {
       "water": 6807.94562345661,
        "Butanol": 254.1440982828153,
        "Yeast": 20,
        "LacticAcid": 8.942380056435137,
        "AceticAcid": 5.395930114365206,
        "CO2": 254.05172796831934
        },
        products = ["Butanol"],
        impurities = ['Water', 'LacticAcid', 'AceticAcid', 
                      # 'PyrophosphoricAcid',
                      ],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h
        )


tea_3 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_3,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={"Butanol":0.9,}, # {'product ID': purity in weight%}
                 products_and_market_prices={"Butanol":0.85}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )


#%% AdipicAcid

stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        "water": 6651.450347887181,
        "AdipicAcid": 234.59455226106215,
        "Yeast": 20,
        "CO2": 117.2546436776835
        },
        products = ['AdipicAcid'],
        impurities = ['Water', 
                      ],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='corn',
                  upstream_feed_capacity=1000,
                 products_and_purities={'AdipicAcid':0.5,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'AdipicAcid':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )
#%%
LacticAcid = tmo.Chemical('LacticAcid')
HP = tmo.Chemical(ID='HP', search_ID='3-hydroxypropionic acid')
HP.copy_models_from(LacticAcid, names = ['V', 'Hvap', 'Psat', 'mu', 'kappa'])
HP.Tm = 15 + 273.15 # CAS says < 25 C
HP.Tb = 179.75 + 273.15 # CAS
HP.Hf = LacticAcid.Hf
HP.Pc = LacticAcid.Pc
# HP.copy_models_from(tmo.Chemical('Water'), ['sigma'])

generic.load()
stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        "water": 6327.836228915082,
        HP: 508.28819656562774,
         "Yeast": 20
        },
        products = [HP.ID],
        impurities = ['Water', 
                      ],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='corn',
                  upstream_feed_capacity=1000,
                 products_and_purities={HP.ID:0.9,}, # {'product ID': purity in weight%}
                 products_and_market_prices={HP.ID:1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%%
LacticAcid = tmo.Chemical('LacticAcid')
HP = tmo.Chemical(ID='HP', search_ID='3-hydroxypropionic acid')
HP.copy_models_from(LacticAcid, names = ['V', 'Hvap', 'Psat', 'mu', 'kappa'])
HP.Tm = 15 + 273.15 # CAS says < 25 C
HP.Tb = 179.75 + 273.15 # CAS
HP.Hf = LacticAcid.Hf
HP.Pc = LacticAcid.Pc
# HP.copy_models_from(tmo.Chemical('Water'), ['sigma'])

generic.load()
stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        "water": 4178.758376169724,
        "AcrylicAcid": 245.24905484291463,
        "Yeast": 20,
        # "LacticAcid": 262.94353844721786
        },
        products = ['AcrylicAcid'],
        impurities = ['Water', 
                      ],
        fermentation_feed_glucose_flow = 84.11395309250501, #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='corn',
                  upstream_feed_capacity=1000,
                 products_and_purities={'AcrylicAcid':0.9,}, # {'product ID': purity in weight%}
                 products_and_market_prices={'AcrylicAcid':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )