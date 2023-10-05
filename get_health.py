# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 19:27:25 2023

@author: Amir
"""

from pymem import  *
from pymem.process import  *

pm = pymem.Pymem("gta-vc.exe")

game_module = module_from_name(pm.process_handle, "gta-vc.exe").lpBaseOfDll

a = []
while True:
    a = pm.read_float(game_module + 0x38D80C)
    print(a)