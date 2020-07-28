#!/usr/bin/python3
# coding: utf-8

import sys, os
import Parser as ps
import Code as cd
import SymbolTable as st

ROM_ADDRESS = 0
RAM_ADDRESS = 16

def main():
    filename = sys.argv[1]
    outfile = os.path.splitext(filename)[0] + '.hack'

    t = st.SymbolTable()
    rom_counter = ROM_ADDRESS

    ## 1 周目（シンボルテーブルの作成）
    with ps.Parser(filename) as p:
        while p.hasMoreCommands():
            p.advance()
            if p.commandType() == ps.L_COMMAND:
                t.table[p.symbol()] = rom_counter
            else:
                rom_counter += 1

    ## 2 周目（.hack ファイルの生成）
    ram_counter = RAM_ADDRESS

    with open(outfile, 'wt') as fout:
        with ps.Parser(filename) as p:
            while p.hasMoreCommands():
                p.advance()

                if p.commandType() == ps.A_COMMAND:    ## @Xxx
                    s = p.symbol()
                    if s.isdecimal():  ## @123
                        bin = format(int(s), '016b')
                    else:              ## @VAR
                        if t.contains(s):
                            bin = format(t.getAddress(s), '016b')
                        else:
                            t.addEntry(s, ram_counter)
                            bin = format(ram_counter, '016b')
                            ram_counter += 1
                elif p.commandType() == ps.L_COMMAND:  ## (Xxx)
                    continue
                else:                                  ## C 命令
                    bin_comp = cd.Code().comp(p.comp())
                    bin_dest = cd.Code().dest(p.dest())
                    bin_jump = cd.Code().jump(p.jump())
                    bin = '111' + bin_comp + bin_dest + bin_jump

                fout.write(bin + '\n')

if __name__=='__main__':
    main()
