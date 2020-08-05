#!/usr/bin/python3
# coding: utf-8

import sys, os, glob
import JackTokenizer as jt
import CompilationEngine as ce

def main():
    path = sys.argv[1]

    if os.path.isfile(path):
        file_list = [sys.argv[1]]
    else:
        if path[-1] != '/':
            path = path + '/'
        file_list = glob.glob(path + '*.jack')

    for input_file in file_list:
        j = jt.JackTokenizer(input_file)
        output_file = input_file.replace('.jack', 'T.xml')
        fout = open(output_file, 'wt')

        fout.write('<tokens>' + '\n')

        while j.hasMoreTokens():
            while j.token_list:
                j.advance()
                if j.tokenType() == jt.KEYWORD:
                    fout.write('<keyword> ' + j.token + ' </keyword>' + '\n')
                elif j.tokenType() == jt.SYMBOL:
                    symbol = j.token
                    if symbol == '<':
                        symbol = '&lt;'
                    elif symbol == '>':
                        symbol = '&gt;'
                    elif symbol == '&':
                        symbol = '&amp;'
                    fout.write('<symbol> ' + symbol + ' </symbol>' + '\n')
                elif j.tokenType() == jt.IDENTIFIER:
                    fout.write('<identifier> ' + j.token + ' </identifier>' + '\n')
                elif j.tokenType() == jt.INT_CONST:
                    fout.write('<integerConstant> ' + j.token + ' </integerConstant>' + '\n')
                elif j.tokenType() == jt.STRING_CONST:

                    fout.write('<stringConstant> ' + j.token.split('"')[1] + ' </stringConstant>' + '\n')

        fout.write('</tokens>' + '\n')

        j.f.close()
        fout.close()

if __name__=='__main__':
    main()
