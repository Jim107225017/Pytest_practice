# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:19:12 2022

@author: ChiChun.Chen
"""


def conditions_search(data: dict, conditions: dict) -> bool:
    return all(data.get(KEY)==VALUE for KEY, VALUE in conditions.items())

