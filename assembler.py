import sys






RAM = 16


def dec_to_bin(decimal):
	binary = bin(decimal)
	binary = binary[2:]
	for bit in range ((16 - len(binary))):
		binary = "0" + binary
	return binary

class Parser:
	def __init__(self, line):
		self.code = line
		self.jump = "000"
		self.dest = "000"
		self.command = "0000000"

	def get_a_binary(self):
		global RAM
		if self.code[1:].isnumeric():
			decimal = int(self.code[1:])
			return dec_to_bin(decimal)

		else:
			symbol = sym.get(self.code[1:])
			if symbol == None:
				sym[self.code[1:]] = RAM
				binary = dec_to_bin(RAM)
				RAM += 1
				return binary
			return dec_to_bin(int(symbol))

	def get_d_binary(self):
		has_dest = False
		has_jump = False
		equal_loc = self.code.find("=")
		if equal_loc != -1:
			has_dest = True
		if self.code.find(";") != -1:
			has_jump = True
		if has_dest:
			self.dest = calc_dest(self.code[:equal_loc])
			self.code = self.code[(equal_loc + 1):]
		if has_jump:
			self.jump = calc_jump(self.code[-2:])
			self.code = self.code[:-4]
		self.command = calc_command(self.code)
		return "111" + self.command + self.dest + self.jump

		


def calc_dest(dest):
	code = ""
	if dest.find("A") != -1:
		code = code + "1"
	else:
		code = code + "0"
	if dest.find("D") != -1:
		code = code + "1"
	else:
		code = code + "0"
	if dest.find("M") != -1:
		code = code + "1"
	else:
		code = code + "0"
	return code

def calc_jump(jump):
	if jump == "GT":
		return "001"
	elif jump == "MP":
		return "111"
	elif jump == "EQ":
		return "010"
	elif jump == "GE":
		return "011"
	elif jump == "LT":
		return "100"
	elif jump == "NE":
		return "101"
	else:
		return "110"

def calc_command(com):
	if com.find("M") != -1:
		if com[0] == "D":
			if com == "D+M":
				return "1000010"
			elif com == "D-M":
				return "1010011"
			elif com == "D&M":
				return "1000000"
			else:
				return "1010101"
		elif com[0] == "M":
			if com == "M":
				return "1110000"
			elif com == "M+1":
				return "1110111"
			elif com == "M-1":
				return "1110010"
			elif com == "M-D":
				return "1000111"
		elif com == "!M":
			return "1110001"
		else:
			return "1110011"
	elif com[0] == "D":
		if com == "D":
			return "0001100"
		elif com == "D+1":
			return "0011111"
		elif com == "D-1":
			return "0001110"
		elif com == "D+A":
			return "0000010"
		elif com == "D-A":
			return "0010011"
		elif com == "D&A":
			return "0000000"
		else:
			return "0010101"
	elif com[0] == "A":
		if com == "A":
			return "0110000"
		elif com == "A+1":
			return "0110111"
		elif com == "A-1":
			return "0110010"
		elif com == "A-D":
			return "0000111"
	elif com == "0":
		return "0101010"
	elif com == "1":
		return "0111111"
	elif com == "-1":
		return "0111010"
	elif com == "!D":
		return "0001101"
	elif com == "!A":
		return "0110001"
	elif com == "-D":
		return "0001111"
	elif com == "-A":
		return "0110011"


def erase_comments(line):
	newline = ""
	for char in line:
		if char == "/":
			break
		newline = newline + char
	return newline

sym = {
	"SP":"0", "LCL": "1", "ARG": "2", "THIS": "3",
	"THAT":"4", "SCREEN":"16384", "KBD":"24576"
}
for n in range(16):
	sym[("R" + str(n))] = n


def main():
	new_file = open(sys.argv[1][:-3] + "hack", "w")
	with open(sys.argv[1]) as f:
		counter = 0
		for line in f:
			## Removes whitespace from line
			newline = ''.join(line.split())
			if len(newline) == 0 or newline[:2] == "//":
				continue

			## define labels
			if newline[0] == "(":
				end = newline.find(")")
				sym[newline[1:end]] = counter
				counter = counter - 1

			counter = counter + 1

	with open(sys.argv[1]) as f:
		for line in f:
			## Removes whitespace from line
			line = ''.join(line.split())
			if len(line) == 0 or line[:2] == "//":
				continue

			## erases any leftover comments (at end of string)
			newline = erase_comments(line)

			## initialize Parser object
			instruction = Parser(newline)

			if newline[0] == "(":
				continue

			## translate A instructions
			elif newline[0] == "@":
				code = instruction.get_a_binary()

			## translate C instructions
			else:
				code = instruction.get_d_binary()
			new_file.write(code + "\n")

			






main()