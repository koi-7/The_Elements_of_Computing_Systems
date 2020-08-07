#!/usr/bin/python3
# coding: utf-8

import JackTokenizer as jt

class CompilationEngine:
    def __init__(self, input_file, output_file):
        '''
        与えられた入力と出力に対して新しいコンパイルエンジンを生成する
        次に呼ぶルーチンは compileClass() でなければならない
        str, str -> void
        '''
        self.j = jt.JackTokenizer(input_file)
        self.fout = open(output_file, 'wt')

    def compileClass(self):  # checked
        '''
        クラスをコンパイルする
        void -> void
        '''
        self.fout.write('<class>' + '\n')

        self.write_xml()           ## 'class'
        self.write_xml()           ## className
        self.write_xml()           ## '{'
        self.compileClassVarDec()  ## classVarDec*
        self.compileSubroutine()   ## subroutineDec*
        self.write_xml()           ## '}'

        self.fout.write('</class>' + '\n')

    def compileClassVarDec(self):  # checked
        '''
        スタティック宣言またはフィールド宣言をコンパイルする
        void -> void
        '''
        # classVarDec 0個
        if self.j.token != 'static' and self.j.token != 'field':
            pass

        # classVarDec 1個以上
        else:
            while self.j.token == 'static' or self.j.token == 'field':
                self.fout.write('<classVarDec>' + '\n')
                self.write_xml()      ## 'static' or 'field'
                self.write_xml()      ## type
                self.write_xml()      ## varName
                while self.j.token == ',':
                    self.write_xml()  ## ','
                    self.write_xml()  ## varName
                self.write_xml()      ## ';'
                self.fout.write('</classVarDec>' + '\n')

    def compileSubroutine(self):  # checked
        '''
        メソッド、ファンクション、コンストラクタをコンパイルする
        void -> void
        '''
        # subroutineDec
        if self.j.token == '}':
            self.fout.write('<subroutineDec>' + '\n')
            self.fout.write('</subroutineDec>' + '\n')
        elif self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
            while self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
                self.fout.write('<subroutineDec>' + '\n')
                self.write_xml()  ## constructor or function or method
                self.write_xml()  ## 'void' | type
                self.write_xml()  ## subroutineName
                self.write_xml()  ## '('
                self.compileParameterList()  ## parameterList
                self.write_xml()  ## ')'
                self.compileSubroutine()  ## subroutineBody
                self.fout.write('</subroutineDec>' + '\n')

        # subroutineBody
        elif self.j.token == '{':
            self.fout.write('<subroutineBody>' + '\n')

            self.write_xml()  ## '{'
            self.compileVarDec()  ## varDec*
            self.compileStatements()  ## statements
            self.write_xml()  ## '}'

            self.fout.write('</subroutineBody>' + '\n')

        # subroutineCall
        elif self.j.token_list[0] == '(' or self.j.token_list[0] == '.':
            if self.j.token_list[0] == '.':
                self.write_xml()  ## className | varName
                self.write_xml()  ## '.'
            self.write_xml()  ## subroutineName
            self.write_xml()  ## '('
            self.compileExpressionList()  ## expressionList
            self.write_xml()  ## ')'

    def compileParameterList(self):  # checked
        '''
        パラメータのリストをコンパイルする
        () は含まない
        void -> void
        '''
        self.fout.write('<parameterList>' + '\n')

        # 引数なし
        if self.j.token == ')':
            pass

        # 引数あり
        else:
            self.write_xml()      ## type
            self.write_xml()      ## varName
            while self.j.token == ',':
                self.write_xml()  ## ','
                self.write_xml()  ## type
                self.write_xml()  ## varName

        self.fout.write('</parameterList>' + '\n')

    def compileVarDec(self):  # checked
        '''
        var 宣言をコンパイルする
        void -> void
        '''
        # varDec 0個
        if self.j.token != 'var':
            pass

        # varDec 1個以上
        else:
            while self.j.token == 'var':
                self.fout.write('<varDec>' + '\n')
                self.write_xml()      ## 'var'
                self.write_xml()      ## type
                self.write_xml()      ## varName
                while self.j.token == ',':
                    self.write_xml()  ## ','
                    self.write_xml()  ## varName
                self.write_xml()      ## ';'
                self.fout.write('</varDec>' + '\n')


    def compileStatements(self):  # checked
        '''
        一連の文をコンパイルする
        {} は含まない
        void -> void
        '''
        self.fout.write('<statements>' + '\n')

        while self.j.token == 'let' or self.j.token == 'if' or self.j.token == 'while' or self.j.token == 'do' or self.j.token == 'return':
            if self.j.token == 'let':
                self.compileLet()     ## letStatement

            elif self.j.token == 'if':
                self.compileIf()      ## ifStatement

            elif self.j.token == 'while':
                self.compileWhile()   ## whileStatement

            elif self.j.token == 'do':
                self.compileDo()      ## doStatement

            elif self.j.token == 'return':
                self.compileReturn()  ## returnStatement

        self.fout.write('</statements>' + '\n')

    def compileDo(self):  ## checked
        '''
        do 文をコンパイルする
        void -> void
        '''
        self.fout.write('<doStatement>' + '\n')
        self.write_xml()          ## 'do'
        self.compileSubroutine()  ## subroutineCall
        self.write_xml()          ## ';'

        self.fout.write('</doStatement>' + '\n')

    def compileLet(self):  ## checked
        '''
        let 文をコンパイルする
        void -> void
        '''
        self.fout.write('<letStatement>' + '\n')

        self.write_xml()              ## 'let'
        self.write_xml()              ## varName
        if self.j.token == '[':
            self.write_xml()          ## '['
            self.compileExpression()  ## expression
            self.write_xml()          ## ']'
        self.write_xml()              ## '='
        self.compileExpression()      ## expression
        self.write_xml()              ## ';'

        self.fout.write('</letStatement>' + '\n')

    def compileWhile(self):  ## checked
        '''
        while 文をコンパイルする
        void -> void
        '''
        self.fout.write('<whileStatement>' + '\n')

        self.write_xml()  ## 'while'
        self.write_xml()  ## '('
        self.compileExpression()
        self.write_xml()  ## ')'
        self.write_xml()  ## '{'
        self.compileStatements()  ## statements
        self.write_xml()  ## '}'

        self.fout.write('</whileStatement>' + '\n')

    def compileReturn(self):  ## checked
        '''
        return 文をコンパイルする
        void -> void
        '''
        self.fout.write('<returnStatement>' + '\n')

        self.write_xml()  ## 'return'
        if self.j.token != ';':
            self.compileExpression()
        self.write_xml()  ## ';'

        self.fout.write('</returnStatement>' + '\n')

    def compileIf(self):  ## checked
        '''
        if 文をコンパイルする
        else 文を伴う可能性がある
        void -> void
        '''
        self.fout.write('<ifStatement>' + '\n')

        self.write_xml()  ## 'if'
        self.write_xml()  ## '('
        self.compileExpression()
        self.write_xml()  ## ')'
        self.write_xml()  ## '{'
        self.compileStatements()
        self.write_xml()  ## '}'
        if self.j.token == 'else':
            self.write_xml()  ## 'else'
            self.write_xml()  ## '{'
            self.compileStatements()
            self.write_xml()  ## '}'

        self.fout.write('</ifStatement>' + '\n')

    def compileExpression(self):  ## checked
        '''
        式をコンパイルする
        void -> void
        '''
        op_set = {'+', '-', '*', '/', '&', '|', '<', '>', '='}

        self.fout.write('<expression>' + '\n')

        self.compileTerm()      ## term
        while self.j.token in op_set:
            self.write_xml()    ## op
            self.compileTerm()  ## term

        self.fout.write('</expression>' + '\n')

    def compileTerm(self):  ## checked
        '''
        term をコンパイルする
        場合によって先読みをする必要がある
        void -> void
        '''
        self.fout.write('<term>' + '\n')

        if self.j.token == '(':
            self.write_xml()  ## '('
            self.compileExpression()  ## expression
            self.write_xml()  ## ')'

        elif self.j.token == '-' or self.j.token == '~':
            self.write_xml()  ## '-' | '~'
            self.compileTerm()  ## term

        elif self.j.token_list[0] == '[':
            self.write_xml()  ## varName
            self.write_xml()  ## '['
            self.compileExpression()  ## expression
            self.write_xml()  ## ']'

        elif self.j.token_list[0] == '(':
            self.compileSubroutine()  ## subroutineCall

        else:
            self.write_xml()  ## integerConstant | stringConstant | keywordConstant | varName

        self.fout.write('</term>' + '\n')

    def compileExpressionList(self):  ## checled
        '''
        コンマで分離された式のリストをコンパイルする
        void -> void
        '''
        self.fout.write('<expressionList>' + '\n')

        if self.j.token == ')':
            pass

        else:
            self.compileExpression()  ## expression
            while self.j.token == ',':
                self.write_xml()  ## ','
                self.compileExpression()  ## expression

        self.fout.write('</expressionList>' + '\n')

    def write_xml(self):
        '''
        トークンのタイプを見て xml に書き込みを行う
        書き込み後は次のトークンに進む
        void -> void
        '''
        xml_str = ''

        if self.j.tokenType() == jt.KEYWORD:
            xml_str = '<keyword> ' + self.j.token + ' </keyword>'
        elif self.j.tokenType() == jt.SYMBOL:
            xml_str = '<symbol> ' + self.j.token + ' </symbol>'
        elif self.j.tokenType() == jt.IDENTIFIER:
            xml_str = '<identifier> ' + self.j.token + ' </identifier>'
        elif self.j.tokenType() == jt.INT_CONST:
            xml_str = '<integerConstant> ' + self.j.token + ' </integerConstant>'
        elif self.j.tokenType() == jt.STRING_CONST:
            xml_str = '<stringConstant> ' + self.j.token.strip('"') + ' </stringConstant>'

        self.fout.write(xml_str + '\n')

        if self.j.hasMoreTokens():
            self.j.advance()




