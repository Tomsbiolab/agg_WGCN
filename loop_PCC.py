#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:15:54 2020

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
    help='Path to the folder that contains the experiments folders.'
    )

parser.add_argument(
    '-s','--scripts',
    dest='scripts',
    action='store',
    required=True,
    help='Path to the folder that contains the scripts needed for the network generation.'
    )

parser.add_argument(
    '-a','--annotations',
    dest='annotation',
    action='store',
    required=True,
    help='Path to the file that contains the gene lenght information.'
    )

args = parser.parse_args ()

path = args.path
scripts = args.scripts
anno = args.annotation

folders = os.listdir(path)
os.chdir(scripts)

for name in folders:
    
    folder = path + '/' + name
    file = folder+'/'+name+'_all_counts.txt'
    command = 'Rscript generating_PCC.R '+ folder + ' ' + file + ' ' + path + ' ' + anno + ' ' + scripts
    os.system(command)
    
