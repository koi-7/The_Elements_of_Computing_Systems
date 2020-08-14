#!/usr/bin/python3
# coding: utf-8

import JackTokenizer as JT
import SymbolTable as ST
import VMWriter as VMW

class CompilationEngine:
    def __init__(self, input_file, output_file):
        """
        与えられた入力と出力に対して新しいコンパイルエンジンを生成する
        次に呼ぶルーチンは compileClass() でなければならない
        str, str -> void
        """
        self.j = JT.JackTokenizer(input_file)
        self.v = VMW.VMWriter(output_file)
        self.s = ST.SymbolTable()

    def compileClass(self):
        """
        クラスをコンパイルする
        void -> void
        """
        self.next()           ## 'class'
        self.next()# self.write_xml()           ## className
        self.next()           ## '{'
        self.compileClassVarDec()  ## classVarDec*
        self.compileSubroutine()   ## subroutineDec*
        self.next()           ## '}'

    def compileClassVarDec(self):
        """
        スタティック宣言またはフィールド宣言をコンパイルする
        void -> void
        """
        # classVarDec 0個
        if self.j.token != 'static' and self.j.token != 'field':
            pass

        # classVarDec 1個以上
        else:
            while self.j.token == 'static' or self.j.token == 'field':
                if self.j.token == 'static':
                    kind = ST.STATIC
                elif self.j.token == 'field':
                    kind = ST.FIELD
                self.next()
                type = self.j.token            ## type
                self.next()
                self.s.define(self.j.token, type, kind)            ## varName
                self.next()
                while self.j.token == ',':
                    self.next()        ## ','
                    self.s.define(self.j.token, type, kind)        ## varName
                    self.next()
                self.next()            ## ';'

    def compileSubroutine(self):
        """
        メソッド、ファンクション、コンストラクタをコンパイルする
        void -> void
        """
        # subroutineDec
        ## subroutineDec なし
        if self.j.token == '}':
            pass
        ## subroutineDec あり
        elif self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
            while self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
                self.next()             ## constructor or function or method
                self.write_xml()             ## 'void' | type
                self.write_xml()             ## subroutineName
                self.write_xml()             ## '('
                self.compileParameterList()  ## parameterList
                self.write_xml()             ## ')'
                self.compileSubroutine()     ## subroutineBody

        # subroutineBody
        elif self.j.token == '{':
            self.write_xml()          ## '{'
            self.compileVarDec()      ## varDec*
            self.compileStatements()  ## statements
            self.write_xml()          ## '}'

        # subroutineCall
        elif self.j.token_list[0] == '(' or self.j.token_list[0] == '.':
            if self.j.token_list[0] == '.':
                self.write_xml()          ## className | varName
                self.write_xml()          ## '.'
            self.write_xml()              ## subroutineName
            self.write_xml()              ## '('
            self.compileExpressionList()  ## expressionList
            self.write_xml()              ## ')'

    def compileParameterList(self):
        """
        パラメータのリストをコンパイルする
        () は含まない
        void -> void
        """
        pass

        # # 引数なし
        # if self.j.token == ')':
        #     pass

        # # 引数あり
        # else:
        #     self.write_xml()            ## type
        #     self.write_xml()            ## varName
        #     while self.j.token == ',':
        #         self.write_xml()        ## ','
        #         self.write_xml()        ## type
        #         self.write_xml()        ## varName


    def compileVarDec(self):
        """
        var 宣言をコンパイルする
        void -> void
        """
        pass
        # # varDec 0個
        # if self.j.token != 'var':
        #     pass

        # # varDec 1個以上
        # else:
        #     while self.j.token == 'var':
        #         self.write_xml()            ## 'var'
        #         self.write_xml()            ## type
        #         self.write_xml()            ## varName
        #         while self.j.token == ',':
        #             self.write_xml()        ## ','
        #             self.write_xml()        ## varName
        #         self.write_xml()            ## ';'

    def compileStatements(self):
        """
        一連の文をコンパイルする
        {} は含まない
        void -> void
        """
        pass

        # while self.j.token == 'let' or self.j.token == 'if' or self.j.token == 'while' or self.j.token == 'do' or self.j.token == 'return':
        #     if self.j.token == 'let':
        #         self.compileLet()     ## letStatement

        #     elif self.j.token == 'if':
        #         self.compileIf()      ## ifStatement

        #     elif self.j.token == 'while':
        #         self.compileWhile()   ## whileStatement

        #     elif self.j.token == 'do':
        #         self.compileDo()      ## doStatement

        #     elif self.j.token == 'return':
        #         self.compileReturn()  ## returnStatement

    def compileDo(self):
        """
        do 文をコンパイルする
        void -> void
        """
        pass
        # self.write_xml()          ## 'do'
        # self.compileSubroutine()  ## subroutineCall
        # self.write_xml()          ## ';'

    def compileLet(self):
        """
        let 文をコンパイルする
        void -> void
        """
        pass
        # self.write_xml()              ## 'let'
        # self.write_xml()              ## varName
        # if self.j.token == '[':
        #     self.write_xml()          ## '['
        #     self.compileExpression()  ## expression
        #     self.write_xml()          ## ']'
        # self.write_xml()              ## '='
        # self.compileExpression()      ## expression
        # self.write_xml()              ## ';'

    def compileWhile(self):
        """
        while 文をコンパイルする
        void -> void
        """
        pass
        # self.write_xml()          ## 'while'
        # self.write_xml()          ## '('
        # self.compileExpression()  ## expression
        # self.write_xml()          ## ')'
        # self.write_xml()          ## '{'
        # self.compileStatements()  ## statements
        # self.write_xml()          ## '}'

    def compileReturn(self):
        """
        return 文をコンパイルする
        void -> void
        """
        pass
        # self.write_xml()              ## 'return'
        # if self.j.token != ';':
        #     self.compileExpression()  ## expression
        # self.write_xml()              ## ';'

    def compileIf(self):
        """
        if 文をコンパイルする
        else 文を伴う可能性がある
        void -> void
        """
        pass
        # self.write_xml()              ## 'if'
        # self.write_xml()              ## '('
        # self.compileExpression()      ## expression
        # self.write_xml()              ## ')'
        # self.write_xml()              ## '{'
        # self.compileStatements()      ## statements
        # self.write_xml()              ## '}'
        # if self.j.token == 'else':
        #     self.write_xml()          ## 'else'
        #     self.write_xml()          ## '{'
        #     self.compileStatements()  ## statements
        #     self.write_xml()          ## '}'

    def compileExpression(self):
        """
        式をコンパイルする
        void -> void
        """
        pass
        # op_set = {'+', '-', '*', '/', '&', '|', '<', '>', '='}

        # self.compileTerm()             ## term
        # while self.j.token in op_set:
        #     self.write_xml()           ## op
        #     self.compileTerm()         ## term

    def compileTerm(self):
        """
        term をコンパイルする
        場合によって先読みをする必要がある
        void -> void
        """
        pass

        # if self.j.token == '(':
        #     self.write_xml()          ## '('
        #     self.compileExpression()  ## expression
        #     self.write_xml()          ## ')'

        # elif self.j.token == '-' or self.j.token == '~':
        #     self.write_xml()    ## '-' | '~'
        #     self.compileTerm()  ## term

        # elif self.j.token_list[0] == '[':
        #     self.write_xml()          ## varName
        #     self.write_xml()          ## '['
        #     self.compileExpression()  ## expression
        #     self.write_xml()          ## ']'

        # elif self.j.token_list[0] == '(' or self.j.token_list[0] == '.':
        #     self.compileSubroutine()  ## subroutineCall

        # else:
        #     self.write_xml()  ## integerConstant | stringConstant | keywordConstant | varName

    def compileExpressionList(self):
        """
        コンマで分離された式のリストをコンパイルする
        void -> void
        """
        pass

        # if self.j.token == ')':
        #     pass

        # else:
        #     self.compileExpression()      ## expression
        #     while self.j.token == ',':
        #         self.write_xml()          ## ','
        #         self.compileExpression()  ## expression

    def write_xml(self):
        """
        トークンのタイプを見て xml に書き込みを行う
        書き込み後は次のトークンに進む
        void -> void
        """
        pass
        # xml_str = ''

        # if self.j.tokenType() == jt.KEYWORD:
        #     key = [k for k, v in jt.keyword_dict.items() if v == self.j.keyWord()]
        #     xml_str = '<keyword> ' + key[0] + ' </keyword>'
        # elif self.j.tokenType() == jt.SYMBOL:
        #     xml_str = '<symbol> ' + self.j.symbol() + ' </symbol>'
        # elif self.j.tokenType() == jt.IDENTIFIER:
        #     xml_str = '<identifier> ' + self.j.identifier() + ' </identifier>'
        # elif self.j.tokenType() == jt.INT_CONST:
        #     xml_str = '<integerConstant> ' + str(self.j.intVal()) + ' </integerConstant>'
        # elif self.j.tokenType() == jt.STRING_CONST:
        #     xml_str = '<stringConstant> ' + self.j.stringVal() + ' </stringConstant>'

        # self.fout.write(xml_str + '\n')

        # if self.j.hasMoreTokens():
        #     self.j.advance()

    def next(self):
        """
        hasMoreTokens() と advance() を同時に行うためのメソッド
        void -> void
        """
        if self.j.hasMoreTokens():
            self.j.advance()
