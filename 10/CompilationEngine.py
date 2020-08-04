#!/usr/bin/python3
# coding: utf-8

class CompilationEngine:
    def __init__(self, input_file, output_file):
        '''
        与えられた入力と出力に対して新しいコンパイルエンジンを生成する
        次に呼ぶルーチンは compileClass() でなければならない
        str, str -> void
        '''
        pass

    def compileClass(self):
        '''
        クラスをコンパイルする
        void -> void
        '''
        pass

    def compileClassVarDec(self):
        '''
        スタティック宣言またはフィールド宣言をコンパイルする
        void -> void
        '''
        pass

    def compileSubroutine(self):
        '''
        メソッド、ファンクション、コンストラクタをコンパイルする
        void -> void
        '''
        pass

    def compileParameterList(self):
        '''
        パラメータのリストをコンパイルする
        () は含まない
        void -> void
        '''
        pass

    def compileVarDec(self):
        '''
        var 宣言をコンパイルする
        void -> void
        '''
        pass

    def compileStatements(self):
        '''
        一連の文をコンパイルする
        {} は含まない
        void -> void
        '''
        pass

    def compileDo(self):
        '''
        do 文をコンパイルする
        void -> void
        '''
        pass

    def compileLet(self):
        '''
        let 文をコンパイルする
        void -> void
        '''
        pass

    def compileWhile(self):
        '''
        while 文をコンパイルする
        void -> void
        '''
        pass

    def compileReturn(self):
        '''
        return 文をコンパイルする
        void -> void
        '''
        pass

    def compileIf(self):
        '''
        if 文をコンパイルする
        else 文を伴う可能性がある
        void -> void
        '''
        pass

    def compileExpression(self):
        '''
        式をコンパイルする
        void -> void
        '''
        pass

    def compileTerm(self):
        '''
        term をコンパイルする
        場合によって先読みをする必要がある
        void -> void
        '''
        pass

    def compileExpressionList(self):
        '''
        コンマで分離された式のリストをコンパイルする
        void -> void
        '''
        pass
