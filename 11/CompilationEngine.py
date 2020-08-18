#!/usr/bin/python3
# coding: utf-8

import JackTokenizer as JT
import SymbolTable as ST
import VMWriter as VMW

label_number = 0
parameterList_count = 0
expressionList_count = 0

class CompilationEngine:
    def __init__(self, input_file, output_file):
        '''
        与えられた入力と出力に対して新しいコンパイルエンジンを生成する
        次に呼ぶルーチンは compileClass() でなければならない
        str, str -> void
        '''
        self.j = JT.JackTokenizer(input_file)
        self.s = ST.SymbolTable()
        self.v = VMW.VMWriter(output_file)

        self.class_name = ''

    def compileClass(self):
        '''
        クラスをコンパイルする
        void -> void
        '''
        # self.fout.write('<class>' + '\n')
        self.write_xml()           ## 'class'
        self.class_name = self.j.token
        self.write_xml()           ## className
        self.write_xml()           ## '{'
        self.compileClassVarDec()  ## classVarDec*
        self.compileSubroutine()   ## subroutineDec*
        self.write_xml()           ## '}'
        # self.fout.write('</class>' + '\n')

    def compileClassVarDec(self):
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
                # self.fout.write('<classVarDec>' + '\n')
                if self.j.token == 'static':
                    kind = ST.STATIC
                else:
                    kind = ST.FIELD
                self.write_xml()            ## 'static' or 'field'
                type = self.j.token
                self.write_xml()            ## type
                self.write_xml(type, kind)            ## varName
                while self.j.token == ',':
                    self.write_xml()        ## ','
                    self.write_xml(type, kind)        ## varName
                self.write_xml()            ## ';'
                # self.fout.write('</classVarDec>' + '\n')

    def compileSubroutine(self):
        '''
        メソッド、ファンクション、コンストラクタをコンパイルする
        void -> void
        '''
        # subroutineDec
        ## subroutineDec なし
        if self.j.token == '}':
            # self.fout.write('<subroutineDec>' + '\n')
            # self.fout.write('</subroutineDec>' + '\n')
            pass
        ## subroutineDec あり
        elif self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
            while self.j.token == 'constructor' or self.j.token == 'function' or self.j.token == 'method':
                global parameterList_count
                subroutine_name = self.class_name + '.'
                # self.fout.write('<subroutineDec>' + '\n')
                self.write_xml()             ## 'constructor' | 'function' | 'method'
                self.write_xml()             ## 'void' | type
                subroutine_name += self.j.token
                self.write_xml()             ## subroutineName
                self.write_xml()             ## '('
                self.compileParameterList()  ## parameterList
                self.write_xml()             ## ')'
                self.v.writeFunction(subroutine_name, parameterList_count)
                self.compileSubroutine()     ## subroutineBody
                # self.fout.write('</subroutineDec>' + '\n')

        # subroutineBody
        elif self.j.token == '{':
            # self.fout.write('<subroutineBody>' + '\n')
            self.write_xml()          ## '{'
            self.compileVarDec()      ## varDec*
            self.compileStatements()  ## statements
            self.write_xml()          ## '}'
            # self.fout.write('</subroutineBody>' + '\n')

        # subroutineCall
        elif self.j.token_list[0] == '(' or self.j.token_list[0] == '.':
            global expressionList_count
            subroutine_name = ''
            if self.j.token_list[0] == '.':
                subroutine_name = subroutine_name + self.j.token + '.'
                self.write_xml()          ## className | varName
                self.write_xml()          ## '.'
            subroutine_name = subroutine_name + self.j.token
            self.write_xml()              ## subroutineName
            self.write_xml()              ## '('
            self.compileExpressionList()  ## expressionList
            self.write_xml()              ## ')'

            self.v.writeCall(subroutine_name, expressionList_count)
            self.v.writePop(VMW.TEMP, 0)

    def compileParameterList(self):
        '''
        パラメータのリストをコンパイルする
        () は含まない
        void -> void
        '''
        # self.fout.write('<parameterList>' + '\n')

        # 引数なし
        if self.j.token == ')':
            pass

        # 引数あり
        else:
            expressionList_count += 1
            type = self.j.token
            self.write_xml()            ## type
            kind = ST.ARG
            self.write_xml(type, kind)            ## varName
            while self.j.token == ',':
                expressionList_count += 1
                self.write_xml()        ## ','
                self.write_xml()        ## type
                self.write_xml(type, kind)        ## varName

        # self.fout.write('</parameterList>' + '\n')

    def compileVarDec(self):
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
                # self.fout.write('<varDec>' + '\n')
                kind = ST.VAR
                self.write_xml()            ## 'var'
                type = self.j.token
                self.write_xml()            ## type
                self.write_xml(type, kind)            ## varName
                while self.j.token == ',':
                    self.write_xml()        ## ','
                    self.write_xml(type, kind)        ## varName
                self.write_xml()            ## ';'
                # self.fout.write('</varDec>' + '\n')

    def compileStatements(self):
        '''
        一連の文をコンパイルする
        {} は含まない
        void -> void
        '''
        # self.fout.write('<statements>' + '\n')

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

        # self.fout.write('</statements>' + '\n')

    def compileDo(self):
        '''
        do 文をコンパイルする
        void -> void
        '''
        # self.fout.write('<doStatement>' + '\n')
        self.write_xml()          ## 'do'
        self.compileSubroutine()  ## subroutineCall
        self.write_xml()          ## ';'
        # self.fout.write('</doStatement>' + '\n')

    def compileLet(self):
        '''
        let 文をコンパイルする
        void -> void
        '''
        # self.fout.write('<letStatement>' + '\n')
        self.write_xml()              ## 'let'
        self.write_xml()              ## varName
        if self.j.token == '[':
            self.write_xml()          ## '['
            self.compileExpression()  ## expression
            self.write_xml()          ## ']'
        self.write_xml()              ## '='
        self.compileExpression()      ## expression
        self.write_xml()              ## ';'
        # self.fout.write('</letStatement>' + '\n')

    def compileWhile(self):
        '''
        while 文をコンパイルする
        void -> void
        '''
        global label_number

        label1 = 'L' + str(label_number)
        label2 = 'L' + str(label_number + 1)
        label_number += 2

        self.v.writeLabel(label1)

        self.write_xml()          ## 'while'
        self.write_xml()          ## '('
        self.compileExpression()  ## expression
        self.write_xml()          ## ')'

        self.v.writeIf(label2)

        self.write_xml()          ## '{'
        self.compileStatements()  ## statements
        self.write_xml()          ## '}'

        self.v.writeGoto(label1)

        self.v.writeLabel(label2)

    def compileReturn(self):
        '''
        return 文をコンパイルする
        void -> void
        '''
        self.write_xml()              ## 'return'
        if self.j.token == ';':
            self.v.writePush(VMW.CONST, 0)
        else:
            self.compileExpression()  ## expression
        self.write_xml()              ## ';'

        self.v.writeReturn()

    def compileIf(self):
        '''
        if 文をコンパイルする
        else 文を伴う可能性がある
        void -> void
        '''
        global label_number

        label1 = 'L' + str(label_number)
        label2 = 'L' + str(label_number + 2)
        label_number += 2

        self.write_xml()              ## 'if'
        self.write_xml()              ## '('
        self.compileExpression()      ## expression
        self.write_xml()              ## ')'

        self.v.writeIf(label1)

        self.write_xml()              ## '{'
        self.compileStatements()      ## statements
        self.write_xml()              ## '}'

        self.v.writeGoto(label2)

        self.v.writeLabel(label1)

        if self.j.token == 'else':
            self.write_xml()          ## 'else'
            self.write_xml()          ## '{'
            self.compileStatements()  ## statements
            self.write_xml()          ## '}'

        self.v.writeLabel(label2)

    def compileExpression(self):
        '''
        式をコンパイルする
        void -> void
        '''
        op_dict = {
            '+': VMW.ADD, '-': VMW.SUB, '*': '', '/': '', '&': VMW.AND,
            '|': VMW.OR, '<': VMW.LT, '>': VMW.GT, '=': VMW.EQ,
        }
        op = ''

        # self.fout.write('<expression>' + '\n')
        self.compileTerm()             ## term
        while self.j.token in op_dict:
            op = self.j.token
            self.write_xml()           ## op
            self.compileTerm()         ## term
            if op == '*':
                self.v.writeCall('Math.multiply', 2)
            elif op == '/':
                self.v.writeCall('Math.divide', 2)
            else:
                self.v.writeArithmetic(op_dict[op])
        # self.fout.write('</expression>' + '\n')

    def compileTerm(self):
        '''
        term をコンパイルする
        場合によって先読みをする必要がある
        void -> void
        '''
        # self.fout.write('<term>' + '\n')

        if self.j.token == '(':
            self.write_xml()          ## '('
            self.compileExpression()  ## expression
            self.write_xml()          ## ')'

        elif self.j.token == '-' or self.j.token == '~':
            self.write_xml()    ## '-' | '~'
            self.compileTerm()  ## term

        elif self.j.token_list[0] == '[':
            self.write_xml()          ## varName
            self.write_xml()          ## '['
            self.compileExpression()  ## expression
            self.write_xml()          ## ']'

        elif self.j.token_list[0] == '(' or self.j.token_list[0] == '.':
            self.compileSubroutine()  ## subroutineCall

        else:
            if self.j.tokenType() == JT.INT_CONST:
                self.v.writePush(VMW.CONST, self.j.token)
            self.write_xml()  ## integerConstant | stringConstant | keywordConstant | varName

        # self.fout.write('</term>' + '\n')

    def compileExpressionList(self):
        '''
        コンマで分離された式のリストをコンパイルする
        void -> void
        '''
        global expressionList_count

        expressionList_count = 0
        # self.fout.write('<expressionList>' + '\n')

        if self.j.token == ')':
            pass

        else:
            self.compileExpression()      ## expression
            expressionList_count += 1
            while self.j.token == ',':
                expressionList_count += 1
                self.write_xml()          ## ','
                self.compileExpression()  ## expression

        # self.fout.write('</expressionList>' + '\n')

    def write_xml(self, *args):
        '''
        次のトークンを読み込む
        引数が存在する場合、シンボルテーブルへのデータ追加も行う
        void -> void
        str, str -> void
        '''
        if self.j.tokenType() == JT.IDENTIFIER:
            if len(args) > 0:
                self.s.define(self.j.identifier(), args[0], args[1])

        if self.j.hasMoreTokens():
            self.j.advance()
