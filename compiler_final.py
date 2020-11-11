import sys
import os

def main():
    f = sys.argv[1]
    
    if os.path.isfile(f):
        tzer = Tokenizer(f)
        write_file = open(f[:-4] + "vm", "w")
        comp = Compiler(tzer, write_file)
        comp.compile_Class()
        tzer.close()
        write_file.close()

    else:
        with os.scandir(f) as it:
            for entry in it:
                if entry.name.endswith('.jack'):
                    tzer = Tokenizer(entry)
                    write_file = open('/Users/StudioMac/Desktop/nand2tetris/projects/11/' + f + '/' + entry.name[:-4] + "vm", "w")
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
        self.input = tokenizer
        self.class_name = ""
        self.sym_tab = SymbolTable()
        self.vm = VMWriter(outputfile)
        self.arith_dict = {'+': 'add', '-': 'sub', '*': 'call Math.multiply 2', '/': 'call Math.divide 2', '&': 'and', '|': 'or', '<': 'lt', '>': 'gt', '=': 'eq'}
        self.args_temp = 0
        self.label1 = []
        self.label2 = []
        self.label3 = []
        self.counter = 0
    
    def compile_Class(self):
        if self.input.hasMoreTokens():
            # Current token: Keyword: Class
            # Current token: Name of class // Save self.class_name
            if self.input.hasMoreTokens():
                self.class_name = self.input.get_Token()
            #  Current token: Left curly '{'
            self.input.hasMoreTokens()
            # Compile everything within the {} for class
            while self.input.hasMoreTokens():
                if self.input.get_Token() in ['field', 'static']:
                    self.compile_Class_Var_Dec()
                elif self.input.get_Token() in ['constructor', 'function', 'method']:
                    self.compile_Subroutine()
                elif self.input.get_Token() == '}':
                    continue


    def compile_Class_Var_Dec(self):

        # Kind of variable already loaded in the previous function call

        #Saves current kind of variable being declared
        current_kind = self.input.get_Token()

        #Loads and stores Variable Type
        self.input.hasMoreTokens()
        current_type = self.input.get_Token()

        #Write Class_Var_Declarations
        while self.input.get_Token() != ';':
            self.input.hasMoreTokens()
            token = self.input.get_Token()
            if token not in [',', ';']:
                self.sym_tab.define(token, current_type, current_kind)

    
    def compile_Subroutine(self):

        # Create new Subroutine Symbol Table
        self.sym_tab.startSubroutine()

        #Type of subroutine already loaded in the previous function call

        sub_type = self.input.get_Token()

        #If type of sub is a method, update symbol table
        if sub_type == 'method':
            self.sym_tab.define('this', self.class_name, 'argument')

        #Loads and stores Return Type of Subroutine
        self.input.hasMoreTokens()

        #Loads and writes subroutineName  (Subroutine - Defined)
        self.input.hasMoreTokens()
        current_name = self.input.get_Token()

        #Current token: '('
        self.input.hasMoreTokens()
            

        self.compile_Parameter_List()
        

        # Current token: Write '{'
        self.input.hasMoreTokens()

        #Write VarDec
        self.input.hasMoreTokens()
        while self.input.get_Token() == 'var':
            self.compile_Var_Dec()

        self.vm.writeFunction(self.class_name + '.' + current_name, self.sym_tab.varCount('local'))

        if sub_type == 'constructor':
            self.vm.writePush('constant', str(self.sym_tab.varCount('field')))
            self.vm.writeCall('Memory.alloc', '1')
            self.vm.writePop('pointer', '0')

        elif sub_type == 'method':
            self.vm.writePush('argument', '0')
            self.vm.writePop('pointer', '0')

        self.compile_Statements()

    def compile_Parameter_List(self):

        # Current token: Either ')' or the first token of the parameter list
        self.input.hasMoreTokens()

        #Write Parameter List, if it exists
        while self.input.get_Token() != ")":

            #Compile type of argument
            current_type = self.input.get_Token()

            #Load name of Argument
            self.input.hasMoreTokens()

            #Compile name of argument - add to symbol tab, write xml
            token = self.input.get_Token()
            self.sym_tab.define(token, current_type, 'argument')

            #Load tokenizer for next round through while loop, or for ',' , or to to move on
            self.input.hasMoreTokens()

            if self.input.get_Token() == ',':
                self.input.hasMoreTokens()

        # Current token: ')'


    def compile_Var_Dec(self):

        #Kind of variable already loaded in the previous function call

        #Current Token: Variable Type
        self.input.hasMoreTokens()

        #Stores variable type in current_type and writes to xml
        current_type = self.input.get_Token()

        #Write Local Var_Declarations and Update Symbol Table
        while self.input.get_Token() != ';':
            self.input.hasMoreTokens()
            token = self.input.get_Token()
            if token not in [',', ';']:
                self.sym_tab.define(token, current_type, 'local')

        # Get tokenizer loaded, since it was loaded when we entered var_dec
        self.input.hasMoreTokens()

    def compile_Statements(self):

        #!!! TOKENIZER HAS TO ALREADY BE LOADED, COMING INTO STATEMENTS

        #Compile Statements, if they exist

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

        # Current token: '}'

    def compile_Do(self):

        #Starts loaded with 'do' as the token
        
        #Store subroutine/Class/variable name
        self.input.hasMoreTokens()
        current_name = self.input.get_Token()
        subname = current_name

        #Load ( or .
        self.input.hasMoreTokens()
        token = self.input.get_Token()

        #Set-up subroutine flag
        flag = False

        if token == '.':
            '''
            Unnecessary????????
            if self.sym_tab.kindOf(current_name) == None:
                #self.write_sym("Class - used")
                a = 1

            else:
                #variable holding a class - Used
                a = 1
            '''

            #Current token: Name of Subroutine
            self.input.hasMoreTokens()

            #Check to see if current_name is Class or Object ... Switch to Class if necessary

            if self.sym_tab.kindOf(current_name) != None:
                current_name = self.sym_tab.typeOf(current_name)
                flag = True

            current_name += ('.' + self.input.get_Token())

            #Current token: (
            self.input.hasMoreTokens()
        
        cur_kind = ''

        if '.' in current_name:
            if flag:
                cur_kind = self.sym_tab.kindOf(subname)
                if cur_kind == 'local':
                    self.vm.writePush('local', str(self.sym_tab.indexOf(subname)))
                elif cur_kind == 'field':
                    self.vm.writePush('this', str(self.sym_tab.indexOf(subname)))
        else:
            self.vm.writePush('pointer', '0')

        # At this point, tokenizer is UNLOADED
        self.compile_Expression_List()

        # Current token: ';'
        self.input.hasMoreTokens()

        #Write function call



        #HAVE TO DISTINGUISH BETWEEN FUNCTION VS METHOD HERE!!!!!!!!!!!!!!
        if '.' in current_name:
            if flag:
                self.vm.writeCall(current_name, str(1 + self.args_temp))
            else:
                self.vm.writeCall(current_name, str(self.args_temp))
        else:
            self.vm.writeCall(f'{self.class_name}.{current_name}', str(1 + self.args_temp))

        # !!!!!!! Because this is a DO statement, returned values are discarded
        self.vm.writePop('temp', '0')

        #Preload for next round through Statements
        self.input.hasMoreTokens()

    def compile_Let(self):

        #Current token: 'let'
        
        #Current token: varName 
        self.input.hasMoreTokens()

        current_name = self.input.get_Token()
        current_kind = self.sym_tab.kindOf(current_name)
        current_idx = self.sym_tab.indexOf(current_name)
        is_array = False

        #Current token: either '=' ,  or '[' if an array
        self.input.hasMoreTokens()

        if self.input.get_Token() == '[':

            is_array = True

            #Current token: [

            self.vm.writePush(self.sym_tab.kindOf(current_name), str(self.sym_tab.indexOf(current_name)))

            #Current token: first token of an expression
            self.input.hasMoreTokens()
            self.compile_Expression()

            #Current token: ']'   (Already loaded at end of compile_expression)

            self.vm.writeArithmetic('add')

            #Current token: '='
            self.input.hasMoreTokens()

        #Current token: first token of ensuing expression
        self.input.hasMoreTokens()
        self.compile_Expression()

        #If not an array:

        if not is_array:
            # Current token: ';' (Preloaded at end of compile_Expresssion)
            if current_kind == 'field':
                current_kind = 'this'
            self.vm.writePop(current_kind, str(current_idx))
        else:
            self.vm.writePop('temp', '0')
            self.vm.writePop('pointer', '1')
            self.vm.writePush('temp', '0')
            self.vm.writePop('that', '0')

        #Preload for next round through Statements
        self.input.hasMoreTokens()
    

    def compile_While(self):

        #Current token: 'while' (Already loaded)

        self.counter += 1
        self.label1.append("WHILE_LABEL_A" + str(self.counter))
        self.label2.append("WHILE_LABEL_B" + str(self.counter))

        #Current token: '('
        self.input.hasMoreTokens()

        self.vm.writeLabel(self.label1[-1])

        #Current token: First token of ensuing Expression
        self.input.hasMoreTokens()
        self.compile_Expression()

        #Current token: ')' (Already loaded after compile_Expression)

        self.vm.writeArithmetic('not')
        self.vm.writeIf(self.label2[-1])

        #Current token: '{'
        self.input.hasMoreTokens()

        #Preload tokenizer, and write statements
        self.input.hasMoreTokens()
        self.compile_Statements()

        # !!!!!!!!!! Write end Curly brace '}'
        # !!!!!!!!!! self.write_line()

        self.vm.writeGoto(self.label1[-1])
        self.vm.writeLabel(self.label2[-1])

        #Preload for next round through Statements
        self.input.hasMoreTokens()

        #Remove current labels from label lists
        self.label1.pop()
        self.label2.pop()

    def compile_Return(self):

        #Current token: 'return' (Already loaded)
        
        #Current token: either ';' or the first token of an Expression
        self.input.hasMoreTokens()

        if self.input.get_Token() != ';':
            self.compile_Expression()
        else:
            self.vm.writePush('constant', '0')

        #Current token: ';' (Already loaded)

        self.vm.writeReturn()

        #Preload for next round through Statements
        self.input.hasMoreTokens()

    def compile_If(self):
        
        #Current token: 'if' (Already loaded)
        
        #Current token: "("
        self.input.hasMoreTokens()

        #Current token: First token of expression
        self.input.hasMoreTokens()
        self.compile_Expression()

        #Write Flow of control commands
        self.counter += 1
        self.label1.append("IF_LABEL_A" + str(self.counter))
        self.label2.append("IF_LABEL_B" + str(self.counter))

        self.vm.writeArithmetic('not')
        self.vm.writeIf(self.label1[-1])

        #Current token: ')' (already loaded from compile_Expression)

        #Current token: '{'
        self.input.hasMoreTokens()

        #Preload tokenizer, and write statements
        self.input.hasMoreTokens()
        self.compile_Statements()

        # !!!!!!!!!! Write end Curly brace '}'
        # !!!!!!!!!  self.write_line()

        #Current token: 'else' or continuing on
        self.input.hasMoreTokens()

        self.vm.writeGoto(self.label2[-1])
        self.vm.writeLabel(self.label1[-1])
        

        # Check for else
        if self.input.get_Token() == 'else':

            #Current token: 'else'
        
            # Current token: '{'
            self.input.hasMoreTokens()

            #Preload tokenizer, and write statements
            self.input.hasMoreTokens()
            self.compile_Statements()

            # !!!!!!!!!!!! Write end Curly brace '}'
            # !!!!!!!!!!! self.write_line()

            # Preload tokenizer for next round through statements
            self.input.hasMoreTokens()

        self.vm.writeLabel(self.label2[-1])

        #Remove current labels from label lists
        self.label1.pop()
        self.label2.pop()

    def compile_Expression_List(self):

        #Load tokenizer
        self.input.hasMoreTokens()

        nArgs = 0


        while self.input.get_Token() != ")":
            if self.input.get_Token() == ",":
                self.input.hasMoreTokens()
            else:
                #TOKENIZER IS LOADED (and should be, if this is a later run through)
                self.compile_Expression()
                nArgs +=1

        self.args_temp = nArgs

        #LEAVES UNLOADED, HAVING ALREADY COMPILED ')'

    def compile_Expression(self):

        #Enters Loaded

        self.compile_Term()

        #Leaves compile_Term loaded (loaded right now)

        
        while self.input.get_Token() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:

            current_op = self.input.get_Token()

            self.input.hasMoreTokens()
            self.compile_Term()

            #Writes op

            self.vm.writeArithmetic(self.arith_dict[current_op])

    
        #LEAVES LOADED

    def compile_Term(self):

        #Enters Loaded

        # If term is an expression
        if self.input.get_Token() == '(':
            
            #Current token: '('

            #Current token: First token of Expression
            self.input.hasMoreTokens()
            self.compile_Expression()

            
            #Current token: ')'

            #LOADING FOR EXIT
            self.input.hasMoreTokens()

        elif self.input.get_Token() in ['-', '~']:

            #Current token: '~' or '-'
            un_operator = self.input.get_Token()

            #Current token: First token of Term
            self.input.hasMoreTokens()
            self.compile_Term()

            #Write unary operator
            if un_operator == '-':
                self.vm.writeArithmetic('neg')
            elif un_operator == '~':
                self.vm.writeArithmetic('not')

        elif self.input.get_Type() == 'identifier':

            #Current token: identifier

            #Compile identifier, if not class or subRoutine
            token = self.input.get_Token()
            current_kind = self.sym_tab.kindOf(token)
            if current_kind != None:
                if current_kind == 'field':
                    self.vm.writePush('this', str(self.sym_tab.indexOf(token)))
                else:
                    self.vm.writePush(current_kind, str(self.sym_tab.indexOf(token)))
                

            #LOAD TOKENIZER
            self.input.hasMoreTokens()

            if self.input.get_Token() == '[':

                #Current token: "["

                #Current token: First token of expression
                self.input.hasMoreTokens()
                self.compile_Expression()

                #Current token: ']' (Loaded in compile_Expression)

                self.vm.writeArithmetic('add')
                self.vm.writePop('pointer', '1')
                self.vm.writePush('that', '0')

                #LOAD FOR EXIT
                self.input.hasMoreTokens()

            elif self.input.get_Token() == '(':

                #subroutine call identifier was previous token   Subroutine identifier  -- Used

                #Current token: "("

                #Enters Expression_List unloaded
                self.compile_Expression_List()

                #Current token: ")"
                self.input.hasMoreTokens()

                self.vm.writeCall(f"{self.class_name}.{token}", str(self.args_temp))

                #LOAD FOR EXIT
                self.input.hasMoreTokens()

            elif self.input.get_Token() == '.':

                # token = current Class or object identifier
                #Class identifier - Used

                #Current token: "."

                #See if token (identifier) is in symbol table (is it an object?)
                object_vs_class = self.sym_tab.kindOf(token)
                if object_vs_class == None:
                    #Current token: sub Name   - Subroutine identifier -- Used
                    self.input.hasMoreTokens()
                    subR = self.input.get_Token()

                    #Current token: "("
                    self.input.hasMoreTokens()

                    #Enters unloaded
                    self.compile_Expression_List()

                    #NEEDS TO RETURN TO ME, THE CODER, THE NUMBER OF EXPRESSIONS
                    #NEEDS TO WRITE call token.subR expNum
                    self.vm.writeCall(f"{token}.{subR}", str(self.args_temp))

                    #LOAD FOR EXIT
                    self.input.hasMoreTokens()

                else:
                    #Push self as first argument

                    # !!!!!!!!!!!!!!! DANGER !!!!!!!!!!!
                    if current_kind == None:
                        self.vm.writePush(self.sym_tab.kindOf(token), str(self.sym_tab.indexOf(token)))
                    
                    #Turn object name into Class name
                    token = self.sym_tab.typeOf(token)

                    #Current token: sub Name   - Subroutine identifier -- Used
                    self.input.hasMoreTokens()
                    subR = self.input.get_Token()

                    #Current token: "("
                    self.input.hasMoreTokens()

                    #Enters unloaded
                    self.compile_Expression_List()

                    if object_vs_class == None:
                        self.vm.writeCall(f"{token}.{subR}", str(self.args_temp))
                    else:
                        self.vm.writeCall(f"{token}.{subR}", str(self.args_temp + 1))

                    #LOAD FOR EXIT
                    self.input.hasMoreTokens()

                
        #Write Constant
        else:
            #Current token: constant
            current_type = self.input.get_Type()
            token = self.input.get_Token()
            if current_type == 'integerConstant':
                self.vm.writePush('constant', str(self.input.get_Token()))
            elif current_type == 'stringConstant':
                token = self.input.get_Token()
                self.vm.writePush('constant', str(len(token)))
                self.vm.writeCall('String.new', '1')
                for char in token:
                    self.vm.writePush('constant', str(ord(char)))
                    self.vm.writeCall('String.appendChar', '2')
            elif token == 'this':
                self.vm.writePush('pointer', '0')
            elif token == 'true':
                self.vm.writePush('constant', '1')
                self.vm.writeArithmetic('neg')
            elif token in ['false', 'null']:
                self.vm.writePush('constant', '0')
            
            #LOAD FOR EXIT
            self.input.hasMoreTokens()

        #compile_Term leaves LOADED TOKENIZER

