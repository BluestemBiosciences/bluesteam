# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 12:47:45 2022

@author: sarangbhagwat
"""

from bluesteam.biorefineries import generic
from bluesteam.biorefineries.generic._bluestea import BluesTEA
from bluesteam.biorefineries.generic.utils import BlueStream, has_required_properties
import thermosteam as tmo

#%%
import os
os.environ['NUMBA_DISABLE_JIT'] = '1'

#%% Example_1
MPO = tmo.Chemical(ID='MPO', search_ID='2-methyl-1-propanol')
stream_1 = BlueStream(
        ID='stream_1',
        composition_dict = {
        "Water": 6618.481179294014,
        "AdipicAcid": 154.89413990078867,
        "Yeast": 20,
        "LacticAcid": 17.884760112870275,
        "AceticAcid": 10.791860228730412,
        "MPO": 86.31073179134295,
        "CO2": 250.04038489513735
        },
        products = ['AdipicAcid',],
        impurities = ['Water', 
                      'LacticAcid',
                      'AceticAcid',
                       "MPO",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_1 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_1.ID+'_sys',
                  bluestream=stream_1,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'AdipicAcid':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'AdipicAcid':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_2
LacticAcid = tmo.Chemical('LacticAcid')
HP = tmo.Chemical(ID='HP', search_ID='3-hydroxypropionic acid')
HP.copy_models_from(LacticAcid, names = ['V', 'Hvap', 'Psat', 'mu', 'kappa'])
HP.Tm = 15 + 273.15 # CAS says < 25 C
HP.Tb = 179.75 + 273.15 # CAS
HP.Hf = LacticAcid.Hf
HP.Pc = LacticAcid.Pc

stream_2 = BlueStream(
        ID='stream_2',
        composition_dict = {
        "water": 6331.54716019406,
       "HP": 496.4281386457651,
       "Yeast": 20,
       "LacticAcid": 17.884760112870275,
       "AceticAcid": 10.791860228730412,
       "Ethanol": 3.556724191556348,
       "SuccinicAcid": 7.113448383112774
        },
        products = ['HP',],
        impurities = [
            "water",
            "LacticAcid",
            "AceticAcid",
            "Ethanol",
            "SuccinicAcid",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_2 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_2.ID+'_sys',
                  bluestream=stream_2,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'HP':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'HP':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_3
LacticAcid = tmo.Chemical('LacticAcid')
HP = tmo.Chemical(ID='HP', search_ID='3-hydroxypropionic acid')
HP.copy_models_from(LacticAcid, names = ['V', 'Hvap', 'Psat', 'mu', 'kappa'])
HP.Tm = 15 + 273.15 # CAS says < 25 C
HP.Tb = 179.75 + 273.15 # CAS
HP.Hf = LacticAcid.Hf
HP.Pc = LacticAcid.Pc

stream_3 = BlueStream(
        ID='stream_3',
        composition_dict = {
        "water": 6331.54716019406,
       "HP": 508.28819656562774,
       "Yeast": 20,
       "LacticAcid": 17.884760112870275,
       "AceticAcid": 10.791860228730412,
        },
        products = ['HP',],
        impurities = [
            "water",
            "LacticAcid",
            "AceticAcid",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_3 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_3.ID+'_sys',
                  bluestream=stream_3,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'HP':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'HP':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_4
APO = tmo.Chemical(ID='APO', search_ID='azepan-2-one')

stream_4 = BlueStream(
        ID='stream_4',
        composition_dict = {
        "water": 6807.791760751999,
        "APO": 203.31527862625188,
        "Yeast": 20,
        "LacticAcid": 17.884760112870275,
        "AceticAcid": 10.791860228730412,
        "CO2": 304.86207356198526
        },
        products = ['APO',],
        impurities = [
            "water",
            "LacticAcid",
            "AceticAcid",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_4 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_4.ID+'_sys',
                  bluestream=stream_4,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'APO':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'APO':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_5
Butanol = tmo.Chemical(ID='Butanol', search_ID='n-butanol')

stream_5 = BlueStream(
        ID='stream_5',
        composition_dict = {
        "water": 6554.027140435833,
        "Butanol": 254.14409828281325,
        "Yeast": 20,
        "LacticAcid": 17.884760112870275,
        "AceticAcid": 10.791860228730412,
        "CO2": 508.10345593664937
        },
        products = ['Butanol',],
        impurities = [
            "water",
            "LacticAcid",
            "AceticAcid",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_5 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_5.ID+'_sys',
                  bluestream=stream_5,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'Butanol':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'Butanol':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_6
BDO = tmo.Chemical(ID='BDO', search_ID='2,3-Butanediol')

stream_6 = BlueStream(
        ID='stream_6',
        composition_dict = {
        "water": 6437.895913598838,
        "BDO": 277.2481072176166,
        "Yeast": 20,
        "LacticAcid": 17.884760112870275,
        "AceticAcid": 10.791860228730412,
        "CO2": 415.72100940270406
        },
        products = ['BDO',],
        impurities = [
            "water",
            "LacticAcid",
            "AceticAcid",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_6 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_6.ID+'_sys',
                  bluestream=stream_6,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'BDO':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'BDO':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_7
BDO = tmo.Chemical(ID='BDO', search_ID='2,3-Butanediol')

stream_7 = BlueStream(
        ID='stream_7',
        composition_dict = {
        "water": 6437.895913598838,
        "BDO": 277.2481072176166,
        "Yeast": 20,
        "CO2": 415.72100940270406
        },
        products = ['BDO',],
        impurities = [
            "water",
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_7 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_7.ID+'_sys',
                  bluestream=stream_7,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'BDO':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'BDO':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )

#%% Example_8
BD_1_4_O = tmo.Chemical(ID='BD_1_4_O', search_ID='1,4-Butanediol')

stream_8 = BlueStream(
        ID='stream_8',
        composition_dict = {
       "water": 6468.800723734534,
        "BD_1_4_O": 245.24905484291597,
        "Yeast": 20,
        "LacticAcid": 17.884760112870275,
        "AceticAcid": 10.791860228730412,
        "IsoamylAcetate": 18.519033854532868,
        "CO2": 414.03746087047836
        },
        products = ['BD_1_4_O',],
        impurities = [
            "water",
            'LacticAcid',
            'AceticAcid',
            'IsoamylAcetate',
                       
                      ],
        fermentation_feed_glucose_flow = 265 , #kmol/h # note: for corn, we get about 0.1567990 kmol-glucose/h per wet-metric-tonne-corn/d or about 0.677959 kg-glucose per wet-kg-corn; note also that the moisture content of corn is 85 wt%
        )

tea_8 = BluesTEA(
    system_ID = 'sys1',
                # system_ID=stream_8.ID+'_sys',
                  bluestream=stream_8,
                  upstream_feed='sucrose',
                  upstream_feed_capacity=1000,
                 products_and_purities={'BDO':0.999}, # {'product ID': purity in weight%}
                 products_and_market_prices={'BDO':1.75}, # {'product ID': price in $/pure-kg})
                 current_equipment=None,
                 fermentation_residence_time=100., # h
                 aeration_rate=15e-3,
                 )