#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 15:11:32 2020

@author: luis
"""

import os
from argparse import ArgumentParser

def main(raw_folder, scripts_folder):

    folders = os.listdir(raw_folder)
    
    os.chdir(scripts_folder)
    
    for folder in folders:
        
        command = 'python3 merge_matrices.py -p ' + raw_folder + '/' + folder + ' -o ' + raw_folder + '/' + folder + '/' + folder + '_all_counts.txt'
        os.system(command)

#enddef

'''MAIN PROGRAM'''

parser = ArgumentParser (
)

parser.add_argument(
    '-r','--raw_counts_folder',
    dest='raw',
    action='store',
    required=True,
    help='Path of the folder that contains the raw counts matrix of all the runs.'
    )

parser.add_argument(
    '-s','--scripts_folder',
    dest='scripts',
    action='store',
    required=True,
    help='Path of the folder that contains all the scripts for the construction of the network.'
    )

args = parser.parse_args ()

scripts = args.scripts
raw = args.raw

main(raw, scripts)
