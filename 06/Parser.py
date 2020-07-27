#!/usr/bin/python3
# coding: utf-8

import re
import Code as cd


A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

symbol_pattern = r'[a-zA-z_.$0-9]+'
dest_pattern = r'(A?M?D?)'
comp_pattern = r'([AMD]?[\+\-\!&\|]?[01AMD]?)'
jump_pattern = r'(J?[EGLNM]?[TQEP]?)'

a_pattern = r'@([0-9]+)'
c_pattern = dest_pattern + r'=?' + comp_pattern + r';?' + jump_pattern
l_pattern = r'\(' + symbol_pattern + r'\)'


class Parser:
    def __init__(self, filename):
        '''
        入力ファイル / ストリームを開きパースを行う準備をする
        in:  str
        out: void
        '''
        self.command = ''
        self.f = open(filename, 'rt')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()


    def hasMoreCommands(self):
        '''
        入力にまだコマンドが存在するか？
        in:  void
        out: bool
        '''
        while True:
            line = self.f.readline()
            if line == '':
                return False
            elif re.match(r'^\n$|^/{2}', line):
                continue
            else:
                self.command = line
                return True

    def advance(self):
        '''
        入力から次のコマンドを読み、それを現在のコマンドにする
        in:  void
        out: void
        '''
        self.command = self.command.rstrip()

    def commandType(self):
        '''
        現コマンドの種類を返す
        in:  void
        out: A_COMMAND, C_COMMAND, L_COMMAND
        '''
        if re.match(a_pattern, self.command):
            return A_COMMAND
        elif re.match(c_pattern, self.command):
            return C_COMMAND
        elif re.match(l_pattern, self.command):
            return L_COMMAND

    def symbol(self):
        '''
        現コマンドのシンボルもしくは10進数の数値を返す
        in:  void
        out: str
        '''
        if self.commandType() == A_COMMAND:          ## 定数
            m = re.match(a_pattern, self.command)
            const = int(m.group(1))
            return format(const, '016b')
        elif self.commandType() == L_COMMAND:        ## シンボル
            pass

    def dest(self):
        '''
        現 C 命令の dest ニーモニックを返す
        in:  void
        out: str
        '''
        m = re.match(c_pattern, self.command)
        mnemonic = m.group(1)
        return cd.Code().dest(mnemonic)

    def comp(self):
        '''
        現 C 命令の comp ニーモニックを返す
        in:  void
        out: str
        '''
        m = re.match(c_pattern, self.command)
        mnemonic = m.group(2)
        return cd.Code().comp(mnemonic)

    def jump(self):
        '''
        現 C 命令の jump ニーモニックを返す
        in:  void
        out: str
        '''
        m = re.match(c_pattern, self.command)
        mnemonic = m.group(3)
        return cd.Code().jump(mnemonic)
