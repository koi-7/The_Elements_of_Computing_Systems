#!/usr/bin/python3
# coding: utf-8

class JackTokenizer:
    def __init__(self, input_file):
        '''
        入力ファイル / ストリームを開き、トークン化を行う準備をする
        str -> void
        '''
        pass

    def hasMoreTokens(self):
        '''
        入力にまだトークンは存在するか？
        void -> bool
        '''
        pass

    def advance(self):
        '''
        入力から次のトークンを取得し、それを現在のトークンとする
        hasMoreTokens が True の場合のみ呼び出すことができる
        void -> void
        '''
        pass

    def tokenType(self):
        '''
        現トークンの種類を返す
        void -> KEYWORD | SYMBOL | IDENTIFIER | INT_CONST | STRING_CONST
        '''
        pass

    def keyWord(self):
        '''
        現トークンのキーワードを返す
        tokenType() が KEYWORD の場合のみ呼び出すことができる
        void -> CLASS | METHOD | FUNCTION | CONSTRUCTOR | INT | BOOLEAN | CHAR |
                VOID | VAR | STATIC | FIELD | LET | DO | IF | ELSE | WHILE |
                RETURN | TRUE | FALSE | NULL | THIS
        '''
        pass

    def symbol(self):
        '''
        現トークンの文字を返す
        tokenType() が SYMBOL の場合のみ呼び出すことができる
        void -> str
        '''
        pass

    def identifier(self):
        '''
        現トークンの識別子を返す
        tokenType() が IDENTIFIER の場合のみ呼び出すことができる
        void -> str
        '''
        pass

    def intVal(self):
        '''
        現トークンの整数の値を返す
        tokenType() が INT_CONST の場合のみ呼び出すことができる
        void -> int
        '''
        pass

    def stringVal(self):
        '''
        現トークンの文字列を返す
        tokenType() が STRING_CONST の場合のみ呼び出すことができる
        void -> str
        '''
        pass
