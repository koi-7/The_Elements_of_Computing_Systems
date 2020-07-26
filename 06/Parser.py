#!/usr/bin/python3
# coding: utf-8

class Parser:
    def __init__(self, filename):
        pass

    def hasMoreCommands(self):
        '''
        入力にまだコマンドが存在するか？
        in:  void
        out: bool
        '''
        pass

    def advance(self):
        '''
        入力から次のコマンドを読み、それを現在のコマンドにする
        in:  void
        out: void
        '''
        pass

    def commandType(self):
        '''
       現コマンドの種類を返す
        in:  void
        out: COMMAND
        '''
        pass

    def symbol(self):
        '''
        現コマンドのシンボルを返す
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
