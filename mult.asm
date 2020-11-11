// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R0     //a=R0
D=M
@a
M=D

@R1     //b=R1
D=M
@b
M=D

D=0
@product
M=D     //product=0

(LOOP)

@a
D=M
@END
D;JEQ      // if a=0, jump to the end

@b
D=M
@product   // product = product + b
M=D+M

@a
M=M-1      // a=a-1

@LOOP
0;JMP

(END)
@product
D=M
@R2
M=D         //R2 = product

(INF)
@INF
0;JMP



