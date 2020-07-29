#!/usr/bin/python3
# coding: utf-8

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
        if command == 'add':
            self.f.write('@SP' + '\n')
            self.f.write('M=M-1' + '\n')
            self.f.write('A=M-1' + '\n')
            self.f.write('D=M' + '\n')
            self.f.write('A=A+1' + '\n')
            self.f.write('M=D+M' + '\n')
        else:
            pass

    def writePushPop(self, command, segment, index):
        '''
        C_PUSH または C_POP コマンドをアセンブリコードに変換し、それを書き込む
        int, str, int -> void
        '''
        if command == 'push':
            if segment == 'constant':
                self.f.write('@' + index + '\n')
                self.f.write('D=A' + '\n')
                self.f.write('@SP' + '\n')
                self.f.write('M=M+1' + '\n')
                self.f.write('A=M-1' + '\n')
                self.f.write('M=D' + '\n')
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
