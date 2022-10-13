# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 10:56:49 2022

@author: sarangbhagwat
"""

import numpy as np
from matplotlib import pyplot as plt
import biosteam as st
import thermosteam as tmo
import pandas as pd
from datetime import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable

print('\n')
print('Setting up model ...\n')
def load_corn():
    from biorefineries import corn
    corn._load_chemicals()
    corn._load_system()
    f = corn.flowsheet
    u = f.unit
    s = f.stream
    tea = corn.corn_tea
    globals().update({'corn':corn, 'f':f, 'u':u, 's':s, 'tea':tea, 'corn_sys':f('corn_sys')})
    for unit in u:
        globals().update({unit.ID:unit})
    
load_corn()
V405.V = 200
corn.corn_tea.IRR = 0.10
corn_sys.simulate()
s.ethanol.price = tea.solve_price(s.ethanol)

#%%
def get_ethanol_MPSP(IRR=tea.IRR, units='$/gal'):
    corn_sys.simulate()
    tea.IRR = IRR
    s.ethanol.price = ethanol_MPSP = tea.solve_price(s.ethanol)
    if units == '$/kg':
        return ethanol_MPSP
    elif units == '$/gal':
        return ethanol_MPSP * 2.98669
    else:
        print('Units must be $/kg or $/gal.')
    
def get_annual_ownership_cost():
    # corn_sys.simulate()
    relevant_units = [K401, H401, V405]
    return (sum([i.power_utility.rate for i in relevant_units])*0.06*tea.operating_hours + sum([i.installed_cost for i in relevant_units])*0.13 + sum([i.installed_cost for i in relevant_units])*0.06)/(V405.tau*V405.outs[1].F_vol)

def get_cost_to_deliver_oxygen():
    # corn_sys.simulate()
    relevant_units = [K401, H401, V405]
    return (sum([i.power_utility.rate for i in relevant_units])*0.06*tea.operating_hours + sum([i.installed_cost for i in relevant_units])*0.13 + sum([i.installed_cost for i in relevant_units])*0.06)/(V405.air.imass['O2']*tea.operating_hours)

def load_yields_and_aeration_rate_and_get_MPSP(etoh_yield, yeast_yield, aer_rate,
                                               IRR=tea.IRR, units='$/gal'):
    fermentor.reaction.X = etoh_yield
    fermentor.growth.X = yeast_yield
    fermentor.aeration_rate = aer_rate
    return get_ethanol_MPSP(IRR, units)

def load_feedstock_capacity_and_get_MPSP(feedstock_capacity,
                                               IRR=tea.IRR, units='$/gal'):
    s.corn.F_mass = feedstock_capacity * 1e3 / (tea.operating_hours)
    return get_ethanol_MPSP(IRR, units)

#%%

print('Generating validation plots ...\n')
fermentor = u.V405
ann_own_costs = []
ctdos = []
MPSPs = []
aer_rates = np.linspace(0.004, 0.150, 5)
for r in aer_rates:
    fermentor.aeration_rate = r
    MPSPs.append(get_ethanol_MPSP())
    ann_own_costs.append(get_annual_ownership_cost())
    ctdos.append(get_cost_to_deliver_oxygen())
    
f1,ax1 = plt.subplots(1)
plt.ylabel('Annual cost of ownership [$/m^3/y]')
plt.xlabel('Aeration rate [mmol/L/h]')
ax1.plot(1e3*aer_rates, ann_own_costs)
f2,ax2 = plt.subplots(1)
plt.ylabel('Ethanol MPSP [$/kg]')
plt.xlabel('Aeration rate [mmol/L/h]')
ax2.plot(1e3*aer_rates, MPSPs)
f3,ax3 = plt.subplots(1)
plt.ylabel('Cost to deliver oxygen [$/kg-O2]')
plt.xlabel('Aeration rate [mmol/L/h]')
ax3.plot(1e3*aer_rates, ctdos)
f1.show()
f2.show()
f3.show()
print('\n\n')

#%%
print('Generating fermentation performance-aeration rate space ...')
# fermentor = u.V405
aer_rates = [0., 0.004, 0.010, 0.025]
etoh_yields = np.linspace(0.3, 0.95, 5)
yeast_yields = np.linspace(0.02, 0.3, 5)
MPSPs = []

# for aer_rate in aer_rates:
#     fermentor.aeration_rate = aer_rate
#     MPSPs.append([])
#     for etoh_yield in etoh_yields:
#         fermentor.reaction.X = etoh_yield
#         MPSPs[-1].append([])
#         for yeast_yield in yeast_yields:
#             fermentor.growth.X = min(1-etoh_yield-1e-3, yeast_yield)
#             # corn_sys.simulate()
#             MPSPs[-1][-1].append(get_ethanol_MPSP())

for rate in aer_rates:
    print(f'{str(aer_rates.index(rate)+1)}. fermentor.aeration_rate = {str(round(rate, 3))} mol/L/h ...')
    fermentor.aeration_rate = rate
    
    results = []
    
    for i in etoh_yields:
        b = []
        fermentor.reaction.X = i
        for j in yeast_yields:
            if j<=1-i-1e-3:
                fermentor.growth.X = j
                b.append(get_ethanol_MPSP())
            else:
                b.append(np.nan)
        results.append(b)
    
    results_pd = pd.DataFrame(results, etoh_yields, yeast_yields)
    
    # Save results as excel file
    dateTimeObj = datetime.now()
    minute = str(dateTimeObj.minute)
    minute = minute if len(minute)==2 else '0'+minute
    file_to_save = f'MPSP_across_ferm_yields_at_ar={str(fermentor.aeration_rate)}_%s.%s.%s-%s.%s'%(dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, minute)
    
    with pd.ExcelWriter(file_to_save+'.xlsx') as writer:
        results_pd.to_excel(writer, sheet_name='PFR tau in s across E0s in M')
    
    
    # Plot results
    x = np.array([etoh_yields for i in range(len(etoh_yields))])
    y = np.array([yeast_yields for i in range(len(yeast_yields))]).transpose()
    ax = plt.subplot()
    levels = np.linspace(1,6,10)
    im = ax.contourf(x, y, results, levels=levels)
    # ax.ticklabel_format(style='sci', scilimits=(0,0), axis='both')
    plt.xlabel('Ethanol fermentation yield [% theoretical]')
    plt.ylabel('Yeast fermentation yield [% theoretical]')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    # ax.clabel(im, fmt='%3.0f', colors='black', fontsize=12)
    
    plt.colorbar(im, cax=cax, label='Ethanol MPSP [$/gal]')
    
    plt.figure()
    
print('\n\n')

#%% Plot MPSP vs capacity

feed_capacities = np.linspace(365996/10, 365996*10, 20)
prod_capacities = []
MPSPs = []
for fc in feed_capacities:
    MPSPs.append(load_feedstock_capacity_and_get_MPSP(fc))
    prod_capacities.append(s.ethanol.F_mass*tea.operating_hours/(2.98669*1e6))