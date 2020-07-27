#!/usr/bin/python3
# coding: utf-8

import sys, os
import Parser as ps
import Code as cd

def main():
    filename = sys.argv[1]
    outfile = os.path.splitext(filename)[0] + '.hack'

    with open(outfile, 'wt') as fout:
        with ps.Parser(filename) as p:
            while p.hasMoreCommands():
                p.advance()
                print('command: ' + p.command + ' (type: ' + str(p.commandType()) + ')')
                if p.commandType() != ps.C_COMMAND:          ## @Xxx or (Xxx)
                    s = p.symbol()
                    if True:          ## 定数
                        bin = format(int(s), '016b')
                    else:             ## シンボル
                        pass
                else:                                        ## C 命令
                    bin_comp = cd.Code().comp(p.comp())
                    bin_dest = cd.Code().dest(p.dest())
                    bin_jump = cd.Code().jump(p.jump())
                    bin = '111' + bin_comp + bin_dest + bin_jump
                print('bin:     ' + bin)
                print('')
                fout.write(bin + '\n')

if __name__=='__main__':
    main()
