"""Implementation of protein sequence coding
"""

__version__ = '0.0.1'
__all__ = ['ct_code_of', 'ac_code_of', 'ld_code_of', 
           'mos_code_of', 
           'mos0_code_of', 
           'mos1_code_of', #'corrcoef_of', 
           ]

__author__ = 'Gui Yuanmiao <smalltalkman@foxmail.com>'

from coding.ct import ct_code_of
from coding.ac import ac_code_of
from coding.ld import ld_code_of
from coding.mos import mos_code_of
from coding.mos0 import mos0_code_of
from coding.mos1 import mos1_code_of#, corrcoef_of
