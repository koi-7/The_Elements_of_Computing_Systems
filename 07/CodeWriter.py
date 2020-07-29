#!/usr/bin/python3
# coding: utf-8

jump_addr = 0

class CodeWriter:



    def __init__(self, filename):
        '''
        出力ファイル / ストリームを開き、書き込む準備を行う
        str -> void
        '''
        self.f = open(filename, 'wt')

        self.f.write('@256' + '\n')
        self.f.write('D=A' + '\n')
        self.f.write('@SP' + '\n')
        self.f.write('M=D' + '\n')

    def setFileName(self, fileName):
        '''
        CodeWriter モジュールに新しい VM ファイルの変換が開始したことを知らせる
        str -> void
        '''
        pass

    def writeArithmetic(self, command):
        '''
        与えられた算術コマンドをアセンブリコードに変換し、それを書き込む
        str -> void
        '''
        global jump_addr

        self.f.write('\n')

        if command == 'add':
            self.f.write('@SP'   + '     // add \n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=D+M' + '\n')

        elif command == 'sub':
            self.f.write('@SP'   + '     // sub \n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=M-D' + '\n')

        elif command == 'neg':
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('M=-D'  + '\n')
            self.f.write('@SP'   + '\n')
            self.f.write('M=M+1' + '\n')

        elif command == 'eq':
            eq_jump1 = 'jump' + str(jump_addr)
            eq_jump2 = 'jump' + str(jump_addr + 1)
            jump_addr += 2
            self.f.write('@SP' + '     // eq \n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('D=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('D=M-D' + '\n')
            self.f.write('@' + eq_jump1 + '\n')
            self.f.write('D;JEQ' + '\n')
            self.f.write('@SP' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=0' + '\n')
            self.f.write('@' + eq_jump2 + '\n')
            self.f.write('0;JMP' + '\n')
            self.f.write('(' + eq_jump1 + ')' + '\n')
            self.f.write('@SP' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=0' + '\n')
            self.f.write('M=-1' + '\n')
            self.f.write('(' + eq_jump2 + ')' + '\n')

        elif command == 'gt':
            eq_jump1 = 'jump' + str(jump_addr)
            eq_jump2 = 'jump' + str(jump_addr + 1)
            jump_addr += 2
            self.f.write('@SP' + '     // gt \n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('D=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('D=M-D' + '\n')
            self.f.write('@' + eq_jump1 + '\n')
            self.f.write('D;JGT' + '\n')
            self.f.write('@SP' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=0' + '\n')
            self.f.write('@' + eq_jump2 + '\n')
            self.f.write('0;JMP' + '\n')
            self.f.write('(' + eq_jump1 + ')' + '\n')
            self.f.write('@SP' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=0' + '\n')
            self.f.write('M=-1' + '\n')
            self.f.write('(' + eq_jump2 + ')' + '\n')

        elif command == 'lt':
            eq_jump1 = 'jump' + str(jump_addr)
            eq_jump2 = 'jump' + str(jump_addr + 1)
            jump_addr += 2
            self.f.write('@SP' + '     // lt \n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('D=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('D=M-D' + '\n')
            self.f.write('@' + eq_jump1 + '\n')
            self.f.write('D;JLT' + '\n')
            self.f.write('@SP' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=0' + '\n')
            self.f.write('@' + eq_jump2 + '\n')
            self.f.write('0;JMP' + '\n')
            self.f.write('(' + eq_jump1 + ')' + '\n')
            self.f.write('@SP' + '\n')
            self.f.write('A=M' + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=0' + '\n')
            self.f.write('M=-1' + '\n')
            self.f.write('(' + eq_jump2 + ')' + '\n')

        elif command == 'and':
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=D&M' + '\n')

        elif command == 'or':
            self.f.write('@SP'   + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M'   + '\n')
            self.f.write('D=M'   + '\n')
            self.f.write('A=A-1' + '\n')
            self.f.write('M=D|M' + '\n')

        elif command == 'not':
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
        int, str, int -> void
        '''

        segment_dict = {
            'argument': 'ARG',
            'local': 'LCL',
            'static': 16,
            'constant': '',
            'this': 'THIS',
            'that': 'THAT',
            'pointer': 3,
            'temp': 5,
        }

        self.f.write('\n')

        if command == 'push':
            if segment == 'argument' or segment == 'local' or segment == 'this' or segment == 'that':
                self.f.write('@' + str(index) + '     // push a or l or th \n')
                self.f.write('D=A' + '\n')
                self.f.write('@' + segment_dict[segment] + '\n')
                self.f.write('A=D+M' + '\n')
                self.f.write('D=M' + '\n')
                self.f.write('@SP' + '     // ここから push \n')
                self.f.write('M=M+1' + '\n')
                self.f.write('A=M-1' + '\n')
                self.f.write('M=D' + '\n')
            elif segment == 'static':
                self.f.write('@' + str(index) + '     // push static \n')
                self.f.write('D=A' + '\n')
                self.f.write('@' + segment_dict[segment] + '\n')
                self.f.write('A=D+M' + '\n')
                self.f.write('D=M' + '\n')
                self.f.write('@SP' + '     // ここから push \n')
                self.f.write('M=M+1' + '\n')
                self.f.write('A=M-1' + '\n')
                self.f.write('M=D' + '\n')
            elif segment == 'constant':
                self.f.write('@' + str(index) + '     // push constant\n')
                self.f.write('D=A'       + '\n')
                self.f.write('@SP'       + '\n')
                self.f.write('M=M+1'     + '\n')
                self.f.write('A=M-1'     + '\n')
                self.f.write('M=D'       + '\n')
            elif segment == 'pointer' or segment == 'temp':
                self.f.write('@' + str(segment_dict[segment] + index) + ' // push p or tmp\n')
                self.f.write('D=M' + '\n')
                self.f.write('@SP' + '     // ここから push \n')
                self.f.write('M=M+1' + '\n')
                self.f.write('A=M-1' + '\n')
                self.f.write('M=D' + '\n')

        elif command == 'pop':
            if segment == 'argument' or segment == 'local' or segment == 'this' or segment == 'that':
                self.f.write('// pop a or l or th \n')
                self.f.write('@SP' + '\n')
                self.f.write('M=M-1' + '\n')
                self.f.write('A=M' + '\n')
                self.f.write('D=M' + '\n')
                self.f.write('@' + segment_dict[segment] + '\n')
                for i in range(index):
                    self.f.write('A=A+1' + '\n')  ## 力業
                self.f.write('M=D' + '\n')

            elif segment == 'static':
                self.f.write('// pop static \n')
                self.f.write('@SP' + '\n')
                self.f.write('M=M-1' + '\n')
                self.f.write('A=M' + '\n')
                self.f.write('D=M' + '\n')
                self.f.write('@' + segment_dict[segment] + '\n')
                for i in range(index):
                    self.f.write('A=A+1' + '\n')  ## 力業
                self.f.write('M=D' + '\n')

            elif segment == 'pointer' or segment == 'temp':
                self.f.write('@' + str(segment_dict[segment] + index) + ' // pop p or tmp\n')
                self.f.write('' + '\n')
                self.f.write('' + '\n')
                self.f.write('' + '\n')
                self.f.write('' + '\n')
                self.f.write('' + '\n')


    def close(self):
        '''
        出力ファイルを閉じる
        void -> void
        '''
        self.f.close()
