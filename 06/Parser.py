#!/usr/bin/python3
# coding: utf-8

import re
import Code as cd


A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2


a_pattern = r''
c_pattern = r''
l_pattern = r''


class Parser:
    def __init__(self, filename):
        '''
        入力ファイル / ストリームを開きパースを行う準備をする
        in:  str
        out: void
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
        in:  void
        out: bool
        '''
        if self.command == '':
            return False
        else:
            return True

    def advance(self):
        '''
        入力から次のコマンドを読み、それを現在のコマンドにする
        in:  void
        out: void
        '''
        self.command = self.f.readline()

    def commandType(self):
        '''
        現コマンドの種類を返す
        in:  void
        out: A_COMMAND, C_COMMAND, L_COMMAND
        '''
        pass

    def symbol(self):
        '''
        現コマンドのシンボルもしくは10進数の数値を返す
        in:  void
        out: str
        '''
        pass

    def dest(self):
        '''
        現 C 命令の dest ニーモニックを返す
        in:  void
        out: str
        '''
        pass

    def comp(self):
        '''
        現 C 命令の comp ニーモニックを返す
        in:  void
        out: str
        '''
        pass

    def jump(self):
        '''
        現 C 命令の jump ニーモニックを返す
        in:  void
        out: str
        '''
        pass
