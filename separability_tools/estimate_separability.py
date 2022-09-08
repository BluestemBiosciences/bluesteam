# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 23:51:43 2022

@author: sarangbhagwat
"""

from bluesteam.separability_tools.utils import BlueStream, run_sequential_distillation, get_sorted_results
from datetime import datetime

#%% Run comparison

# Inputs - these are a list of possible broth streams output from fermentation
streams = [
    BlueStream(
        ID='AdAcG', # can customize this name; an auto-generated name will be given by default
        composition_dict = { # Keys: Chemicals; Use CAS IDs where unsure of names # Values: molar flows (kmol/h)
        'Water' : 1000,
        'AdipicAcid' : 20,
        'AceticAcid' : 20,
        'Glycerol' : 20,
        },
        products = ['AdipicAcid', 'AceticAcid', 'Glycerol'], # Chemicals; Use CAS IDs where unsure of names
        impurities = ['Water'] # Chemicals; Use CAS IDs where unsure of names
        ),
    
    BlueStream(
        ID='EtAcG',
        composition_dict = {
        'Water' : 1000,
        'Ethanol' : 20,
        'AceticAcid' : 20,
        'Glycerol' : 20,
        },
        products = ['Ethanol', 'AceticAcid', 'Glycerol'],
        impurities = ['Water']
        ),
    
    BlueStream(
        ID='AdG',
        composition_dict = {
        'Water' : 1000,
        'AdipicAcid' : 20,
        'Glycerol' : 20,
        },
        products = ['AdipicAcid', 'Glycerol'],
        impurities = ['Water']
        ),
    
    BlueStream(
        ID='Ad',
        composition_dict = {
        'Water' : 1000,
        'AdipicAcid' : 20,
        },
        products = ['AdipicAcid',],
        impurities = ['Water']
        ),
    
    ]

# Save file with the current time in the name (for a custom file name, edit the file_to_save string)
dateTimeObj = datetime.now()
minute = '0' + str(dateTimeObj.minute) if len(str(dateTimeObj.minute))==1 else str(dateTimeObj.minute)
file_to_save='bluesteam_separability_results_%s.%s.%s-%s.%s'%(dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, minute)

# Run
results = get_sorted_results(streams, print_results=True, file_to_save=file_to_save)

