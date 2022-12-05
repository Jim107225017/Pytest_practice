# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:38:39 2022

@author: ChiChun.Chen
"""

# %%
# Include Modules
from src.utility import conditions_search


# %%
def test_conditions_searchs():
    
    data = {'id': 1,
            'title': 'CS50',
            'description': 'Intro to CS and art of programming!',
            'author': 'Havard',
            'borrowed': False}
    
    con_1 = {'id': 1}
    con_2 = {'id': 2}
    con_3 = {'id': 1, 'title': 'CS50'}
    con_4 = {'id': 1, 'title': 'abcd1234'}
    
    assert conditions_search(data, con_1) == True
    assert conditions_search(data, con_2) == False
    assert conditions_search(data, con_3) == True
    assert conditions_search(data, con_4) == False
    
