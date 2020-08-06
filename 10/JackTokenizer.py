#!/usr/bin/python3
# coding: utf-8

import re

KEYWORD      = 0
SYMBOL       = 1
IDENTIFIER   = 2
INT_CONST    = 3
STRING_CONST = 4

CLASS       = 5
METHOD      = 6
FUNCTION    = 7
CONSTRUCTOR = 8
INT         = 9
BOOLEAN     = 10
CHAR        = 11
VOID        = 12
VAR         = 13
STATIC      = 14
FIELD       = 15
LET         = 16
DO          = 17
IF          = 18
ELSE        = 19
WHILE       = 20
RETURN      = 21
TRUE        = 22
FALSE       = 23
NULL        = 24
THIS        = 25

keyword_dict = {
    'class': CLASS, 'constructor': CONSTRUCTOR, 'function': FUNCTION,
    'method': METHOD, 'field': FIELD, 'static': STATIC, 'var': VAR, 'int': INT,
    'char': CHAR, 'boolean': BOOLEAN, 'void': VOID, 'true': TRUE, 'false': FALSE,
    'null': NULL, 'this': THIS, 'let': LET, 'do': DO, 'if': IF, 'else': ELSE,
    'while': WHILE, 'return': RETURN,
}

symbol_set = {
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
    '-', '*', '/', '&', '|', '<', '>', '=', '~'
}

class JackTokenizer:
    def __init__(self, input_file):
        '''
        入力ファイル / ストリームを開き、トークン化を行う準備をする
        str -> void
        '''
        self.token = ''
        self.token_list = []
        self.f = open(input_file, 'rt')


    def hasMoreTokens(self):
        '''
        入力にまだトークンは存在するか？
        void -> bool
        '''
        API_comment = False

        while True:
            self.token_list = []
            line = self.f.readline()
            if line == '':                     ## ファイルの終端
                return False
            elif re.match(r'^\s*\n$|^\s*//.*\n$|^\s*/\*\*.*\*/\s*\n$', line):  ## 改行のみもしくはコメントのみ
                continue
            elif re.match(r'^\s*/\*\*.*\n', line):  ## API コメントの始まり
                API_comment = True
                continue
            elif re.match(r'.*\*/$', line):  ## API コメントの終わり
                API_comment = False
                continue
            elif API_comment:  ## API コメントの途中
                continue
            else:                ## コメントを含むかもしれないその他の行
                # コメントと改行の除去
                line = line.split('//')[0]
                line = line.strip()

                # トークンリストを作る
                list = line.split('"')
                if len(list) == 3:
                    list[1] = '"' + list[1] + '"'
                    token_list_left = self.make_token_list(list[0])
                    token_list_right = self.make_token_list(list[2])
                    self.token_list = token_list_left + [list[1]] + token_list_right
                else:
                    self.token_list = self.make_token_list(list[0])

                # リストから余分な要素を削除
                while '' in self.token_list:
                    self.token_list.remove('')
                while ' ' in self.token_list:
                    self.token_list.remove(' ')

                return True

    def advance(self):
        '''
        入力から次のトークンを取得し、それを現在のトークンとする
        hasMoreTokens が True の場合のみ呼び出すことができる
        void -> void
        '''
        self.token = self.token_list.pop(0)

    def tokenType(self):
        '''
        現トークンの種類を返す
        void -> KEYWORD | SYMBOL | IDENTIFIER | INT_CONST | STRING_CONST
        '''
        if self.token in keyword_dict:
            return KEYWORD
        elif self.token in symbol_set:
            return SYMBOL
        elif self.token.isdecimal():
            return INT_CONST
        elif self.token[0] == '"':
            return STRING_CONST
        else:
            return IDENTIFIER

    def keyWord(self):
        '''
        現トークンのキーワードを返す
        tokenType() が KEYWORD の場合のみ呼び出すことができる
        void -> CLASS | METHOD | FUNCTION | CONSTRUCTOR | INT | BOOLEAN | CHAR |
                VOID | VAR | STATIC | FIELD | LET | DO | IF | ELSE | WHILE |
                RETURN | TRUE | FALSE | NULL | THIS
        '''
        return keyword_dict[self.token]

    def symbol(self):
        '''
        現トークンの文字を返す
        tokenType() が SYMBOL の場合のみ呼び出すことができる
        void -> str
        '''
        s = self.token
        if s == '<':
            s = '&lt;'
        elif s == '>':
            s = '&gt;'
        elif s == '&':
            s = '&amp;'
        return s

    def identifier(self):
        '''
        現トークンの識別子を返す
        tokenType() が IDENTIFIER の場合のみ呼び出すことができる
        void -> str
        '''
        return self.token

    def intVal(self):
        '''
        現トークンの整数の値を返す
        tokenType() が INT_CONST の場合のみ呼び出すことができる
        void -> int
        '''
        return int(self.token)

    def stringVal(self):
        '''
        現トークンの文字列を返す
        tokenType() が STRING_CONST の場合のみ呼び出すことができる
        void -> str
        '''
        return self.token.strip('"')

    def make_token_list(self, line):
        '''
        " を含まない文字列からトークンのリストを作成する
        str -> str list
        '''
        if line == '':
            return ['']
        elif len(line) == 1:
            return [line]

        list = []
        left = 0
        right = 1
        for char in line:
            if char == ' ' or char in symbol_set:
                list.append(line[left:right-1])
                list.append(char)
                left = right
                right = left + 1
            else:
                right += 1

        return list


