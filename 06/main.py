#!/usr/bin/python3
# coding: utf-8

import sys, os
import Parser as ps

def main():
    filename = sys.argv[1]
    outfile = os.path.splitext(filename)[0] + '.hack'

    with open(outfile, 'wt') as fout:
        with ps.Parser(filename) as p:
            while p.hasMoreCommands():
                p.advance()
                print('command: ' + p.command)
                if p.commandType() != ps.C_COMMAND:
                    bin = p.symbol()
                else:
                    bin = '111' + p.comp() + p.dest() + p.jump()
                print('bin:     ' + bin)
                fout.write(bin + '\n')

if __name__=='__main__':
    main()
