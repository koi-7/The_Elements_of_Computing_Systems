#!/usr/bin/python3
# coding: utf-8

import sys, os
import Parser as ps
import Code as cd
import SymbolTable as st

START_ADDRESS = 16

def main():
    filename = sys.argv[1]
    outfile = os.path.splitext(filename)[0] + '.hack'

    t = st.SymbolTable()
    address_counter = START_ADDRESS

    ## 1 周目（シンボルテーブルの作成）
    with ps.Parser(filename) as p:
        while p.hasMoreCommands():
            p.advance()
            if p.commandType() != ps.C_COMMAND:
                s = p.symbol()
                if (not str.isdecimal(s)) & (not t.contains(s)):
                    t.addEntry(s, address_counter)
                    address_counter += 1

    print(t.table)
    exit()
    ########## とりあえずここまで ##########

    ## 2 周目（.hack ファイルの生成）
    with open(outfile, 'wt') as fout:
        with ps.Parser(filename) as p:
            while p.hasMoreCommands():
                p.advance()
                print('command: ' + p.command + ' (type: ' + str(p.commandType()) + ')')
                if p.commandType() != ps.C_COMMAND:  ## @Xxx or (Xxx)
                    s = p.symbol()
                    if s.isdecimal():  ## 定数
                        bin = format(int(s), '016b')
                    else:              ## シンボル
                        bin = format(t.getAddress(s), '016b')
                else:                                ## C 命令
                    bin_comp = cd.Code().comp(p.comp())
                    bin_dest = cd.Code().dest(p.dest())
                    bin_jump = cd.Code().jump(p.jump())
                    bin = '111' + bin_comp + bin_dest + bin_jump
                print('bin:     ' + bin)
                print('')
                fout.write(bin + '\n')

if __name__=='__main__':
    main()
