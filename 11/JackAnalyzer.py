#!/usr/bin/python3
# coding: utf-8

import sys, os, glob
import CompilationEngine as CE

def main():
    # ファイル名処理
    path = sys.argv[1]

    if os.path.isfile(path):
        input_file_list = [sys.argv[1]]
    else:
        if path[-1] != '/':
            path = path + '/'
        input_file_list = glob.glob(path + '*.jack')

    # パース
    for input_file in input_file_list:
        output_file = input_file.replace('.jack', '.vm')
        c = CE.CompilationEngine(input_file, output_file)

        # トークンリストの作成
        c.j.make_token_list()

        if c.j.hasMoreTokens():
            c.j.advance()

        if c.j.token == 'class':
            c.compileClass()

        c.j.f.close()
        # c.fout.close()
        c.v.close()

    # print('')
    # print('')
    # print('')
    # print(c.s.tables[1])
    # print('')
    # print('')
    # print('')

if __name__=='__main__':
    main()
