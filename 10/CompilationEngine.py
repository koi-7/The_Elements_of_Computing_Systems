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

        # トークンリストの作成
        self.j.make_token_list()

    def compileClass(self):
        '''
        クラスをコンパイルする
        void -> void
        '''

        self.fout.write('<class>' + '\n')

        if self.j.hasMoreTokens():  ## class
            self.j.advance()
            self.write_xml()

        if self.j.hasMoreTokens():  ## クラス名
            self.j.advance()
            self.write_xml()

        if self.j.hasMoreTokens():  ## {
            self.j.advance()
            self.write_xml()

        if self.j.hasMoreTokens():
            self.j.advance()
            self.compileClassVarDec()  # classVarDec
            self.compileSubroutine()  # subroutineDec

        if self.j.hasMoreTokens():  ## {
            self.j.advance()
            self.write_xml()

        if not self.j.hasMoreTokens():
            self.fout.write('</class>' + '\n')

    def compileClassVarDec(self):  ## ok
        '''
        スタティック宣言またはフィールド宣言をコンパイルする
        void -> void
        '''
        if self.j.token != 'static' and self.j.token != 'field':
            return

        self.fout.write('<classVarDec>' + '\n')

        self.write_xml()  ## static or field
        self.j.advance()
        self.write_xml()  ## type
        self.j.advance()
        self.write_xml()  ## varName
        self.j.advance()
        while self.j.token == ',':
            self.write_xml()  ## ,
            self.j.advance()
            self.write_xml()  ## varName
            self.j.advance()
        self.write_xml()  ## ;

        self.fout.write('</classVarDec>' + '\n')

        if self.j.hasMoreTokens():
            self.j.advance()

    def compileSubroutine(self):  ## TODO
        '''
        メソッド、ファンクション、コンストラクタをコンパイルする
        void -> void
        '''

        if self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':  ## subroutineDec
            while self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
                self.fout.write('<subroutineDec>' + '\n')
                self.write_xml()  ## constructor or function or method
                self.j.advance()
                self.write_xml()  ## 'void' or type
                self.j.advance()
                self.write_xml()  ## subroutineName
                self.j.advance()
                self.write_xml()  ## '('
                self.j.advance()
                self.compileParameterList()
                self.write_xml()  ## ')'
                self.j.advance()
                self.fout.write('TODO: subtourineBody \n')
                self.fout.write('</subroutineDec>' + '\n')
                break
            return
        elif self.j.token == '{':  ## subroutineBody
            return

        else:  ## subroutineName
            return


    def compileParameterList(self):  ## ok
        '''
        パラメータのリストをコンパイルする
        () は含まない
        void -> void
        '''
        if self.j.token == ')':  ## 引数なし
            self.fout.write('<parameterList>' + '\n')
            self.fout.write('</parameterList>' + '\n')
            return
        else:                    ## 引数あり
            self.fout.write('<parameterList>' + '\n')
            self.write_xml()  ## type
            self.j.advance()
            self.write_xml()  ## varName
            self.j.advance()
            while self.j.token == ',':
                self.write_xml()  ## ','
                self.j.advance()
                self.write_xml()  ## type
                self.j.advance()
                self.write_xml()  ## varName
                self.j.advance()
            self.fout.write('</parameterList>' + '\n')

    def compileVarDec(self):  ## TODO
        '''
        var 宣言をコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileStatements(self):  ## TODO
        '''
        一連の文をコンパイルする
        {} は含まない
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileDo(self):  ## TODO
        '''
        do 文をコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileLet(self):  ## TODO
        '''
        let 文をコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileWhile(self):  ## TODO
        '''
        while 文をコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileReturn(self):  ## TODO
        '''
        return 文をコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileIf(self):  ## TODO
        '''
        if 文をコンパイルする
        else 文を伴う可能性がある
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileExpression(self):  ## TODO
        '''
        式をコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileTerm(self):  ## TODO
        '''
        term をコンパイルする
        場合によって先読みをする必要がある
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def compileExpressionList(self):  ## TODO
        '''
        コンマで分離された式のリストをコンパイルする
        void -> void
        '''
        if self.j.hasMoreTokens():
            self.j.advance()

    def write_xml(self):  ## ok
        '''
        トークンのタイプを見て xml に書き込みを行う
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