class SymbolTable:
    def __init__(self):
        self.class_level = {}
        self.sub_level = {}
        self.indices = {'static': -1, 
                        'field': -1,
                        'argument': -1,
                        'local': -1}

    def startSubroutine(self):
        self.sub_level = {}
        self.indices['argument'] = -1
        self.indices['local'] = -1

    def define(self, name, typ, kind):
        if kind in ['static', 'field']:
            x = self.class_level
        else:
            x = self.sub_level

        self.indices[kind] += 1
        x[name] = (typ, kind, self.indices[kind])

    def varCount(self, kind):
        return self.indices[kind] + 1

    def kindOf(self, name):
        kind = self.sub_level.get(name)
        if kind == None:
            class_kind = self.class_level.get(name)
            if class_kind == None:
                return None
            else:
                return class_kind[1]
        else:
            return kind[1]
    
    def typeOf(self, name):
        typ = self.sub_level.get(name)
        if typ == None:
            class_typ = self.class_level.get(name)
            return class_typ[0]
        else:
            return typ[0]

    def indexOf(self, name):
        idx = self.sub_level.get(name)
        if idx == None:
            class_idx = self.class_level.get(name)
            return class_idx[2]
        else:
            return idx[2]

class VMWriter:

    def __init__(self, outputfile):
        self.out = outputfile

    def writePush(self, segment, index):
        # Can be:
        # constant, argument, local, static, this, that, pointer, temp
        self.out.write('push ' + segment + " " + index + '\n')

    def writePop(self, segment, index):
        self.out.write('pop ' + segment + " " + index + '\n')

    def writeArithmetic(self, command):
        #Can be: add, sub, neg, eq, gt, lt, and, or, not
        self.out.write(command + '\n')
    
    def writeLabel(self, label):
        self.out.write(f"label {label}\n")

    def writeGoto(self, label):
        self.out.write(f"goto {label}\n")

    def writeIf(self, label):
        self.out.write(f"if-goto {label}\n")

    def writeCall(self, name, nArgs):
        self.out.write(f"call {name} {str(nArgs)}\n")

    def writeFunction(self, name, nLocals):
        self.out.write(f'function {name} {nLocals}\n')

    def writeReturn(self):
        self.out.write('return\n')
main()

#Git Practice
#branch test