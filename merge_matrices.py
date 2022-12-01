#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 11:11:24 2020

@author: luis
"""

from argparse import ArgumentParser
import csv
from os import scandir
from os.path import abspath

def ls(ruta):
    return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file()]

#enddef
    
def lectura_matrices(archivos):
    
    resultado = []
    
    for i in range(len(archivos)):
        
        lectura = open(archivos[i],'r')
        
        if i == 0:
            
            for line in lectura:
                
                line = line.strip()
                linea = line.split('\t')
                resultado.append(linea)
                
        else:
            
            contador = 0
            
            for line in lectura:
                
                line = line.strip()
                linea = line.split('\t')
                
                try:
                
                    dato = linea[6]
                    resultado[contador].append(dato)
                    contador = contador + 1
                    
                except:
                    
                    contador = contador + 1
                    continue
                
                
    
    return(resultado)
    
#enddef
    
def escritura(lista, nombre):
    
    for linea in lista:
        if len(linea)>1:
#            print(linea)
        
            with open(nombre, mode='a') as result_file:
                line_writer = csv.writer(result_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
                line_writer.writerow(linea)

'''MAIN PROGRAM'''

parser = ArgumentParser (
)

parser.add_argument(
    '-p','--path',
    dest='path',
    action='store',
    required=True,
    help='Path to the folder that contains the matrix counts files.'
    )

parser.add_argument(
    '-o','--output',
    dest='output',
    action='store',
    required=True,
    help='output file'
    )

args = parser.parse_args ()

ruta = args.path
output = args.output

#ruta = '/home/luis/Escritorio/matrices'
lista = ls(ruta)

lista.sort(key = str.lower)

merge = lectura_matrices(lista)

#output = '/home/luis/Escritorio/matrices/all_counts.csv'
escritura(merge, output)