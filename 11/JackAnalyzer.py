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

    print(input_file_list)
    # パース
    for input_file in input_file_list:
        output_file = input_file.replace('.jack', '.xml')
        c = CE.CompilationEngine(input_file, output_file)

        # トークンリストの作成
        c.j.make_token_list()

        if c.j.hasMoreTokens():
            c.j.advance()

        if c.j.token == 'class':
            c.compileClass()

        c.j.f.close()
        c.fout.close()

if __name__=='__main__':
    main()
