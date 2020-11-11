import sys
import os


class Parser:
    def __init__(self, inputFile):
        self.readFile = open(inputFile, "r")
        self.currentCommand = ""
        self.currentCommandList = []
        self.command_type = ""
        self.arg1 = ""
        self.arg2 = ""

    def advance(self):
         self.currentCommand = self.readFile.readline()
         self.currentCommandList = self.currentCommand.split()

    def hasMoreCommands(self):
        return (self.currentCommand != "")

    def get_current_command(self):
        return self.currentCommand

    def commandType(self):

        if self.currentCommand == "\n" or self.currentCommand == "":
            return
        elif self.currentCommandList[0] == "return":
            self.command_type = "C_RETURN"
        elif self.currentCommandList[0] == "call":
            self.command_type = "C_CALL"
            self.arg1 = self.currentCommandList[1]
            self.arg2 = self.currentCommandList[2]
        elif self.currentCommandList[0] == "function":
            self.command_type = "C_FUNCTION"
            self.arg1 = self.currentCommandList[1]
            self.arg2 = self.currentCommandList[2]
        elif self.currentCommandList[0] == "push":
            self.command_type = "C_PUSH"
            self.arg1 = self.currentCommandList[1]
            self.arg2 = self.currentCommandList[2]
        elif self.currentCommandList[0] == "pop":
            self.command_type = "C_POP"
            self.arg1 = self.currentCommandList[1]
            self.arg2 = self.currentCommandList[2]
        elif self.currentCommandList[0] == "label":
            self.command_type = "C_LABEL"
            self.arg1 = self.currentCommandList[1]
        elif self.currentCommandList[0] == "goto":
            self.command_type = "C_GOTO"
            self.arg1 = self.currentCommandList[1]
        elif self.currentCommandList[0] == "if-goto":
            self.command_type = "C_IF"
            self.arg1 = self.currentCommandList[1]
        else:
            self.command_type = "C_ARITHMETIC"
            self.arg1 = self.currentCommandList[0]

        return self.command_type

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2

