#!/usr/bin/python3
# coding: utf-8

import Parser as ps

jump_addr = 0           ## writeArithmetic で使用
label_number = 0        ## writeIf で使用
return_addr_number = 0  ## writeCall で使用

segment_dict = {
    'local':    1,  ## LCL
    'argument': 2,  ## ARG,
    'this':     3,  ## THIS
    'that':     4,  ## THAT
    'pointer':  3,  ## THIS
    'temp':     5,  ## R5
    'static':   16,
    'constant': '',
}

class CodeWriter:
    def __init__(self, output_file):
        '''
        出力ファイル / ストリームを開き、書き込む準備を行う
        str -> void
        '''
        self.input_file = ''
        self.f = open(output_file, 'wt')

    def setFileName(self, fileName):
        '''
        CodeWriter モジュールに新しい VM ファイルの変換が開始したことを知らせる
        str -> void
        '''
        self.input_file = fileName

    def writeInit(self):
        '''
        VM の初期化を行うアセンブリコードを書く
        void -> void
        '''
        ## SP=256
        self.f.write('@256' + '\n')
        self.f.write('D=A'  + '\n')
        self.f.write('@SP'  + '\n')
        self.f.write('M=D'  + '\n')

        ## call Sys.init
        self.writeCall('Sys.init', 0)

    def writeArithmetic(self, command):
        '''
        与えられた算術コマンドをアセンブリコードに変換し、それを書き込む
        str -> void
        '''
        global jump_addr

        if command == 'add':
            self.f.write('// add \n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=D+M' + '\n')

        elif command == 'sub':
            self.f.write('// sub \n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=M-D' + '\n')

        elif command == 'neg':
            self.f.write('// neg \n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('M=-D'  + '\n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M+1' + '\n')

        elif command == 'eq':
            jump1 = 'jump' + str(jump_addr)
            jump2 = 'jump' + str(jump_addr + 1)
            jump_addr += 2
            self.f.write('// eq \n')
            self.f.write('@SP'                + '\n')
            self.f.write('M=M-1'              + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('D=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('D=M-D'              + '\n')
            self.f.write('@' + jump1       + '\n')
            self.f.write('D;JEQ'              + '\n')
            self.f.write('@SP'                + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('M=0'                + '\n')
            self.f.write('@' + jump2       + '\n')
            self.f.write('0;JMP'              + '\n')
            self.f.write('(' + jump1 + ')' + '\n')
            self.f.write('@SP'                + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('M=0'                + '\n')
            self.f.write('M=-1'               + '\n')
            self.f.write('(' + jump2 + ')' + '\n')

        elif command == 'gt':
            jump1 = 'jump' + str(jump_addr)
            jump2 = 'jump' + str(jump_addr + 1)
            jump_addr += 2
            self.f.write('// gt \n')
            self.f.write('@SP'                + '\n')
            self.f.write('M=M-1'              + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('D=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('D=M-D'              + '\n')
            self.f.write('@' + jump1       + '\n')
            self.f.write('D;JGT'              + '\n')
            self.f.write('@SP'                + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('M=0'                + '\n')
            self.f.write('@' + jump2       + '\n')
            self.f.write('0;JMP'              + '\n')
            self.f.write('(' + jump1 + ')' + '\n')
            self.f.write('@SP'                + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('M=0'                + '\n')
            self.f.write('M=-1'               + '\n')
            self.f.write('(' + jump2 + ')' + '\n')

        elif command == 'lt':
            jump1 = 'jump' + str(jump_addr)
            jump2 = 'jump' + str(jump_addr + 1)
            jump_addr += 2
            self.f.write('// lt \n')
            self.f.write('@SP'                + '\n')
            self.f.write('M=M-1'              + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('D=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('D=M-D'              + '\n')
            self.f.write('@' + jump1       + '\n')
            self.f.write('D;JLT'              + '\n')
            self.f.write('@SP'                + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('M=0'                + '\n')
            self.f.write('@' + jump2       + '\n')
            self.f.write('0;JMP'              + '\n')
            self.f.write('(' + jump1 + ')' + '\n')
            self.f.write('@SP'                + '\n')
            self.f.write('A=M'                + '\n')
            self.f.write('A=A-1'              + '\n')
            self.f.write('M=0'                + '\n')
            self.f.write('M=-1'               + '\n')
            self.f.write('(' + jump2 + ')' + '\n')

        elif command == 'and':
            self.f.write('// and \n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=D&M' + '\n')

        elif command == 'or':
            self.f.write('// or \n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=D|M' + '\n')

        elif command == 'not':
            self.f.write('// not \n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('M=!D'  + '\n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M+1' + '\n')

    def writePushPop(self, command, segment, index):
        '''
        C_PUSH または C_POP コマンドをアセンブリコードに変換し、それを書き込む
        str, str, int -> void
        '''

        global segment_dict

        if command == ps.C_PUSH:
            if segment == 'argument' or segment == 'local' or segment == 'this' or segment == 'that':
                self.f.write('// push argument, local, this, that \n')
                self.f.write('@' + str(index)                 + '\n')
                self.f.write('D=A'                            + '\n')
                self.f.write('@' + str(segment_dict[segment]) + '\n')
                self.f.write('A=D+M'                          + '\n')
                self.f.write('D=M'                            + '\n')
                self.f.write('@SP'                            + '\n')
                self.f.write('M=M+1'                          + '\n')
                self.f.write('A=M-1'                          + '\n')
                self.f.write('M=D'                            + '\n')
            elif segment == 'pointer' or segment == 'temp':
                self.f.write('// push pointer, temp \n')
                self.f.write('@' + str(segment_dict[segment] + index) + '\n')
                self.f.write('D=M'                                    + '\n')
                self.f.write('@SP'                                    + '\n')
                self.f.write('M=M+1'                                  + '\n')
                self.f.write('A=M-1'                                  + '\n')
                self.f.write('M=D'                                    + '\n')
            elif segment == 'constant':
                self.f.write('// push constant \n')
                self.f.write('@' + str(index) + '\n')
                self.f.write('D=A'            + '\n')
                self.f.write('@SP'            + '\n')
                self.f.write('M=M+1'          + '\n')
                self.f.write('A=M-1'          + '\n')
                self.f.write('M=D'            + '\n')
            elif segment == 'static':
                self.f.write('// push static \n')
                self.f.write('@' + str(index)                 + '\n')
                self.f.write('D=A'                            + '\n')
                self.f.write('@' + str(segment_dict[segment]) + '\n')
                self.f.write('A=D+M'                          + '\n')
                self.f.write('D=M'                            + '\n')
                self.f.write('@SP'                            + '\n')
                self.f.write('M=M+1'                          + '\n')
                self.f.write('A=M-1'                          + '\n')
                self.f.write('M=D'                            + '\n')

        elif command == ps.C_POP:
            if segment == 'argument' or segment == 'local' or segment == 'this' or segment == 'that':
                self.f.write('// pop argument, local, this, that \n')
                self.f.write('@' + str(index)                 + '\n')
                self.f.write('D=A'                            + '\n')
                self.f.write('@' + str(segment_dict[segment]) + '\n')
                self.f.write('D=D+M'                          + '\n')
                self.f.write('@SP'                            + '\n')
                self.f.write('A=M'                            + '\n')
                self.f.write('M=D'                            + '\n')
                self.f.write('A=A-1'                          + '\n')
                self.f.write('D=M'                            + '\n')
                self.f.write('A=A+1'                          + '\n')
                self.f.write('A=M'                            + '\n')
                self.f.write('M=D'                            + '\n')
                self.f.write('@SP'                            + '\n')
                self.f.write('M=M-1'                          + '\n')
            elif segment == 'pointer' or segment == 'temp':
                self.f.write('// pop pointer or temp\n')
                self.f.write('@' + str(segment_dict[segment] + index) + '\n')
                self.f.write('D=A'                                    + '\n')
                self.f.write('@SP'                                    + '\n')
                self.f.write('A=M'                                    + '\n')
                self.f.write('M=D'                                    + '\n')
                self.f.write('A=A-1'                                  + '\n')
                self.f.write('D=M'                                    + '\n')
                self.f.write('A=A+1'                                  + '\n')
                self.f.write('A=M'                                    + '\n')
                self.f.write('M=D'                                    + '\n')
                self.f.write('@SP'                                    + '\n')
                self.f.write('M=M-1'                                  + '\n')
            elif segment == 'static':
                ## （今は）シンボル、複数ファイルがないので以下の通り
                self.f.write('// pop static\n')
                self.f.write('@' + str(index)                 + '\n')
                self.f.write('D=A'                            + '\n')
                self.f.write('@' + str(segment_dict[segment]) + '\n')
                self.f.write('D=D+M'                          + '\n')
                self.f.write('@SP'                            + '\n')
                self.f.write('A=M'                            + '\n')
                self.f.write('M=D'                            + '\n')
                self.f.write('A=A-1'                          + '\n')
                self.f.write('D=M'                            + '\n')
                self.f.write('A=A+1'                          + '\n')
                self.f.write('A=M'                            + '\n')
                self.f.write('M=D'                            + '\n')
                self.f.write('@SP'                            + '\n')
                self.f.write('M=M-1'                          + '\n')

    def writeLabel(self, label):
        '''
        label コマンドを行うアセンブリコードを書く
        str -> void
        '''

        self.f.write('// label \n')
        self.f.write('(' + label + ')' + '\n')

    def writeGoto(self, label):
        '''
        goto コマンドを行うアセンブリコードを書く
        str -> void
        '''
        self.f.write('// goto \n')
        self.f.write('@' + label + '\n')
        self.f.write('0;JMP' + '\n')

    def writeIf(self, label):
        '''
        if-goto コマンドを行うアセンブリコードを書く
        str -> void
        '''
        global label_number

        new_label = 'Label' + str(label_number)
        label_number += 1

        self.f.write('// if-goto \n')
        self.f.write('@SP' + '\n')
        self.f.write('M=M-1' + '\n')
        self.f.write('A=M' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@' + new_label + '\n')
        self.f.write('D;JEQ' + '\n')
        self.f.write('@' + label + '\n')
        self.f.write('0;JMP' + '\n')
        self.f.write('(' + new_label + ')' + '\n')

    def writeCall(self, functionName, numArgs):
        '''
        call コマンドを行うアセンブリコードを書く
        str, int -> void
        '''
        global return_addr_number

        return_addr_label = 'return_address' + str(return_addr_number)
        return_addr_number += 1

        self.f.write('// call \n')
        ## push return-address
        self.f.write('@' + return_addr_label + '\n')
        ## push LCL

        ## push ARG

        ## push THIS

        ## push THAT

        ## ARG = SP-n-5
        self.f.write('' + '\n')
        ## LCL = SP
        self.f.write('' + '\n')
        ## goto f
        self.f.write('@' + functionName + '\n')
        self.f.write('A=M' + '\n')
        self.f.write('0;JMP' + '\n')
        ## (return-address)
        self.writeLabel(return_addr_label)

    def writeReturn(self):
        '''
        return コマンドを行うアセンブリコードを書く
        void -> void
        '''
        self.f.write('// return \n')
        ## FRAME = LCL
        self.f.write('@LCL' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@FRAME' + '\n')
        self.f.write('M=D' + '\n')
        ## RET = *(FRAME - 5)
        self.f.write('@5' + '\n')
        self.f.write('D=A' + '\n')
        self.f.write('@FRAME' + '\n')
        self.f.write('A=M-D' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@RET' + '\n')
        self.f.write('M=D' + '\n')
        ## *ARG = pop()
        self.writePushPop(ps.C_POP, 'argument', 0)
        self.f.write('///// pop ここまで ここから return の続き /////' + '\n')
        ## SP = ARG + 1
        self.f.write('@ARG' + '\n')
        self.f.write('D=M+1' + '\n')
        self.f.write('@SP' + '\n')
        self.f.write('M=D' + '\n')
        ## THAT = *(FRAME-1)
        self.f.write('@1' + '\n')
        self.f.write('D=A' + '\n')
        self.f.write('@FRAME' + '\n')
        self.f.write('A=M-D' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@THAT' + '\n')
        self.f.write('M=D' + '\n')
        ## THIS = *(FRAME-2)
        self.f.write('@2' + '\n')
        self.f.write('D=A' + '\n')
        self.f.write('@FRAME' + '\n')
        self.f.write('A=M-D' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@THIS' + '\n')
        self.f.write('M=D' + '\n')
        ## ARG = *(FRAME-3)
        self.f.write('@3' + '\n')
        self.f.write('D=A' + '\n')
        self.f.write('@FRAME' + '\n')
        self.f.write('A=M-D' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@ARG' + '\n')
        self.f.write('M=D' + '\n')
        ## LCL = *(FRAME-4)
        self.f.write('@4' + '\n')
        self.f.write('D=A' + '\n')
        self.f.write('@FRAME' + '\n')
        self.f.write('A=M-D' + '\n')
        self.f.write('D=M' + '\n')
        self.f.write('@LCL' + '\n')
        self.f.write('M=D' + '\n')
        ## goto RET
        self.f.write('@RET' + '\n')
        self.f.write('A=M' + '\n')
        self.f.write('0;JMP' + '\n')

    def writeFunction(self, functionName, numLocals):
        '''
        function コマンドを行うアセンブリコードを書く
        str, int -> void
        '''
        self.f.write('// function \n')
        self.f.write('(' + functionName + ')' + '\n')
        for i in range(numLocals):
            self.writePushPop(ps.C_PUSH, 'constant', 0)

    def close(self):
        '''
        出力ファイルを閉じる
        void -> void
        '''
        self.f.close()
