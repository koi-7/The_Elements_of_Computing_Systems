# mult.asm

まず知っている言語でアルゴリズムを書き起こす（例: Python）

```python
def mult(r0, r1):
    mul = 0
    while r1 != 0:
        mul = mul + r0
        r1 = r1 - 1
    return mul
```

これをより Hack 言語に近い適当な（脳内）言語に落とし込む

```
    Memory[mul]=0
(LOOP)
    D=Memory[R1]
    A=0
    D=D-A
    A=END
    D;JEQ
    Memory[mul]=Memory[mul]+Memory[R0]
    Memory[R1]=Memory[R1]-1
    A=LOOP
    0;JMP
(END)
    Memory[R2]=Memory[mul]
    A=END
    0;JMP
```

最後に Hack 言語に書き換える

```
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
```
