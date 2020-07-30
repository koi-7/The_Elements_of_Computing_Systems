#!/usr/bin/python3
# coding: utf-8

import sys, os
import Parser as ps
import CodeWriter as cw

def main():
    filename = sys.argv[1]
    outfile = os.path.splitext(filename)[0] + '.asm'
    with ps.Parser(filename) as p:
        c = cw.CodeWriter(outfile)
        while p.hasMoreCommands():
            p.advance()
            if p.commandType() == ps.C_PUSH:
                c.writePushPop(ps.C_PUSH, p.arg1(), p.arg2())
            elif p.commandType() == ps.C_POP:
                c.writePushPop(ps.C_POP, p.arg1(), p.arg2())
            elif p.commandType() == ps.C_ARITHMETIC:
                c.writeArithmetic(p.command)

if __name__=='__main__':
    main()
