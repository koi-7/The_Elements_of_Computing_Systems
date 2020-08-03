#!/usr/bin/python3
# coding: utf-8

import re

C_ARITHMETIC = 0
C_PUSH       = 1
C_POP        = 2
C_LABEL      = 3
C_GOTO       = 4
C_IF         = 5
C_CALL       = 6
C_RETURN     = 7
C_FUNCTION   = 8

class Parser:
    def __init__(self, filename):
        '''
        入力ファイル / ストリームを開きパースを行う準備をする
        str -> void
        '''
        self.command = ''
        self.f = open(filename, 'rt')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()

    def hasMoreCommands(self):
        '''
        入力にまだコマンドが存在するか？
        void -> bool
        '''
        while True:
            line = self.f.readline()
            if line == '':
                return False
            elif re.match(r'^\n$|^/{2}', line):
                continue
            else:
                self.command = line
                return True

    def advance(self):
        '''
        入力から次のコマンドを読み、それを現在のコマンドにする
        void -> void
        '''
        line = self.command.split('//')[0]  ## コメント除去
        self.command = line.strip()         ## 改行除去

    def commandType(self):
        '''
        現 VM コマンドの種類を返す
        void -> str
        '''
        command_elems = self.command.split(' ')

        if command_elems[0] == 'push':
            return C_PUSH
        elif command_elems[0] == 'pop':
            return C_POP
        elif command_elems[0] == 'label':
            return C_LABEL
        elif command_elems[0] == 'goto':
            return C_GOTO
        elif command_elems[0] == 'if-goto':
            return C_IF
        elif command_elems[0] == 'call':
            return C_CALL
        elif command_elems[0] == 'return':
            return C_RETURN
        elif command_elems[0] == 'function':
            return C_FUNCTION
        else:
            return C_ARITHMETIC

    def arg1(self):
        '''
        現コマンドの最初の引数が返される
        void -> str
        '''
        command_list = self.command.split(' ')
        return command_list[1]

    def arg2(self):
        '''
        現コマンドの2番目の引数が返される
        void -> int
        '''
        command_list = self.command.split(' ')
        return int(command_list[2])


