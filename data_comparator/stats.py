import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import sqlalchemy as sqla


class SampTwo():
    """
    SampTwo takes two data samples and calculates several statistics between them
    
    """
    def __init__(self, a, b):
        self.ks_stat, self.ks_p = ks_2samp(a,b)
        min_samp_size = min(len(a), len(b))
        max_samp_size = max(len(a), len(b))
        self.valid_size = False if min_samp_size < 30 else True
        self.means = np.array((np.mean(a), np.mean(b)))
        self.stds = np.array((np.std(a), np.std(b)))
        self.counts = np.array((len(a), len(b)))