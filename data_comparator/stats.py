import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from scipy.stats import chisquare  
import sqlalchemy as sqla


class SampTwo():
    """
    SampTwo takes two data samples and calculates the KS statistic between them
    Inputs:
        ref: iterable of numerical data
        comp: iterable of numerical data
    Class objects on output
        - self.counts: numpy array of length of reference and comparison arrays
        - self.means: numpy array of means of reference and comparison arrays
        - self.stds: numpy array of stds of reference and comparison arrays
        - self.chisq_stat: chi-squared statistic output  
        - self.chisq_p: p-value of the self.chisq_stat
    """
    def __init__(self, ref, comp):
        self.ks_stat, self.ks_p = ks_2samp(ref,comp)
        min_samp_size = min(len(ref), len(comp))
        self.valid_size = False if min_samp_size < 30 else True
        self.means = np.array((np.mean(ref), np.mean(comp)))
        self.stds = np.array((np.std(ref), np.std(comp)))
        self.counts = np.array((len(ref), len(comp)))

class CategoryComp():
    """
    CategoryComp compares categories of two samples
    Inputs: 
        ref: iterable of categorical data
        comp: iterable of categorical data
        use_mask=True: boolean
    Assumptions:
        - Number of categories are less than np.sqrt(len(data))
        - More than 1 category in both reference and comparison
        - use_mask adds vanishingly small support to categories in one data not contained in other
    Class objects on output
        - self.counts: pandas DataFrame with reference in row 0, comparison in row 1, columns are categories
        - self.proportions: row-frequency of category observance
        - self.chisq_stat: chi-squared statistic output
        - self.chisq_p: p-value of the self.chisq_stat
    """
    def __init__(self, ref, comp, use_mask = True):
        pd_ref = pd.Series(ref)
        pd_comp = pd.Series(comp)
        _len_ref = len(pd_ref)
        _len_comp = len(pd_comp)
        _n_ref = pd_ref.nunique()
        _n_comp = pd_comp.nunique()
        self.valid_size_large = False if (_n_ref > _len_ref**.5 or _n_comp >_len_comp**.5) else True
        self.valid_size_count = False if (_n_ref <= 1 or _n_comp <= 1) else True
        if self.valid_size_large and self.valid_size_count:
            self.counts = pd.DataFrame(data=(pd_ref.value_counts(),pd_comp.value_counts())).fillna(0)
            self.proportions = self.counts.apply(lambda x : x / x.sum(), axis=1)
            proportions_usemask = self.proportions + .000000000000001
            proportions_usemask = proportions_usemask.div(proportions_usemask.sum(axis=1),axis=0)
            if use_mask:
                self.chisq_stat, self.chisq_p = chisquare(proportions_usemask.iloc[1], proportions_usemask.iloc[0])
            else:
                self.chisq_stat, self.chisq_p = chisquare(self.proportions.iloc[1], self.proportions.iloc[0])



