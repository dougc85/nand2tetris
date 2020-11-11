import sys
import os

def main():
    f = sys.argv[1]
    
    if os.path.isfile(f):
        tzer = Tokenizer(f)
        write_file = open(f[:-4] + "xml", "w")
        comp = Compiler(tzer, write_file)
        comp.compile_Class()
        tzer.close()
        write_file.close()

    else:
        with os.scandir(f) as it:
            for entry in it:
                if entry.name.endswith('.jack'):
                    tzer = Tokenizer(entry)
                    write_file = open(entry.name[:-4] + "xml", "w")
                    comp = Compiler(tzer, write_file)
                    comp.compile_Class()
                    tzer.close()
                    write_file.close()


class Tokenizer:
    def __init__(self, inputfile):
        self.read_file = open(inputfile, "r")
        self.current = ""
        self.type = ""
        self.extra = False
        self.next = ""

    def keywordhelper(self, c):
        self.type = "keyword"
        self.next = c[:]
        
    def hasMoreTokens(self):
        if self.extra:
            c = self.next
            self.extra = False
        else:
            c = self.read_file.read(1)
        # End of file
        if not c:
            return False

        # Removing WhiteSpace
        if c in [" ", "\n", "\t", "\r"]:
            return self.hasMoreTokens()

        # Removing Comments (#$#!#!#@!)
        if c == "/":
            c = self.read_file.read(1)
            if c == "/":
                while c != "\n":
                    c = self.read_file.read(1)
                return self.hasMoreTokens()
            elif c == "*":
                c = self.read_file.read(1)
                if c == "*":
                    c = self.read_file.read(1)
                    end = c[:]
                    c = self.read_file.read(1)
                    end = end + c
                    while end != "*/":
                        c = self.read_file.read(1)
                        end = end[1:] + c
                    return self.hasMoreTokens()
                else:
                    end = c[:]
                    c = self.read_file.read(1)
                    end = end + c
                    while end != "*/":
                        c = self.read_file.read(1)
                        end = end[1:] + c
                    return self.hasMoreTokens()
            # Handling "/" Symbol
            else:
                self.current = "/"
                self.type = "symbol"
                self.extra = True
                self.next = c[:]
                return True
        # Handling Symbols
        if c in ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "&", "|", "<", ">", "=", "~"]:
            self.current = c[:]
            self.type = "symbol"
            return True
        
        # Handle String Constants
        if c == '"':
            c = self.read_file.read(1)
            self.current = ""
            self.type = 'stringConstant'
            while c != '"':
                self.current = self.current + c
                c = self.read_file.read(1)
            return True

        # Handle Integer Constants
        if c.isdigit():
            self.current = ""
            self.type = 'integerConstant'
            while c.isdigit():
                self.current = self.current + c
                c = self.read_file.read(1)
            self.extra = True
            self.next = c[:] 
            return True

        # Handle Identifiers and Keywords
        self.current = ""
        self.extra = True
        counter = 1
        while c.isdigit() or c.isalpha() or c == "_":
            self.current = self.current + c
            c = self.read_file.read(1)

            if counter == 2:
                if self.current == "if" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "do" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 3:
                if self.current == "var" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "int" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "let" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 4:
                if self.current == "char" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "void" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "true" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "else" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "null" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "this" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 5:
                if self.current == "class" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "field" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "false" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "while" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 6:
                if self.current == "method" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "static" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
                if self.current == "return" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 7:
                if self.current == "boolean" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 8:
                if self.current == "function" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            elif counter == 11:
                if self.current == "constructor" and not (c.isdigit() or c.isalpha() or c == "_"):
                    self.keywordhelper(c)
                    return True
            counter += 1

        self.type = "identifier"
        self.next = c[:]
        return True

    def get_Token(self):
        return self.current
    
    def get_Type(self):
        return self.type

    def close(self):
        self.read_file.close()

