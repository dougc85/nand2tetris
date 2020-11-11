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

(LOOP)

    @SCREEN    //Set location to the SCREEN memory location
    D=A
    @location
    M=D

    @SCREEN
    D=A
    @8192
    D=D+A
    @max       // Setting the max screen location
    M=D

    @KBD       //Read Keyboard
    D=M

    @CLEAR     //If no key pressed, jump to CLEAR
    D;JEQ

    (SET)
	@location
	A=M           //get address from location box
	M=-1          //set screen to black
	A=A+1         //increase address by 1
	D=A
	@location
	M=D           //store address back in location box
	@max
	D=D-M
	@SET
	D;JLT
	@LOOP
	0;JMP

    (CLEAR)
	@location
	A=M           //get address from location box
	M=0          //set screen to white
	A=A+1         //increase address by 1
	D=A
	@location
	M=D           //store address back in location box
	@max
	D=D-M
	@CLEAR
	D;JLT
	@LOOP
	0;JMP