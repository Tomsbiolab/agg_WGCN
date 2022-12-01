#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:14:57 2020

@author: luis
"""

from multiprocessing import Process, Array
import csv
from argparse import ArgumentParser
from time import sleep

def reading_pcc_matrix(path):
    
    '''This function reads the PCC matrix and returns its information to the 
    main program'''
    
    result = []
    file = open(path, 'r')
    contador = 0
    
    for line in file:
        
        if contador == 0:
            
            contador = 1
            subresult = ['']
            line = line.strip()
            linea = line.split(' ')
            #removed = linea.pop(0)
            subresult = subresult+linea
            result.append(subresult)
            
        else:
            
            line = line.strip()
            linea = line.split(' ')
            result.append(linea)
            
    return(result)

#enddef

def ranking_PCC(matrix, vector, start, end, rows, core, comparations_vector):
    
    '''This function ranks the PCC values for each row of a given matrix, and 
    returns the ranked matrix'''
    
    # result = ['a']
    # queue.put (result)
    comparations = 0
    
    for x in range(start, end):
        
        try:
            entry = matrix[x]
            removed = entry.pop(0)
            onepercent = 420
            counter = 0
            
            '''This loop converts each value of the row to float variable. When it 
            finds the number 1 (PCC of gene with himself), it converts that number
            on a 0.'''
            
            for y in range(len(entry)):
                
                value = entry[y]
                
                if x == y:
                    
                    entry[y] = -2
                
                else:
                    
                    entry[y] = (float(value))
            
            '''While the counter keeps being lower than the 1% of the total number
            of genes of the matrix, the next loops looks for the maximum value of
            the row, considering that it may be repeated maximum values. Once it 
            finds it, it puts the rank value on the same position of the values list'''
            
            maximun = 0
            equals = 0
            
            while counter < onepercent:
                
                index_line = entry.index(max(entry))
                
                if maximun != entry[index_line]:
                    
                    value = onepercent - counter
                    equals = 0
    
                else:
                    
                    equals += 1
                    value = onepercent - counter + equals
                
                maximun = entry[index_line]
                index_vector = (entry.index(max(entry)) + (rows * x))
                vector[index_vector] = 1
                entry[index_line] = -1
                counter = counter + 1  
                comparations = comparations + 1
        except:
            continue
    comparations_vector[core] = comparations
    sleep(1)
        
#enddef   

def singlethread_ranking_PCC(matrix, start, end, rows):
    
    '''This function ranks the PCC values for each row of a given matrix, and 
    returns the ranked matrix'''
    
    result = [0] * (rows*rows)
    comparations = 0
    
    for x in range(start, end):
        
        entry = matrix[x]
        removed = entry.pop(0)
        onepercent = 420
        counter = 0
        
        '''This loop converts each value of the row to float variable. When it 
        finds the number 1 (PCC of gene with himself), it converts that number
        on a 0.'''
        
        for y in range(len(entry)):
            
            value = entry[y]
            
            if x == y and float(entry[y]) == 1:
                
                entry[y] = -2
            
            else:
                
                entry[y] = (float(value))
        
        '''While the counter keeps being lower than the 1% of the total number
        of genes of the matrix, the next loops looks for the maximum value of
        the row, considering that it may be repeated maximum values. Once it 
        finds it, it puts the rank value on the same position of the values list'''
        
        maximun = 0
        equals = 0
        
        while counter < onepercent:
            
            index_line = entry.index(max(entry))
            
            if maximun != entry[index_line]:
                
                value = onepercent - counter
                equals = 0

            else:
                
                equals += 1
                value = onepercent - counter + equals
            
            maximun = entry[index_line]
            index_vector = (entry.index(max(entry)) + (rows * x))
            result[index_vector] = 1
            entry[index_line] = -1
            counter = counter + 1  
            comparations = comparations + 1
    
    return(result, comparations)
        
#enddef     

def computing_HRR_matrix(vector, rows, start, end, out_vector, core, comparations_vector):
    
    '''This function computes the HRR matrix taking as an input the vector
    with all the PCC ranked values.'''
    
    '''x is the row iterator'''
    
    comp = 0
    
    for x in range(start, end):
        
        '''y is the column iterator'''
        
        for y in range(x, rows):
             
            same_row_value = vector[(x*rows) + y]
            
            other_row_value = vector[(y*rows) + x]
            
            out_vector[(x*rows) + y] = max(other_row_value, same_row_value)
            
            out_vector[(y*rows) + x] = max(other_row_value, same_row_value)
            
            comp = comp + 1
            
    comparations_vector[core] = comp
    sleep(1)

    #print('Done')
            
#enddef

def analysing_cores(cores, value):
    
    cores_list = []
    starts = []
    ends = []
    
    for i in range(0, cores):
        
        cores_list.append(i)
    
    comp = 0
    
    for x in range(value, 0, -1):
        
        comp += x
    
    comp_per_core = comp/(cores)

    previous = 0
    c = 0
    
    for w in range(0, value):
        
        c += (value - w)
        
        if c > comp_per_core:
            
            starts.append(previous)
            ends.append(w)
            c = 0
            previous = w
    
    starts.append(previous)
    ends.append(w+1)
            
    return(cores_list, starts, ends)

#enddef

def escritura(lista, nombre):

    archivo = open(nombre, 'w')
    archivo.close()    
    
    for linea in lista:
        
        with open(nombre, mode='a') as result_file:
            line_writer = csv.writer(result_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
            line_writer.writerow(linea)  
            
#enddef

def main(input_file, output, threads):
    
    '''This functions controls the execution of the rest of the functions.'''

    #reading the PCC matrix
    
    path = input_file
    print('\n***** Starting the execution by reading the',path, 'matrix ****\n')
    pcc = reading_pcc_matrix(path)
    header = pcc.pop(0)
    
    #ranking the PCC rows
    
    cores = threads
    rows = len(pcc)
    vector = Array('i', rows*rows, lock = False)
    comparations_vector = Array('i', cores, lock = False)
    difference = rows//cores
    start = 0
    end = 0
    
    print('Launching ranking processes (1 from ', cores, ')\n', sep = '')
    for i in range(cores):
        
        process = i+1
        
        if process < cores:
            
            end = start + difference
            # print(start, end)
            
        else:
            
            end = rows
            # print(start, end)
        
        t = Process(target = ranking_PCC, args = (pcc, vector, start, end, rows, i, comparations_vector) )
        t.start ()
        
        start = end
     
    for i in range(cores):
        
        t.join()

    print('Ranking processes are finished\n')
    
    print('Number of theoretical rankings: ', 420*rows)
    
    realizados = 0
    for i in range(cores):
        
        realizados = realizados + comparations_vector[i]
        
    print('Number of done rankings: ', realizados)
    
    if realizados != (420*rows):
        
        print('\nError with multiprocessing\n')
        print('Launching ranking processes with 1 core\n', sep = '')
        
        start=0
        end = len(pcc)
        rows = len(pcc)
        result, comparations = singlethread_ranking_PCC(pcc, start, end, rows)
        vector = Array('i', rows*rows, lock = False)
    
        print('Ranking process is finished\n')
        
        print('Number of theoretical rankings: ', 420*rows)
            
        print('Number of done rankings: ', comparations)
        
        for x in range(len(result)):
            if result[x] != 0:
                vector[x] = result[x]
    
    #computing the HRR matrix
    
    out_vector = Array('i', rows*rows, lock = False)
    
    # cores = 1
    cores_list, starts, ends = analysing_cores(cores, rows)
    comparations = 0
    comparations_vector = Array('i', cores, lock = False)
    
    print('Launching HRR generation processes (1 from ', cores, ')\n', sep = '')
    for i in range(cores):
        
        start = int(starts[i])
        end = int(ends[i])
        for iterator in range(start, end):
            
            comparations += rows - iterator
        
        t = Process(target = computing_HRR_matrix, args = (vector, rows, start, end, out_vector, i, comparations_vector) )
        t.start ()
        
    for i in range(cores):
        
        t.join()
        
    print('HRR generation processes are finished\n')
    
    print('HRR comparations to do: ', comparations)
    
    done = 0
    
    for i in range(cores):
        
        done = done + comparations_vector[i]
        
    print('HRR comparations done: ', done)
    
    if done != comparations:
        
        print('\nError with multiprocessing\n')
        out_vector = Array('i', rows*rows, lock = False)
    
        cores = 1
        cores_list, starts, ends = analysing_cores(cores, rows)
        comparations = 0
        comparations_vector = Array('i', cores, lock = False)
        
        print('Launching HRR generation processes with 1 core\n', sep = '')
        for i in range(cores):
            
            start = int(starts[i])
            end = int(ends[i])
            for iterator in range(start, end):
                
                comparations += rows - iterator
            
            t = Process(target = computing_HRR_matrix, args = (vector, rows, start, end, out_vector, i, comparations_vector) )
            t.start ()
            
        for i in range(cores):
            
            t.join()
            
        print('HRR generation process is finished\n')
        
        print('HRR comparations to do: ', comparations)
        
        done = 0
        
        for i in range(cores):
            
            done = done + comparations_vector[i]
            
        print('HRR comparations done: ', done)
    
    '''The code belows writes down the final HRR matrix'''
        
    result = [header]
    
    for x in range(rows):
        
        subresult = [header[x+1]]
        
        for y in range(rows):
            
            index = (x*rows) + y
            subresult.append(out_vector[index])
        
        result.append(subresult)
    
    escritura(result, output)
    
#enddef



###############################################################################



'''MAIN PROGRAM'''

if __name__ == '__main__':
    
    parser = ArgumentParser ()

    parser.add_argument(
        '-p','--path',
        dest='path',
        action='store',
        required=True,
        help='Path of the PCC matrix.'
        )
    
    parser.add_argument(
        '-o','--output',
        dest='output',
        action='store',
        required=True,
        help='Path of the HRR matrix that will be generated.'
        )
    
    parser.add_argument(
        '-t','--threads',
        dest='threads',
        action='store',
        required=True,
        help='Number of processes that will be launched.'
        )
    
    args = parser.parse_args ()
    
    input_file = args.path
    output = args.output
    processes = int(args.threads)
    
    main(input_file, output, processes)
