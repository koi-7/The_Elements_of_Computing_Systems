#!/usr/bin/python3
# coding: utf-8

class SymbolTable:
    def __init__(self):
        '''
        空のシンボルテーブルを作成する
        void -> void
        '''
        self.table = {
            'SP':     0,
            'LCL':    1,
            'ARG':    2,
            'THIS':   3,
            'THAT':   4,
            'R0':     0,
            'R1':     1,
            'R2':     2,
            'R3':     3,
            'R4':     4,
            'R5':     5,
            'R6':     6,
            'R7':     7,
            'R8':     8,
            'R9':     9,
            'R10':    10,
            'R11':    11,
            'R12':    12,
            'R13':    13,
            'R14':    14,
            'R15':    15,
            'SCREEN': 16384,
            'KBD':    24576,
        }

    def addEntry(self, symbol, address):
        '''
        テーブルに (symbol, address) のペアを追加する
        str, int -> void
        '''
        self.table[symbol] = address

    def contains(self, symbol):
        '''
        シンボルテーブルは与えられた symbol を含むか？
        str -> bool
        '''
        return symbol in self.table

    def getAddress(self, symbol):
        '''
        symbol に結びつけられたアドレスを返す
        str -> int
        '''
        return self.table[symbol]