class Compiler:
    def __init__(self, tokenizer, outputfile):
        self.out = outputfile
        self.input = tokenizer
        self.spaces = ""

    def write_line(self):
        self.out.write(f"{self.spaces}<{self.input.get_Type()}> {self.input.get_Token()} </{self.input.get_Type()}>\n")
    
    def compile_Class(self):
        if self.input.hasMoreTokens():
            self.out.write("<class>\n")
            self.spaces = self.spaces + "  "
            # Keyword: Class
            self.write_line()
            # Name of class
            if self.input.hasMoreTokens():
                self.write_line()
            #  Left curly '{'
            if self.input.hasMoreTokens():
                self.write_line()
            # Compile everything within the {} for class
            while self.input.hasMoreTokens():
                if self.input.get_Token() in ['field', 'static']:
                    self.compile_Class_Var_Dec()
                elif self.input.get_Token() in ['constructor', 'function', 'method']:
                    self.compile_Subroutine()
                elif self.input.get_Token() == '}':
                    self.out.write(f"  <{self.input.get_Type()}> {self.input.get_Token()} </{self.input.get_Type()}>\n")
            
            self.spaces = self.spaces[:2]
            self.out.write("</class>")


    def compile_Class_Var_Dec(self):
        self.out.write(f"{self.spaces}<classVarDec>\n")
        self.spaces = self.spaces + "  "

        #Writes the type of variable (already loaded in the previous function call)
        self.write_line()

        #Write Class_Var_Declarations
        while self.input.get_Token() != ';':
            self.input.hasMoreTokens()
            self.write_line()

        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</classVarDec>\n")
    
    def compile_Subroutine(self):
        self.out.write(f"{self.spaces}<subroutineDec>\n")
        self.spaces = self.spaces + "  "

        #Writes the type of subroutine (already loaded in the previous function call)
        self.write_line()

        #Write and Compile Subroutine Stuff
        while self.input.get_Token() != '(':
            self.input.hasMoreTokens()
            self.write_line()
            

        self.compile_Parameter_List()
        
        #Write Subroutine Body
        self.out.write(f"{self.spaces}<subroutineBody>\n")
        self.spaces = self.spaces + "  "

        #Write '{'
        self.input.hasMoreTokens()
        self.write_line()

        #Write VarDec
        self.input.hasMoreTokens()
        while self.input.get_Token() == 'var':
            self.compile_Var_Dec()

        self.compile_Statements()

        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</subroutineBody>\n")

        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</subroutineDec>\n")

    def compile_Parameter_List(self):
        self.out.write(f"{self.spaces}<parameterList>\n")
        self.spaces = self.spaces + "  "

        
        self.input.hasMoreTokens()

        #Write Parameter List, if it exists
        while self.input.get_Token() != ")":
            self.write_line()
            self.input.hasMoreTokens()

        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</parameterList>\n")
        # Write ')'
        self.write_line()


    def compile_Var_Dec(self):
        self.out.write(f"{self.spaces}<varDec>\n")
        self.spaces = self.spaces + "  "

        #Writes the type of variable (already loaded in the previous function call)
        self.write_line()

        #Write var_Declarations
        while self.input.get_Token() != ';':
            self.input.hasMoreTokens()
            self.write_line()

        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</varDec>\n")

        # Get tokenizer loaded, since it was loaded when we entered var_dec
        self.input.hasMoreTokens()

    def compile_Statements(self):

        #!!! TOKENIZER HAS TO ALREADY BE LOADED, COMING INTO STATEMENTS

        self.out.write(f"{self.spaces}<statements>\n")
        self.spaces = self.spaces + "  "
        
        #Write Statements, if they exist

        
        while self.input.get_Token() != "}":
            if self.input.get_Token() == 'if':
                self.compile_If()
            elif self.input.get_Token() == 'let':
                self.compile_Let()
            elif self.input.get_Token() == 'do':
                self.compile_Do()
            elif self.input.get_Token() == 'while':
                self.compile_While()
            elif self.input.get_Token() == 'return':
                self.compile_Return()
            # !!!!!!!!!!!!  self.input.hasMoreTokens()
            
            

        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</statements>\n")

        #Write '}'
        self.write_line()


    def compile_Do(self):
        #Starts loaded with 'do' as the token
        self.out.write(f"{self.spaces}<doStatement>\n")
        self.spaces = self.spaces + "  "

        #Write 'do'
        self.write_line()

        while self.input.get_Token() != '(':
            self.input.hasMoreTokens()
            self.write_line()

        # At this point, tokenizer is UNLOADED
        self.compile_Expression_List()

        # Write ';'
        self.input.hasMoreTokens()
        self.write_line()


        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</doStatement>\n")

        #Preload for next round through Statements
        self.input.hasMoreTokens()

    def compile_Let(self):
        self.out.write(f"{self.spaces}<letStatement>\n")
        self.spaces = self.spaces + "  "

        #Write 'let'
        self.write_line()
        
        #Write varName
        self.input.hasMoreTokens()
        self.write_line()

        self.input.hasMoreTokens()

        if self.input.get_Token() == '[':

            #Write '['
            self.write_line()

            self.input.hasMoreTokens()
            self.compile_Expression()

            #Write ']'
            self.write_line()

            self.input.hasMoreTokens()

        # Write '='
        self.write_line()

        self.input.hasMoreTokens()
        self.compile_Expression()

        # Write ';'
        self.write_line()


        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</letStatement>\n")

        #Preload for next round through Statements
        self.input.hasMoreTokens()
    
    def compile_While(self):
        self.out.write(f"{self.spaces}<whileStatement>\n")
        self.spaces = self.spaces + "  "

        #Write 'while'
        self.write_line()
        
        
        #Write '('
        self.input.hasMoreTokens()
        self.write_line()

        self.input.hasMoreTokens()
        self.compile_Expression()

        #Write ')'
        self.write_line()

        #Write '{'
        self.input.hasMoreTokens()
        self.write_line()


        #Preload tokenizer, and write statements
        self.input.hasMoreTokens()
        self.compile_Statements()

        # !!!!!!!!!! Write end Curly brace '}'
        # !!!!!!!!!! self.write_line()

        
        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</whileStatement>\n")

        #Preload for next round through Statements
        self.input.hasMoreTokens()

    def compile_Return(self):
        self.out.write(f"{self.spaces}<returnStatement>\n")
        self.spaces = self.spaces + "  "

        #Write 'return'
        self.write_line()
        
        self.input.hasMoreTokens()
        if self.input.get_Token() != ';':
            self.compile_Expression()

        #Write ';'
        self.write_line()
        
        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</returnStatement>\n")

        #Preload for next round through Statements
        self.input.hasMoreTokens()

    def compile_If(self):
        self.out.write(f"{self.spaces}<ifStatement>\n")
        self.spaces = self.spaces + "  "
        
        #Write 'if'
        self.write_line()
        
        #Write "("
        self.input.hasMoreTokens()
        self.write_line()


        self.input.hasMoreTokens()
        self.compile_Expression()

        #Write ')'
        self.write_line()

        #Write '{'
        self.input.hasMoreTokens()
        self.write_line()


        #Preload tokenizer, and write statements
        self.input.hasMoreTokens()
        self.compile_Statements()

        # !!!!!!!!!! Write end Curly brace '}'
        # !!!!!!!!!  self.write_line()



        self.input.hasMoreTokens()
        

        # Check for else (if not else, this will pre-load tokenizer)
        if self.input.get_Token() == 'else':

            #Write 'else'
            self.write_line()
        
            # Write '{'
            self.input.hasMoreTokens()
            self.write_line()

            #Preload tokenizer, and write statements
            self.input.hasMoreTokens()
            self.compile_Statements()

            # !!!!!!!!!!!! Write end Curly brace '}'
            # !!!!!!!!!!! self.write_line()

            # Preload tokenizer for next round through statements
            self.input.hasMoreTokens()

            self.spaces = self.spaces[:2]
            self.out.write(f"{self.spaces}</ifStatement>\n")
            
        else:
            self.spaces = self.spaces[:2]
            self.out.write(f"{self.spaces}</ifStatement>\n")
        
    def compile_Expression_List(self):
        self.out.write(f"{self.spaces}<expressionList>\n")
        self.spaces = self.spaces + "  "

        #Load tokenizer
        self.input.hasMoreTokens()


        while self.input.get_Token() != ")":
            if self.input.get_Token() == ",":
                #12 spaces
                self.write_line()
                self.input.hasMoreTokens()
            else:
                #TOKENIZER IS LOADED (and should be, if this is a later run through)
                self.compile_Expression()

        #LEAVES UNLOADED, HAVING ALREADY WRITTEN ')'
        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</expressionList>\n")

        #Write ')'
        self.write_line()

    def compile_Expression(self):
        #Enters Loaded

        self.out.write(f"{self.spaces}<expression>\n")
        self.spaces = self.spaces + "  "

        self.compile_Term()

        
        while self.input.get_Token() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            #Writes op
            if self.input.get_Token() == '<':
                self.out.write(f"{self.spaces}<{self.input.get_Type()}> &lt; </{self.input.get_Type()}>\n")
            elif self.input.get_Token() == '>':
                self.out.write(f"{self.spaces}<{self.input.get_Type()}> &gt; </{self.input.get_Type()}>\n")
            elif self.input.get_Token() == '&':
                self.out.write(f"{self.spaces}<{self.input.get_Type()}> &amp; </{self.input.get_Type()}>\n")
            else:
                self.write_line()

            self.input.hasMoreTokens()
            self.compile_Term()

    
        #LEAVES LOADED
        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</expression>\n")

    def compile_Term(self):
        #Enters Loaded

        self.out.write(f"{self.spaces}<term>\n")
        self.spaces = self.spaces + "  "

        # If term is an expression
        if self.input.get_Token() == '(':
            
            #Writes '('
            self.write_line()
            self.input.hasMoreTokens()
            self.compile_Expression()

            
            #Writing ')'
            self.write_line()

            #LOADING FOR EXIT
            self.input.hasMoreTokens()

        elif self.input.get_Token() in ['-', '~']:
            #Writes '~' or '-'
            self.write_line()
            self.input.hasMoreTokens()
            self.compile_Term()

        elif self.input.get_Type() == 'identifier':

            #Writes identifier
            self.write_line()

            #LOAD TOKENIZER
            self.input.hasMoreTokens()

            if self.input.get_Token() == '[':
                #Writes "["
                self.write_line()

                self.input.hasMoreTokens()
                self.compile_Expression()

                #Writing ']'
                self.write_line()

                #LOAD FOR EXIT
                self.input.hasMoreTokens()

            elif self.input.get_Token() == '(':
                #Writes "("
                self.write_line()

                self.compile_Expression_List()

                #Writes ")"
                self.input.hasMoreTokens()
                self.write_line()

                #LOAD FOR EXIT
                self.input.hasMoreTokens()

            elif self.input.get_Token() == '.':
                #Writes "."
                self.write_line()

                #Writes sub Name
                self.input.hasMoreTokens()
                self.write_line()

                #Writes "("
                self.input.hasMoreTokens()
                self.write_line()

                self.compile_Expression_List()

                #LOAD FOR EXIT
                self.input.hasMoreTokens()
        #Write Constant
        else:
            #Writes constant
            self.write_line()

            #LOAD FOR EXIT
            self.input.hasMoreTokens()

        #compile_Type leaves LOADED TOKENIZER
        self.spaces = self.spaces[:2]
        self.out.write(f"{self.spaces}</term>\n")

main()