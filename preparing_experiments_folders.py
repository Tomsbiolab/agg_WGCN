#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 16:57:00 2021

@author: tomslab
"""

from argparse import ArgumentParser
import os
import csv

def reading_summary(path):
    
    file = open(path, 'r')
    
    for line in file:
        
        line = line.strip().split('\t')
        if line[0] == 'Assigned':
            
            if int(line[1]) >= 10000000:
                
                return(True)
            
            else:
                
                return(False)
        
#enddef

def reading_metadata_file(tissue, network_folder, metadata_file, count_summaries_folder, count_matrices_folder):
    
    runs = []
    folders = []
    file = open(metadata_file, 'r')
    counter = 0
    total = 0
    
    first_line = file.readline()
    for line in file:
        
        line = line.strip().split('\t')
        
        if tissue[0] == 'ALL':

            path = count_summaries_folder + line[2] + '_matrix_counts.summary'
            append = reading_summary(path)
            total = total + 1 
            
            if append == True:
            
                if line[6] not in folders:
                    
                    folders.append(line[6])
                    command = 'mkdir ' + network_folder + '/' + line[6]
                    os.system(command)
      
                experiment_folder = network_folder + '/' + line[6]
                command = 'cp ' + count_matrices_folder + '/' + line[2] + '_matrix_counts.txt ' + experiment_folder + '/' + line[2] +'_matrix_counts.txt'
                os.system(command)
                counter = counter + 1
                runs.append(line[2])
                
        else:

            if line[0] in tissue:
                
                total = total +1 
                
                path = count_summaries_folder + line[2] + '_matrix_counts.summary'
                append = reading_summary(path)
                
                if append == True:
                
                    if line[6] not in folders:
                        
                        folders.append(line[6])
                        command = 'mkdir ' + network_folder + '/' + line[6]
                        os.system(command)
          
                    experiment_folder = network_folder + '/' + line[6]
                    command = 'cp ' + count_matrices_folder + '/' + line[2] + '_matrix_counts.txt ' + experiment_folder + '/' + line[2] +'_matrix_counts.txt'
                    os.system(command)
                    counter = counter + 1
                    runs.append(line[2])
    
    print('Number of runs previous to any filter: ', total, sep = '')
    print('\nNumber of runs that remain after the 10M aligned reads filter: ', counter, sep = '')

#enddef

def escritura(lista, nombre):

    archivo = open(nombre, 'w')
    archivo.close()    
    
    for linea in lista:
        
        with open(nombre, mode='a') as result_file:
            line_writer = csv.writer(result_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
            line_writer.writerow(linea)      
               
#enddef

def main(tissues_list, network_folder, metadata_file, count_summaries_folder, count_matrices_folder):
    
    metadata_folder = ('/').join(network_folder.split('/')[0:(len(network_folder.split('/'))-1)])
    tissues_list = tissues_list.split(';')
    name = metadata_folder + '/' + ('_').join(tissues_list) + '_agg_network_metadata.csv'
    reading_metadata_file(tissues_list, network_folder, metadata_file, count_summaries_folder, count_matrices_folder)
    runs = []
    
    folders = os.listdir(network_folder)
    counter = 0
    
    for folder in folders:
        
        lista = os.listdir(network_folder + '/' + folder)
        if len(lista) < 4:
            
            os.system('rm -r ' + network_folder + '/' + folder)
            
        else:
            
            counter = counter + len(lista)
            
            for entry in lista:
                
                run = entry.split('_')[0]
                runs.append(run)
            
    print('\nNumber of runs that remain after the 4 runs per experiment filter: ', counter, sep = '')
    
    metadata = []
    file = open(metadata_file, 'r')
    header = True
    
    for line in file:
        
        line = line.strip().split('\t')
        
        if header == True:
            
            metadata.append(line)
            header = False
        
        else:
            
            if line[2] in runs:
                
                metadata.append(line)
                
    escritura(metadata, name)          
            
#enddef    

'''MAIN PROGRAM'''

parser = ArgumentParser ()

parser.add_argument(
    '--tissues_list',
    dest='tissues_list',
    action='store',
    required=True,
    help='List of tissues for the network generation'
    )

parser.add_argument(
    '--network_folder',
    dest='network_folder',
    action='store',
    required=True,
    help='Path of the network folder.'
    )

parser.add_argument(
    '--metadata_file',
    dest='metadata_file',
    action='store',
    required=True,
    help='Path of the metadata file'
    )

parser.add_argument(
    '--count_summaries_folder',
    dest='count_summaries_folder',
    action='store',
    required=True,
    help='Path of the folder that contains the count summaries generated by the alignment pipeline'
    )

parser.add_argument(
    '--count_matrices_folder',
    dest='count_matrices_folder',
    action='store',
    required=True,
    help='Path of the folder that contains the count matrices generated by the alignment pipeline'
    )

args = parser.parse_args ()

tissues_list = args.tissues_list
network_folder = args.network_folder
metadata_file = args.metadata_file
count_summaries_folder = args.count_summaries_folder
count_matrices_folder = args.count_matrices_folder

main(tissues_list, network_folder, metadata_file, count_summaries_folder, count_matrices_folder)
