#!/usr/bin/python3
# coding: utf-8

import sys, os
import Parser as ps
import CodeWriter as cw

def main():
    filename = sys.argv[1]
    outfile = os.path.splitext(filename)[0] + '.asm'
    with ps.Parser(filename) as p:
        while p.hasMoreCommands():
            p.advance()

if __name__=='__main__':
    main()
