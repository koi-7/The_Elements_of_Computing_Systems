#!/usr/bin/python3
# coding: utf-8

NONE   = 'none'
STATIC = 'static'
FIELD  = 'field'
ARG    = 'arg'
VAR    = 'var'

class SymbolTable:
    def __init__(self):
        """
        空のシンボルテーブルを生成する
        void -> void
        """
        self.tables = [{}, {}]  ## [{サブルーチンのスコープ}, {クラスのスコープ}]
        self.count = {
            'static': 0,
            'field': 0,
            'arg': 0,
            'var': 0,
        }

    def startSubroutine(self):
        """
        新しいサブルーチンのスコープを開始する
        つまり、サブルーチンのシンボルテーブルをリセットする
        void -> void
        """
        self.tables[0] = {}
        self.count['arg'] = 0
        self.count['var'] = 0

    def define(self, name, type, kind):
        """
        引数の名前、型、属性で指定された新しい識別子を定義し、
        それに実行インデックスを割り当てる
        str, str, STATIC | FIELD | ARG | VAR -> void
        """
        if kind == STATIC:
            self.tables[1][name] = (type, 'static', self.count['static'])
            self.count['static'] += 1
        elif kind == FIELD:
            self.tables[1][name] = (type, 'field', self.count['field'])
            self.count['field'] += 1
        elif kind == ARG:
            self.tables[0][name] = (type, 'arg', self.count['arg'])
            self.count['arg'] += 1
        elif kind == VAR:
            self.tables[0][name] = (type, 'var', self.count['var'])
            self.count['var'] += 1


    def varCount(self, kind):
        """
        引数で与えられた属性について、それが現在のスコープで
        定義されている数を返す
        STATIC | FIELD | ARG | VAR -> int
        """
        return self.count[kind]

    def kindOf(self, name):
        """
        引数で与えられた名前の識別子を現在のスコープで探し、その属性を返す
        str -> STATIC | FIELD | ARG | VAR | NONE
        """
        for table in self.tables:
            for key in table.keys():
                if name == key:
                    return table[key][1]

        return NONE


    def typeOf(self, name):
        """
        引数で与えられた名前の識別子を現在のスコープで探し、その型を返す
        str -> str
        """
        for table in self.tables:
            for key in table.keys():
                if name == key:
                    return table[key][0]

    def indexOf(self, name):
        """
        引数で与えられた名前の識別子を現在のスコープで探し、そのインデックスを返す
        str -> int
        """
        for table in self.tables:
            for key in table.keys():
                if name == key:
                    return table[key][2]
