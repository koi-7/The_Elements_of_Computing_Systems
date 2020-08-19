#!/usr/bin/python3
# coding: utf-8

CONST   = 'constant'
ARG     = 'argument'
LOCAL   = 'local'
STATIC  = 'static'
THIS    = 'this'
THAT    = 'that'
POINTER = 'pointer'
TEMP    = 'temp'

ADD = 'add'
SUB = 'sub'
NEG = 'neg'
EQ  = 'eq'
GT  = 'gt'
LT  = 'lt'
AND = 'and'
OR  = 'or'
NOT = 'not'

class VMWriter:
    def __init__(self, output_file):
        """
        新しいファイルを作り、それに書き込む準備をする
        void -> void
        """
        self.f = open(output_file, 'wt')

    def writePush(self, segment, index):
        """
        push コマンドを書く
        CONST | ARG | LOCAL | STATIC | THIS | THAT | POINTER | TEMP, int -> void
        """
        self.f.write('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        """
        pop コマンドを書く
        CONST | ARG | LOCAL | STATIC | THIS | THAT | POINTER | TEMP, int -> void
        """
        self.f.write('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        """
        算術コマンドを書く
        ADD | SUB | NEG | EQ | GT | LT | AND | OR | NOT -> void
        """
        self.f.write(command + '\n')

    def writeLabel(self, label):
        """
        label コマンドを書く
        str -> void
        """
        self.f.write('label ' + label + '\n')

    def writeGoto(self, label):
        """
        goto コマンドを書く
        str -> void
        """
        self.f.write('goto ' + label + '\n')

    def writeIf(self, label):
        """
        If-goto コマンドを書く
        str -> void
        """
        self.f.write('if-goto ' + label + '\n')

    def writeCall(self, name, nArgs):
        """
        call コマンドを書く
        str, int -> void
        """
        self.f.write('call ' + name + ' ' + str(nArgs) + '\n')

    def writeFunction(self, name, nLocals):
        """
        function コマンドを書く
        str, int -> void
        """
        self.f.write('function ' + name + ' ' + str(nLocals) + '\n')

    def writeReturn(self):
        """
        return コマンドを書く
        void -> void
        """
        self.f.write('return' + '\n')

    def close(self):
        """
        出力ファイルを閉じる
        void -> void
        """
        self.f.close()
