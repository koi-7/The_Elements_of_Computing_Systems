#!/usr/bin/python3
# coding: utf-8

class SymbolTable:
    def __init__(self):
        '''
        空のシンボルテーブルを生成する
        void -> void
        '''
        pass

    def startSubroutine(self):
        '''
        新しいサブルーチンのスコープか開始する
        つまり、サブルーチンのシンボルテーブルをリセットする
        void -> void
        '''
        pass

    def define(self, name, type, kind):
        '''
        引数の名前、型、属性でしてされた新しい識別子を定義し、
        それに実行インデックスを割り当てる
        str, str, STATIC | FIELD | ARG | VAR -> void
        '''
        pass

    def varCount(self, kind):
        '''
        引数で与えられた属性について、それが現在のスコープで
        定義されている数を返す
        STATIC | FIELD | ARG | VAR -> int
        '''
        pass

    def kindOf(self, name):
        '''
        引数で与えられた名前の識別子を現在のスコープで探し、その属性を返す
        str -> STATIC | FIELD | ARG | VAR | NONE
        '''
        pass

    def typeOf(self, name):
        '''
        引数で与えられた名前の識別子を現在のスコープで探し、その型を返す
        str -> str
        '''
        pass

    def indexOf(self, name):
        '''
        引数で与えられた名前の識別子を現在のスコープで探し、そのインデックスを返す
        str -> int
        '''
        pass
