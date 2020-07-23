// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// def mult(r0, r1):
//     mul = 0
//     while r1 != 0:
//         mul = mul + r0
//         r1 = r1 - 1
//     return mul

// R0 の値と R1 の値を掛け合わせたものを R2 格納する
    @mul
    M=0
(LOOP)
    @R1
    D=M
    @0
    D=D-A
    @END
    D;JEQ
    @mul
    D=M
    @R0
    D=D+M
    @1
    @R1
    M=M-A
    @LOOP
    0;JMP
(END)
    @mul
    D=M
    @R2
    M=D
    @END
    0;JMP
