#!/usr/bin/python3
# coding: utf-8

import sys, os, glob
import JackTokenizer as jt
import CompilationEngine as ce

def main():
    path = sys.argv[1]

    if os.path.isfile(path):
        file_list = [sys.argv[1]]
        #output_file = os.path.splitext(path)[0] + '.xml'
    else:
        if path[-1] != '/':
            path = path + '/'
        file_list = glob.glob(path + '*.jack')
        #output_file = path + path.split('/')[-2] + '.asm'
        ## Sys.vm を file_list の先頭に
        #index_of_sys = file_list.index(path + 'Sys.vm')
        #file_list[0], file_list[index_of_sys] = \
        #    file_list[index_of_sys], file_list[0]

    for input_file in file_list:
        j = jt.JackTokenizer(input_file)
        output_file = input_file.replace('.jack', 'T.xml')
        c = ce.CompilationEngine(input_file, output_file)
        while j.hasMoreTokens():
            pass





        j.f.close()

if __name__=='__main__':
    main()
