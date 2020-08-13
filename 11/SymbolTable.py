#!/usr/bin/python3
# coding: utf-8

NONE   = 0
STATIC = 1
FIELD  = 2
ARG    = 3
VAR    = 4

class SymbolTable:
    def __init__(self):
        """
        空のシンボルテーブルを生成する
        void -> void
        """
        self.tables = [{}, {}]  ## [{サブルーチンのスコープ}, {クラスのスコープ}]
        self.static_count = 0
        self.field_count = 0
        self.arg_count = 0
        self.var_count = 0

    def startSubroutine(self):
        """
        新しいサブルーチンのスコープを開始する
        つまり、サブルーチンのシンボルテーブルをリセットする
        void -> void
        """
        self.tables[0] = {}
        self.arg_count = 0
        self.var_count = 0

    def define(self, name, type, kind):
        """
        引数の名前、型、属性で指定された新しい識別子を定義し、
        それに実行インデックスを割り当てる
        str, str, STATIC | FIELD | ARG | VAR -> void
        """
        if kind == STATIC:
            self.tables[1][name] = (type, kind, self.static_count)
            self.static_count += 1
        elif kind == FIELD:
            self.tables[1][name] = (type, kind, self.field_count)
            self.field_count += 1
        elif kind == ARG:
            self.tables[0][name] = (type, kind, self.arg_count)
            self.arg_count += 1
        elif kind == VAR:
            self.tables[0][name] = (type, kind, self.var_count)
            self.arg_count += 1


    def varCount(self, kind):
        """
        引数で与えられた属性について、それが現在のスコープで
        定義されている数を返す
        STATIC | FIELD | ARG | VAR -> int
        """
        if kind == STATIC:
            return self.static_count
        elif kind == FIELD:
            return self.field_count
        elif kind == ARG:
            return self.arg_count
        elif kind == VAR:
            return self.var_count

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
