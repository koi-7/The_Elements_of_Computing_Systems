#!/usr/bin/python3
# coding: utf-8

class VMWriter:
    def __init__(self):
        """
        新しいファイルを作り、それに書き込む準備をする
        void -> void
        """
        pass

    def writePush(self, segment, index):
        """
        push コマンドを書く
        CONST | ARG | LOCAL | STATIC | THIS | THAT | POINTER | TEMP, int -> void
        """
        pass

    def writePop(self, segment, index):
        """
        pop コマンドを書く
        CONST | ARG | LOCAL | STATIC | THIS | THAT | POINTER | TEMP, int -> void
        """
        pass

    def writeArithmetic(self, command):
        """
        算術コマンドを書く
        ADD | SUB | NEG | EQ | GT | LT | AND | OR | NOT -> void
        """
        pass

    def writeLabel(self, label):
        """
        label コマンドを書く
        str -> void
        """
        pass

    def writeGoto(self, label):
        """
        goto コマンドを書く
        str -> void
        """
        pass

    def writeIf(self, label):
        """
        If-goto コマンドを書く
        str -> void
        """
        pass

    def writeCall(self, name, nArgs):
        """
        call コマンドを書く
        str, int -> void
        """
        pass

    def writeFunction(self, name, nLocals):
        """
        function コマンドを書く
        str, int -> void
        """
        pass

    def writeReturn(self):
        """
        return コマンドを書く
        void -> void
        """
        pass

    def close(self):
        """
        出力ファイルを閉じる
        void -> void
        """
        pass
