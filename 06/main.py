#!/usr/bin/python3
# coding: utf-8

import Parser as ps

def main():
    with ps.Parser('./add/Add.asm') as p:
        p.advance()
        while p.hasMoreCommands():
            print(p.command, end='')
            p.advance()


if __name__=='__main__':
    main()
