#!/usr/bin/python3
# coding: utf-8

class CodeWriter:
    def __init__(self, filename):
        '''
        出力ファイル / ストリームを開き、書き込む準備を行う
        str -> void
        '''
        self.f = open(filename, 'wt')

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
        pass

    def writePushPop(self, command, segment, index):
        '''
        C_PUSH または C_POP コマンドをアセンブリコードに変換し、それを書き込む
        int, str, int -> void
        '''
        pass

    def close(self):
        '''
        出力ファイルを閉じる
        void -> void
        '''
        self.f.close()
