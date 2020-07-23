// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@8192  // 8192(word) = 32(word/row) * 256(row)
D=A
@screen_word_size
M=D

(LOOP)
    @SCREEN
    D=A
    @fill_address
    M=D

    @KBD
    D=M
    @Key_pressed
    D;JGT

// キーボード非押下（color: 白に設定）
    @color
    M=0
    @Fill_screen
    0;JMP

// キーボード押下（color: 黒に設定）
(Key_pressed)
    @color
    M=-1

// 設定された色でスクリーンを塗る
(Fill_screen)
    // 色とアドレスを指定して着色
    @color
    D=M
    @fill_address
    A=M
    M=D

    // 次のアドレスへ
    @fill_address
    M=M+1

    // 色を塗り終えるまでループ
    D=M
    @SCREEN
    D=D-A
    @screen_word_size
    D=D-M
    @Fill_screen
    D;JLT

    @LOOP
    0;JEQ
