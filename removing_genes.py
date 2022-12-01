#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 14:38:06 2020

@author: luis
"""

from argparse import ArgumentParser

def reading_file(path):
    
    result = []
    file = open(path, 'r')
    
    for line in file:
        
        line = line.strip()
        linea = line.split('\t')
        
        x= 1
        add = False
        
        try:
        
            while x < len(linea):
                
                value = float(linea[x])
                if value > 0.5:
                    
                    add= True
                    
                x = x +1
                
            if add == True:
                
                result.append(line)
                
        except:
            
            result.append(line)
            continue
            
    return(result)
            
        
#enddef
    
def writing_result(path, result):
    
    file = open(path, 'w')
    for line in result:
        
        file.write(line+'\n')
        
    file.close()
    
#enddef
    
        
'''MAIN PROGRAM'''

#reading information

parser = ArgumentParser (
)

parser.add_argument(
    '-i','--input',
    dest='input',
    action='store',
    required=True,
    help='Path to the temporal file with all the FPKM values.'
    )

parser.add_argument(
    '-o','--output',
    dest='output',
    action='store',
    required=True,
    help='output file with the filtered FPKM values'
    )

args = parser.parse_args ()

input_path = args.input
output = args.output

#executing the program

result = reading_file(input_path)

writing_result(output, result)

