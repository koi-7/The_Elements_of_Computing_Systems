#!/usr/bin/python3
# coding: utf-8

import sys, os, glob
import Parser as ps
import CodeWriter as cw

def main():
    path = sys.argv[1]

    if os.path.isfile(path):
        file_list = [sys.argv[1]]
        output_file = os.path.splitext(path)[0] + '.asm'
    else:
        if path[-1] != '/':
            path = path + '/'
        file_list = glob.glob(path + '*.vm')
        output_file = path + path.split('/')[-2] + '.asm'
        ## Sys.vm を file_list の先頭に
        index_of_sys = file_list.index(path + 'Sys.vm')
        file_list[0], file_list[index_of_sys] = \
            file_list[index_of_sys], file_list[0]

    c = cw.CodeWriter(output_file)
    iter_counter = 0

    print(file_list)

    for file in file_list:
        c.setFileName(file)
        if iter_counter == 0:  ## 初回だけ writeInit() を呼ぶ
            c.writeInit()
            iter_counter += 1
        with ps.Parser(file) as p:
            while p.hasMoreCommands():
                p.advance()

                c.f.write('\n')

                if p.commandType() == ps.C_ARITHMETIC:
                    c.writeArithmetic(p.command)
                elif p.commandType() == ps.C_PUSH:
                    c.writePushPop(ps.C_PUSH, p.arg1(), p.arg2())
                elif p.commandType() == ps.C_POP:
                    c.writePushPop(ps.C_POP, p.arg1(), p.arg2())
                elif p.commandType() == ps.C_LABEL:
                    c.writeLabel(p.arg1())
                elif p.commandType() == ps.C_GOTO:
                    c.writeGoto(p.arg1())
                elif p.commandType() == ps.C_IF:
                    c.writeIf(p.arg1())
                elif p.commandType() == ps.C_CALL:
                    c.writeCall(p.arg1(), p.arg2())
                elif p.commandType() == ps.C_RETURN:
                    c.writeReturn()
                elif p.commandType() == ps.C_FUNCTION:
                    c.writeFunction(p.arg1(), p.arg2())

    c.close()

if __name__=='__main__':
    main()
