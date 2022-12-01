#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:14:13 2020

@author: luis
"""

import os
from argparse import ArgumentParser

'''MAIN PROGRAM'''

parser = ArgumentParser (
)

parser.add_argument(
    '-p','--path',
    dest='path',
    action='store',
    required=True,
    help='Path to the folder that contains the PCCs matrix.'
    )
    
parser.add_argument(
    '-s','--scripts',
    dest='script_folder',
    action='store',
    required=True,
    help='Path to the scripts folder.'
    )

args = parser.parse_args ()

path = args.path
scripts = args.script_folder

files = os.listdir(path)
os.chdir(scripts)

for name in files:
    
    print('\nComputing binary HRR matrix for ', name)
    input_file = path+'/'+name
    output = path + '/' + name.split('PCC')[0]+'_binary_HRR_matrix.csv'
    pcc = path + '/' + name
    order = 'python3 computing_binary_HRR_matrix_TOP420.py -p ' + input_file + ' -o ' + output + ' -t 30'
    os.system(order)
