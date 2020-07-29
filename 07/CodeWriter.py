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
        self.f.write('\n')

        if command == 'push':
            if segment == 'constant':
                self.f.write('@' + index + '     // push constant n \n')
                self.f.write('D=A'       + '\n')
                self.f.write('@SP'       + '\n')
                self.f.write('M=M+1'     + '\n')
                self.f.write('A=M-1'     + '\n')
                self.f.write('M=D'       + '\n')
            else:
                pass
        elif command == 'pop':
            pass

    def close(self):
        '''
        出力ファイルを閉じる
        void -> void
        '''
        self.f.close()