class CodeWriter:
    def __init__(self, outputFile):
        self.write_file = open(outputFile, "w")
        self.prefix = outputFile[:-3]
        self.counter = 0
        self.c_string = "0"
        self.current_function = "$" + outputFile[:-4] + "$"
        self.loc_dict = {"local":"LCL", "argument":"ARG", "this":"THIS", "that":"THAT"}

    def write_arith(self, command):
        num = self.c_string
        if command == "add":
            self.write_file.write("//add\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "M=D+M\n" + "@SP\n" + "M=M-1\n")
        elif command == "sub":
            self.write_file.write("//sub\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "M=M-D\n" + "@SP\n" + "M=M-1\n")
        elif command == "neg":
            self.write_file.write("//neg\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=-M\n" + "M=D\n")
        elif command == "eq":
            self.write_file.write("//eq\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "D=M-D\n" + "@TRUE" + num + "\n" + \
                "D;JEQ\n" + \
                "@FALSE" + num + "\n" + "0;JMP\n" + \
                "(TRUE" + num + ")\n" + "@1\n" + "D=-A\n" + \
                "@SP\n" + "A=M\n" + "A=A-1\n" + "A=A-1\n" + "M=D\n" + \
                "@MOVEON" + num + "\n" + "0;JMP\n" + "(FALSE" + num + ")\n" + \
                "@0\n" + "D=A\n" + "@SP\n" + "A=M\n" + "A=A-1\n" + "A=A-1\n" + \
                "M=D\n" + "(MOVEON" + num + ")\n" + "@SP\n" + "M=M-1\n")
            self.counter += 1
            self.c_string = str(self.counter)
        elif command == "gt":
            self.write_file.write("//eq\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "D=M-D\n" + "@TRUE" + num + "\n" + \
                "D;JGT\n" + \
                "@FALSE" + num + "\n" + "0;JMP\n" + \
                "(TRUE" + num + ")\n" + "@1\n" + "D=-A\n" + \
                "@SP\n" + "A=M\n" + "A=A-1\n" + "A=A-1\n" + "M=D\n" + \
                "@MOVEON" + num + "\n" + "0;JMP\n" + "(FALSE" + num + ")\n" + \
                "@0\n" + "D=A\n" + "@SP\n" + "A=M\n" + "A=A-1\n" + "A=A-1\n" + \
                "M=D\n" + "(MOVEON" + num + ")\n" + "@SP\n" + "M=M-1\n")
            self.counter += 1
            self.c_string = str(self.counter)
        elif command == "lt":
            self.write_file.write("//eq\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "D=M-D\n" + "@TRUE" + num + "\n" + \
                "D;JLT\n" + \
                "@FALSE" + num + "\n" + "0;JMP\n" + \
                "(TRUE" + num + ")\n" + "@1\n" + "D=-A\n" + \
                "@SP\n" + "A=M\n" + "A=A-1\n" + "A=A-1\n" + "M=D\n" + \
                "@MOVEON" + num + "\n" + "0;JMP\n" + "(FALSE" + num + ")\n" + \
                "@0\n" + "D=A\n" + "@SP\n" + "A=M\n" + "A=A-1\n" + "A=A-1\n" + \
                "M=D\n" + "(MOVEON" + num + ")\n" + "@SP\n" + "M=M-1\n")
            self.counter += 1
            self.c_string = str(self.counter)
        elif command == "and":
            self.write_file.write("//and\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "M=D&M\n" + "@SP\n" + "M=M-1\n")
        elif command == "or":
            self.write_file.write("//or\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=M\n" + "A=A-1\n" + "M=D|M\n" + "@SP\n" + "M=M-1\n")
        elif command == "not":
            self.write_file.write("//not\n")
            self.write_file.write("@SP\n" + "A=M\n" + "A=A-1\n" + \
                "D=!M\n" + "M=D\n")



    def write_push_pop(self, command, seg, index):
        num = self.c_string
        self.write_file.write("//" + command  + " " + seg + " " + index + "\n")
        if seg == "constant":
            self.write_file.write("@" + index + "\n" + "D=A\n" + \
                "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")
        if seg in ("local", "argument", "this", "that"):
            if command == "C_PUSH":
                self.write_file.write("@" + self.loc_dict[seg] + "\n" + \
                    "D=M\n" + "@address\n" + "M=D\n" + "@" + index + "\n" + \
                    "D=A\n" + "@index\n" + "M=D\n" + \
                    "(LOOP" + num + ")\n" + "@index\n" + \
                    "D=M\n" + "@END" + num + "\n" + \
                    "D;JEQ\n" + "@address\n" + "M=M+1\n" + "@index\n" + \
                    "M=M-1\n" + "@LOOP" + num + "\n" + \
                    "0;JMP\n" + "(END" + num + ")\n" + \
                    "@address\n" + "A=M\n" + "D=M\n" + "@SP\n" + "A=M\n" + \
                    "M=D\n" + "@SP\n" + "M=M+1\n")
            if command == "C_POP":
                self.write_file.write("@" + self.loc_dict[seg] + "\n" + \
                    "D=M\n" + "@address\n" + "M=D\n" + "@" + index + "\n" + \
                    "D=A\n" + "@index\n" + "M=D\n" + \
                    "(LOOP" + num + ")\n" + "@index\n" + \
                    "D=M\n" + "@END" + num + "\n" + \
                    "D;JEQ\n" + "@address\n" + "M=M+1\n" + "@index\n" + \
                    "M=M-1\n" + "@LOOP" + num + "\n" + \
                    "0;JMP\n" + "(END" + num + ")\n" + \
                    "@SP\n" + "M=M-1\n" + "A=M\n" + "D=M\n" + "@address\n" + \
                    "A=M\n" + "M=D\n")
        if seg == "temp":
            if command == "C_PUSH":
                self.write_file.write("@5\n" + \
                    "D=A\n" + "@address\n" + "M=D\n" + "@" + index + "\n" + \
                    "D=A\n" + "@index\n" + "M=D\n" + \
                    "(LOOP" + num + ")\n" + "@index\n" + \
                    "D=M\n" + "@END" + num + "\n" + \
                    "D;JEQ\n" + "@address\n" + "M=M+1\n" + "@index\n" + \
                    "M=M-1\n" + "@LOOP" + num + "\n" + \
                    "0;JMP\n" + "(END" + num + ")\n" + \
                    "@address\n" + "A=M\n" + "D=M\n" + "@SP\n" + "A=M\n" + \
                    "M=D\n" + "@SP\n" + "M=M+1\n")
            if command == "C_POP":
                self.write_file.write("@5\n" + \
                    "D=A\n" + "@address\n" + "M=D\n" + "@" + index + "\n" + \
                    "D=A\n" + "@index\n" + "M=D\n" + \
                    "(LOOP" + num + ")\n" + "@index\n" + \
                    "D=M\n" + "@END" + num + "\n" + \
                    "D;JEQ\n" + "@address\n" + "M=M+1\n" + "@index\n" + \
                    "M=M-1\n" + "@LOOP" + num + "\n" + \
                    "0;JMP\n" + "(END" + num + ")\n" + \
                    "@SP\n" + "M=M-1\n" + "A=M\n" + "D=M\n" + "@address\n" + \
                    "A=M\n" + "M=D\n")
        if seg == "pointer":
            this_that = ""
            if index == "0":
                this_that = "THIS"
            else:
                this_that = "THAT"
            if command == "C_PUSH":
                self.write_file.write("@" + this_that + "\n" + \
                    "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + \
                    "M=M+1\n")
            elif command == "C_POP":
                self.write_file.write("@SP\n" + "M=M-1\n" + "A=M\n" + \
                    "D=M\n" + "@" + this_that + "\n" + "M=D\n")

        if seg == "static":
            if command == "C_PUSH":
                self.write_file.write("@" + self.prefix + index + "\n" + \
                    "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + \
                    "M=M+1\n")
            elif command == "C_POP":
                self.write_file.write("@SP\n" + "M=M-1\n" + "A=M\n" + \
                    "D=M\n" + "@" + self.prefix + index + "\n" + "M=D\n")


        self.counter += 1
        self.c_string = str(self.counter)

    def writeInit(self):
        return

    def writeLabel(self, label):
        self.write_file.write("// label " + label + "\n")
        self.write_file.write(f"({self.current_function}${label})\n")

    def writeGoto(self, label):
        self.write_file.write("// goto " + label + "\n")
        self.write_file.write(f"@{self.current_function}${label}\n" + "0;JMP\n")

    def writeIf(self, label):
        self.write_file.write("// if-goto " + label + "\n")
        self.write_file.write("@SP\n" + "M=M-1\n" + "A=M\n" + "D=M\n" + \
            f"@{self.current_function}${label}\n" + "D;JNE\n")

    def writeCall(self, func, numArgs):
        num = self.c_string
        retAdd = "return$" + num
        self.write_file.write("// call " + func + " " + numArgs + "\n")
        #push retAdd
        self.write_file.write(f"@{retAdd}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # push LCL
        self.write_file.write("@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # push ARG
        self.write_file.write("@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # push THIS
        self.write_file.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # push THAT
        self.write_file.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # ARG = SP-n-5
        self.write_file.write(f"@SP\nD=M\n@5\nD=D-A\n@{numArgs}\nD=D-A\n@ARG\nM=D\n")
        # LCL = SP
        self.write_file.write("@SP\nD=M\n@LCL\nM=D\n")
        # goto f
        self.write_file.write(f"@{func}\n0;JMP\n")
        #(returnAddress)
        self.write_file.write(f"({retAdd})\n")

        self.counter += 1
        self.c_string = str(self.counter)
    def writeReturn(self):
        self.write_file.write("// return\n")
        #FRAME = LCL
        self.write_file.write("@LCL\n" + "D=M\n" + "@frame\n" + "M=D\n")
        #RET = *(FRAME-5)
        self.write_file.write("@5\nD=A\n@frame\nA=M-D\nD=M\n@ret\nM=D\n")
        #*ARG = pop()
        self.write_file.write("@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n")
        #SP=ARG+1
        self.write_file.write("A=A+1\nD=A\n@SP\nM=D\n")
        #THAT=*(FRAME-1)
        self.write_file.write("@frame\nA=M\nA=A-1\nD=A\n@pos\nM=D\nA=M\nD=M\n@THAT\nM=D\n")
        #THIS = *(FRAME-2)
        self.write_file.write("@pos\nA=M\nA=A-1\nD=A\n@pos\nM=D\nA=M\nD=M\n@THIS\nM=D\n")
        #ARG = *(FRAME-3)
        self.write_file.write("@pos\nA=M\nA=A-1\nD=A\n@pos\nM=D\nA=M\nD=M\n@ARG\nM=D\n")
        #LCL = *(FRAME-4)
        self.write_file.write("@pos\nA=M\nA=A-1\nD=A\n@pos\nM=D\nA=M\nD=M\n@LCL\nM=D\n")
        #goto RET
        self.write_file.write("@ret\nA=M\n0;JMP\n")

    def writeFunction(self, func, numLocals):
        num = self.c_string
        self.current_function = func
        self.write_file.write("// function " + func + " " + numLocals + "\n")
        self.write_file.write(f"({func})\n" + f"@{numLocals}\n" + "D=A\n" + \
            "@counter\n" + "M=D\n" + f"(LOOP{num})\n" + "@counter\n" + \
            "D=M\n" + f"@END{num}\n" + "D;JEQ\n" + "@SP\n" + "A=M\n" + \
            "M=0\n" + "@SP\n" + "M=M+1\n" + "@counter\n" + "M=M-1\n" + \
            f"@LOOP{num}\n" + "0;JMP\n" + f"(END{num})\n")

        self.counter += 1
        self.c_string = str(self.counter)

    def writeBootstrap(self):
        self.write_file.write("// bootstrap\n")
        self.write_file.write("@256\nD=A\n@SP\nM=D\n")
        self.writeCall("Sys.init", "0")



    def close(self):
        self.write_file.close()

def main_handle(parser1, writer):
    while True:
        parser1.advance()
        current_command = parser1.get_current_command()
        command_type = parser1.commandType()
        arg1 = parser1.get_arg1()
        arg2 = parser1.get_arg2()

        if not parser1.hasMoreCommands():
            return

        elif current_command[:2] == "//" or current_command[:2] == "\n":
            continue

        elif command_type == "C_ARITHMETIC":
            writer.write_arith(arg1)

        elif command_type == "C_PUSH" or command_type == "C_POP":
            writer.write_push_pop(command_type, arg1, arg2)

        elif command_type == "C_LABEL":
            writer.writeLabel(arg1)

        elif command_type == "C_GOTO":
            writer.writeGoto(arg1)

        elif command_type == "C_IF":
            writer.writeIf(arg1)

        elif command_type == "C_FUNCTION":
            writer.writeFunction(arg1, arg2)

        elif command_type == "C_RETURN":
            writer.writeReturn()

        elif command_type == "C_CALL":
            writer.writeCall(arg1, arg2)


def main():
    
    if os.path.isfile(sys.argv[1]):
        writer = CodeWriter(sys.argv[1][:-2] + "asm")
        writer.writeBootstrap()
        parser1 = Parser(sys.argv[1])

        main_handle(parser1, writer)

    else:
        writer = CodeWriter(sys.argv[1][:-1] + ".asm")
        writer.writeBootstrap()
        with os.scandir(sys.argv[1]) as it:
            for entry in it:
                if entry.name.endswith('.vm'):
                    writer.prefix = entry.name[:-2]
                    parser1 = Parser(entry)
                    main_handle(parser1, writer)
    
    writer.close()
    
main()
