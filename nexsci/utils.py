#from __future__ import division, print_function
#from __future__ import absolute_import
# -*- coding: utf-8 -*-

import numpy as np

def quad_err(err1,err2):
    q = np.sqrt(err1**2+err2**2)
    return float(q)
