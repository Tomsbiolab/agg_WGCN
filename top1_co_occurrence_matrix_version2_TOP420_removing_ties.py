#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:00:36 2020

@author: tomslab
"""

from argparse import ArgumentParser
import csv

def reading_matrix(path):
    
    result = []
    file = open(path, 'r')
    contador = 0
    
    for line in file:
        
        if contador == 0:
            
            line = line.strip().split('\t')
            contador = 1
            result.append(line)
            
        else:
            
            line = line.strip().split('\t')
            result.append(line)
        
    return(result)

#enddef

def filtering_top420_removing_ties(matrix):
    
    print('Generating the EGAD and Cyto matrix')
    
    header = matrix.pop(0)
    header_def = [''] + header
    result_egad = [header_def]
    result_cyto = []
    top_number = 420
    
    for row_iterator in range(0, len(matrix)):
        
        row = matrix[row_iterator]
        source_gene = row.pop(0)
        row = [int(i) for i in row]
        result_row = [0]*(len(row)+1)
        result_row[0] = source_gene
        
        for x in range(0, top_number):
            
            maximum = max(row)
            index = row.index(maximum)
            result_row[index + 1] = maximum
            result_cyto.append([source_gene, header[index], maximum])
            row[index] = -10
                
        result_egad.append(result_row)
            
    return(result_egad, result_cyto)

#enddef    
    
def escritura(lista, nombre):

    archivo = open(nombre, 'w')
    archivo.close()    
    
    for linea in lista:
        
        with open(nombre, mode='a') as result_file:
            line_writer = csv.writer(result_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
            line_writer.writerow(linea)  
            
               
#enddef

def main(input_file, output_cyto, output_egad):

    #reading the matrix file
    
    print('\nReading the co-occurrence matrix\n')
    path = input_file
    matrix = reading_matrix(path)
    
    print('\Filtering the co-occurrence matrix removing TOP420 ties\n')
    result_egad, result_cyto = filtering_top420_removing_ties(matrix)
    
    print('\nWriting EGAD matrix')
    escritura(result_egad, output_egad)
    
    print('\nWriting Cyto matrix')
    escritura(result_cyto, output_cyto)
    
#enddef

'''MAIN PROGRAM'''

if __name__ == '__main__':
    
    parser = ArgumentParser ()

    parser.add_argument(
        '-p','--path',
        dest='path',
        action='store',
        required=True,
        help='Path of the co-occurrence matrix.'
        )
    
    parser.add_argument(
        '-c','--cyto_output',
        dest='cyto_output',
        action='store',
        required=True,
        help='Path of the Cytoscape-format network that will be generated.'
        )
    
    parser.add_argument(
        '-e','--EGAD_output',
        dest='egad_output',
        action='store',
        required=True,
        help='Path of the EGAD-format network that will be generated.'
        )
    
    args = parser.parse_args ()
    
    input_file = args.path
    cyto_output = args.cyto_output
    egad_output = args.egad_output
    
    main(input_file, cyto_output, egad_output)