#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 14:36:46 2022

@author: rfaure
"""

import argparse


def get_contig(file, contig, contigOffset):
       
    with open(file) as f:

        f.seek(contigOffset)
        line = f.readline()         
        sline = line.strip('\n')
        
       
        return sline


def main() :
    args = get_arguments()
    
    assembly = args.assembly
    reads = args.reads
    output = args.output
    
    comp = {'A':'T' , 'C':'G' , 'G':'C' , 'T':'A' }
    
    #compute offsets (to not have to look through the whole fasta file to find one sequence)
    line_offset = {}
    offset = 0
    with open(reads) as readsFile :
        for line in readsFile:
            
            sline = line.strip('\n').split()[0]
            if sline[0] == '>' or sline[0] == '@' :
                line_offset[sline[1:]] = offset  + len(line)#adds pair sline[1]:offset to the dict
                
            offset += len(line)
    
    
    fo = open(output, "w")
    
    with open(assembly) as assemblyFile :
        
        name = ''
        sequence = ''
        storeLines = ''
        for line in assemblyFile :
            
            sline = line.strip('\n').split('\t')
            
            if "S" in sline[0] :
                
                if name != '' :
                    if sequence == '' :
                        sequence = '*'
                    fo.write("S\t"+name+ "\t"+sequence+"\t"+'\t'.join(sline[3:])+"\n")
                    
                fo.write(storeLines)
                
                sequence = ''
                name = sline[1]
                storeLines = ''
                
                
            else :
                storeLines += line
                #fo.write(line)
                
                if "a" in sline[0] :
                    
                    readName = sline[3].split(':')[0]
                    start = int(sline[3].split(':')[1].split('-')[0])
                    length = int(sline[5])
                    orientation = sline[4]
                    
                    read = get_contig(reads, readName, line_offset[readName])
                    
                    subread = read[start : start+length]
                    
                    if orientation == '-':
                        
                        subread = ''
                        for c in read[start+length-1:start-1:-1] :
                            subread += comp[c]
                    
                    
                    sequence += subread
                    
    if sequence == '' :
        sequence = '*'
    fo.write("S\t"+name+ "\t"+sequence+"\n")
    fo.write(storeLines)
                
                
    
def get_arguments():
    parser = argparse.ArgumentParser(description='build_seq_from_miniasm : to rebuild the contigs from the \'a\' lines and the fasta/q file')
    parser.add_argument('--assembly', type=str, required=True,
                        help='Assembly from miniasm, in GFA format with or without the sequences')
    
    parser.add_argument('--reads', type=str, required = True,
                        help='Fasta/q file of the reads used to build the assembly')
    
    parser.add_argument('--output', type=str, required = True,
                        help='Output file in GFA format')
    
    return parser.parse_args()



if __name__ == '__main__':
    main()