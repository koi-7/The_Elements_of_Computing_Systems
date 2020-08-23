#!/usr/bin/python3
# coding: utf-8

import JackTokenizer as JT
import SymbolTable as ST
import VMWriter as VMW

classVarDec_count = 0
subroutine_name = ''
varDec_count = 0
label_number = 0
parameterList_count = 0
varDec_count = 0
expressionList_count = 0

class CompilationEngine:
    def __init__(self, input_file, output_file):
        """
        与えられた入力と出力に対して新しいコンパイルエンジンを生成する
        次に呼ぶルーチンは compileClass() でなければならない
        str, str -> void
        """
        self.j = JT.JackTokenizer(input_file)
        self.s = ST.SymbolTable()
        self.v = VMW.VMWriter(output_file)

        self.class_name = ''

    def compileClass(self):
        """
        クラスをコンパイルする
        void -> void
        """
        self.forward()             ## 'class'
        self.class_name = self.j.token
        self.forward()             ## className
        self.forward()             ## '{'
        self.compileClassVarDec()  ## classVarDec*
        self.compileSubroutine()   ## subroutineDec*
        self.forward()             ## '}'

    def compileClassVarDec(self):
        """
        スタティック宣言またはフィールド宣言をコンパイルする
        void -> void
        """
        global classVarDec_count

        # classVarDec 0個
        if not self.j.token in {'static', 'field'}:
            pass

        # classVarDec 1個以上
        else:
            while self.j.token in {'static', 'field'}:
                if self.j.token == 'static':
                    kind = ST.STATIC
                elif self.j.token == 'field':
                    classVarDec_count += 1
                    kind = ST.FIELD

                self.forward()     ## 'static' or 'field'
                type = self.j.token
                self.forward()     ## type
                name = self.j.token
                self.s.define(name, type, kind)
                self.forward()     ## varName
                while self.j.token == ',':
                    if kind == ST.FIELD:
                        classVarDec_count += 1
                    self.forward()  ## ','
                    name = self.j.token
                    self.s.define(name, type, kind)
                    self.forward()  ## varName
                self.forward()      ## ';'

    def compileSubroutine(self):
        """
        メソッド、ファンクション、コンストラクタをコンパイルする
        void -> void
        """
        global classVarDec_count
        global parameterList_count
        global varDec_count
        global expressionList_count

        # subroutineDec
        ## subroutineDec なし
        if self.j.token == '}':
            pass

        ## subroutineDec あり
        elif self.j.token in {'constructor', 'function', 'method'}:
            while self.j.token in {'constructor', 'function', 'method'}:
                subroutine_name = ''
                parameterList_count = 0
                varDec_count = 0
                dec = ''

                self.s.startSubroutine()
                dec = self.j.token
                if dec == 'method':
                    self.s.define('this', self.class_name, ST.ARG)

                self.forward()               ## 'constructor' | 'function' | 'method'
                self.forward()               ## 'void' | type
                subroutine_name = self.class_name + '.' + self.j.token
                self.forward()               ## subroutineName
                self.forward()               ## '('
                self.compileParameterList()  ## parameterList
                self.forward()               ## ')'

                # subroutineBody
                self.forward()               ## '{'
                self.compileVarDec()         ## varDec*
                self.v.writeFunction(subroutine_name, varDec_count)
                if dec == 'constructor':
                    self.v.writePush(VMW.CONST, classVarDec_count)
                    self.v.writeCall('Memory.alloc', 1)
                    self.v.writePop(VMW.POINTER, 0)
                elif dec == 'method':
                    self.v.writePush(VMW.ARG, 0)
                    self.v.writePop(VMW.POINTER, 0)
                self.compileStatements()     ## statements
                self.forward()               ## '}'

        # subroutineCall
        elif self.j.token_list[0] in {'(', '.'}:
            subroutine_name = ''
            expressionList_count = 0

            if self.j.token_list[0] == '(':
                expressionList_count += 1
                type = self.class_name
                subroutine_name = type + '.'
                index = 0
                self.v.writePush(VMW.POINTER, index)

            elif self.j.token_list[0] == '.':
                kind = self.s.kindOf(self.j.token)

                if kind == ST.NONE:
                    subroutine_name = self.j.token
                elif kind in {ST.VAR, ST.FIELD}:
                    expressionList_count += 1
                    type = self.s.typeOf(self.j.token)
                    subroutine_name = type
                    index = self.s.indexOf(self.j.token)
                    if kind == ST.VAR:
                        self.v.writePush(VMW.LOCAL, index)
                    elif kind == ST.FIELD:
                        self.v.writePush(VMW.THIS, index)

                self.forward()            ## className | varName
                subroutine_name += self.j.token
                self.forward()            ## '.'

            subroutine_name += self.j.token
            self.forward()                ## subroutineName
            self.forward()                ## '('
            self.compileExpressionList()  ## expressionList
            self.forward()                ## ')'
            self.v.writeCall(subroutine_name, expressionList_count)

    def compileParameterList(self):
        """
        パラメータのリストをコンパイルする
        () は含まない
        void -> void
        """
        global parameterList_count

        # 引数なし
        if self.j.token == ')':
            pass

        # 引数あり
        else:
            parameterList_count += 1
            type = self.j.token
            self.forward()      ## type
            name = self.j.token
            self.s.define(name, type, ST.ARG)
            self.forward()      ## varName
            while self.j.token == ',':
                parameterList_count += 1
                self.forward()  ## ','
                type = self.j.token
                self.forward()  ## type
                name = self.j.token
                self.s.define(name, type, ST.ARG)
                self.forward()  ## varName

    def compileVarDec(self):
        """
        var 宣言をコンパイルする
        void -> void
        """
        global varDec_count
        # varDec 0個
        if self.j.token != 'var':
            pass

        # varDec 1個以上
        else:
            while self.j.token == 'var':
                varDec_count += 1
                kind = ST.VAR
                self.forward()      ## 'var'
                type = self.j.token
                self.forward()      ## type
                self.s.define(self.j.token, type, ST.VAR)
                self.forward()      ## varName
                while self.j.token == ',':
                    varDec_count += 1
                    self.forward()  ## ','
                    self.s.define(self.j.token, type, ST.VAR)
                    self.forward()  ## varName
                self.forward()      ## ';'

    def compileStatements(self):
        """
        一連の文をコンパイルする
        {} は含まない
        void -> void
        """
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

    def compileDo(self):
        """
        do 文をコンパイルする
        void -> void
        """
        self.forward()            ## 'do'
        self.compileSubroutine()  ## subroutineCall
        self.v.writePop(VMW.TEMP, 0)
        self.forward()            ## ';'

    def compileLet(self):
        """
        let 文をコンパイルする
        void -> void
        """
        self.forward()                ## 'let'

        name = self.j.token
        kind = self.s.kindOf(name)
        index = self.s.indexOf(name)

        if kind == 'var':
            kind = VMW.LOCAL
        elif kind == 'field':
            kind = VMW.THIS
        elif kind == 'static':
            kind = VMW.STATIC
        else:
            kind = VMW.ARG

        self.forward()                ## varName

        if self.j.token == '[':
            self.forward()            ## '['
            self.compileExpression()  ## expression
            self.forward()            ## ']'
            self.v.writePush(kind, index)
            self.v.writeArithmetic(VMW.ADD)
            self.forward()            ## '='
            self.compileExpression()  ## expression
            self.v.writePop(VMW.TEMP, 0)
            self.v.writePop(VMW.POINTER, 1)
            self.v.writePush(VMW.TEMP, 0)
            self.v.writePop(VMW.THAT, 0)
            self.forward()            ## ';'

        else:
            self.forward()            ## '='
            self.compileExpression()  ## expression
            self.v.writePop(kind, index)
            self.forward()            ## ';'

    def compileWhile(self):
        """
        while 文をコンパイルする
        void -> void
        """
        global label_number

        label1 = 'WHILE_EXP' + str(label_number)
        label2 = 'WHILE_END' + str(label_number)
        label_number += 1

        self.v.writeLabel(label1)
        self.forward()            ## 'while'
        self.forward()            ## '('
        self.compileExpression()  ## expression
        self.forward()            ## ')'
        self.v.writeArithmetic(VMW.NOT)
        self.v.writeIf(label2)
        self.forward()            ## '{'
        self.compileStatements()  ## statements
        self.forward()            ## '}'
        self.v.writeGoto(label1)
        self.v.writeLabel(label2)

    def compileReturn(self):
        """
        return 文をコンパイルする
        void -> void
        """
        self.forward()                ## 'return'
        if self.j.token == ';':
            self.v.writePush(VMW.CONST, 0)
        else:
            self.compileExpression()  ## expression
        self.forward()                ## ';'
        self.v.writeReturn()

    def compileIf(self):
        """
        if 文をコンパイルする
        else 文を伴う可能性がある
        void -> void
        """
        global label_number

        label1 = 'IF_TRUE' + str(label_number)
        label2 = 'IF_FALSE' + str(label_number)
        label3 = 'IF_END' + str(label_number)
        label_number += 1

        self.forward()                ## 'if'
        self.forward()                ## '('
        self.compileExpression()      ## expression
        self.forward()                ## ')'

        self.v.writeIf(label1)
        self.v.writeGoto(label2)
        self.v.writeLabel(label1)

        self.forward()                ## '{'
        self.compileStatements()      ## statements
        self.forward()                ## '}'

        ## else 節あり
        if self.j.token == 'else':
            self.v.writeGoto(label3)
            self.v.writeLabel(label2)
            self.forward()            ## 'else'
            self.forward()            ## '{'
            self.compileStatements()  ## statements
            self.forward()            ## '}'
            self.v.writeLabel(label3)

        ## else 節なし
        else:
            self.v.writeLabel(label2)

    def compileExpression(self):
        """
        式をコンパイルする
        void -> void
        """
        op_dict = {
            '+': VMW.ADD, '-': VMW.SUB, '*': '', '/': '', '&': VMW.AND,
            '|': VMW.OR, '<': VMW.LT, '>': VMW.GT, '=': VMW.EQ,
        }
        op = ''

        self.compileTerm()      ## term
        while self.j.token in op_dict:
            op = self.j.token
            self.forward()      ## op
            self.compileTerm()  ## term
            if op == '*':
                self.v.writeCall('Math.multiply', 2)
            elif op == '/':
                self.v.writeCall('Math.divide', 2)
            else:
                self.v.writeArithmetic(op_dict[op])

    def compileTerm(self):
        """
        term をコンパイルする
        場合によって先読みをする必要がある
        void -> void
        """
        if self.j.token == '(':
            self.forward()            ## '('
            self.compileExpression()  ## expression
            self.forward()            ## ')'

        elif self.j.token == '-' or self.j.token == '~':
            op = self.j.token
            self.forward()            ## '-' | '~'
            self.compileTerm()        ## term
            if op == '-':
                self.v.writeArithmetic(VMW.NEG)
            elif op == '~':
                self.v.writeArithmetic(VMW.NOT)

        elif self.j.token_list[0] == '[':
            kind = self.s.kindOf(self.j.token)
            if kind == ST.VAR:
                kind = VMW.LOCAL
            index = self.s.indexOf(self.j.token)
            self.forward()            ## varName
            self.forward()            ## '['
            self.compileExpression()  ## expression
            self.forward()            ## ']'
            self.v.writePush(kind, index)
            self.v.writeArithmetic(VMW.ADD)
            self.v.writePop(VMW.POINTER, 1)
            self.v.writePush(VMW.THAT, 0)

        elif self.j.token_list[0] == '(' or self.j.token_list[0] == '.':
            self.compileSubroutine()  ## subroutineCall

        else:
            ## integerConstant
            if self.j.token.isdecimal():
                self.v.writePush(VMW.CONST, self.j.token)

            ## keywordConstant
            elif self.j.token in {'true', 'false', 'null', 'this'}:
                if self.j.token == 'true':
                    self.v.writePush(VMW.CONST, 0)
                    self.v.writeArithmetic(VMW.NOT)
                elif self.j.token == 'false':
                    self.v.writePush(VMW.CONST, 0)
                elif self.j.token == 'this':
                    self.v.writePush(VMW.POINTER, 0)
                elif self.j.token == 'null':
                    self.v.writePush(VMW.CONST, 0)

            ## varName
            elif self.j.token in self.s.tables[0] or self.j.token in self.s.tables[1]:
                kind = self.s.kindOf(self.j.token)
                index = self.s.indexOf(self.j.token)
                if kind == ST.STATIC:
                    self.v.writePush(VMW.STATIC, index)
                elif kind == ST.FIELD:
                    self.v.writePush(VMW.THIS, index)
                elif kind == ST.ARG:
                    self.v.writePush(VMW.ARG, index)
                elif kind == ST.VAR:
                    self.v.writePush(VMW.LOCAL, index)

            ## stringConstant
            else:
                str = self.j.stringVal()
                self.v.writePush(VMW.CONST, len(str))
                self.v.writeCall('String.new', 1)
                for s in str:
                    self.v.writePush(VMW.CONST, ord(s))
                    self.v.writeCall('String.appendChar', 2)

            self.forward()  ## integerConstant | stringConstant | keywordConstant | varName

    def compileExpressionList(self):
        """
        コンマで分離された式のリストをコンパイルする
        void -> void
        """
        global expressionList_count

        if self.j.token == ')':
            pass

        else:
            expressionList_count += 1
            self.compileExpression()      ## expression
            while self.j.token == ',':
                expressionList_count += 1
                self.forward()            ## ','
                self.compileExpression()  ## expression

    def forward(self):
        """
        次のトークンを読み込む
        void -> void
        """
        if self.j.hasMoreTokens():
            self.j.advance()
