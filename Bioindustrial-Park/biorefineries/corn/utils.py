# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""

import numpy as np
import thermosteam as tmo
from thermosteam import Chemical, Stream
set_thermo = tmo.settings.set_thermo

__all__ = ('BlueStream', 'dextrose_equivalent',)


class BlueStream:
    def __init__(self,composition_dict,
                 products,
                 impurities,
                 ID=None):
        # chems = []
        # if not ID:
        #     ID = f's_{int(1e6*round(np.random.rand(), 6))}'
        # for k in composition_dict.keys():
        #     if type(k)==str:
        #         chems.append(Chemical(k))
        #     else:
        #         chems.append(k)
        # set_thermo(chems)
        self.ID = ID
        self.stream = stream = Stream(ID=ID)
        for k, v in composition_dict.items():
            if type(k)==str:
                stream.imol[k] = v
            else:
                stream.imol[k.ID] = v
        
        self.products = products
        self.impurities = impurities
    
    def __repr__(self):
        self.stream.show('cmol100')
        return f''
    
    
def dextrose_equivalent(n):
    """
    Return the dextrose equivalent of starch given the degree of polymerization.

    Parameters
    ----------
    n : int
        Degree of polymerization.

    Returns
    -------
    DE : float
        Dextrose equivalent.

    Notes
    -----
    The dextrose equivalent (DE) is a measure of the amount of reducing sugars 
    present in a sugar product, expressed as a percentage on a dry basis 
    relative to dextrose. For polymerized glucose (i.e. dissacharides, 
    oligosaccharides, and polysaccharides), the dextrose equivalent is given 
    by the following formula:
        
    .. math::
        DE = 100% \frac{180}{180n - 18(n - 1)}
        
    This formula (and this function) is not valid for sugars with linkages other 
    than 1-4 and 1-6 glycosidic linkages.
    
    """
    if n < 1: 
        raise ValueError('degree of polymerization, n, must be greater or equal to 1')
    n = float(n)
    MW_glucose = 180.
    MW_water = 18.
    return 100. * MW_glucose / (MW_glucose * n - MW_water * (n - 1))