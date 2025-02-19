def read_file(file):
    with open(file, 'r') as f:
        instructions = []
        opcodes = []
        labels = {}
        lines = f.readlines()

    index = 0 
    for line in lines:
        line = line.strip()
        if ':' in line:
            label, rest = line.split(':', 1)
            label = label.strip()
            rest = rest.strip()
            labels[label] = index
        else:
            rest = line

        if rest:
            parts = rest.split()
            instruction = parts[0]
            operands = []
            if len(parts) > 1:
                operand_string = parts[1].replace(" ", "")
                operands = operand_string.split(',')

                for i in range(len(operands)):
                    if '(' in operands[i] and ')' in operands[i]:
                        imm_val, reg = operands[i].split('(')
                        reg = reg.replace(')', '')
                        operands[i] = imm_val
                        operands.insert(i + 1, reg)

            instructions.append(instruction)
            opcodes.append(operands)
        index += 1
    return instructions, opcodes, labels


def instruction_error(instruction):
    if instruction not in Rtype.keys() and instruction not in Stype.keys() and instruction not in Jtype.keys() and instruction not in Itype.keys() and instruction not in Btype.keys():
        return f"The instruction '{instruction}' is wrong."
    return None

def opcode_error(opcode):
    errors = []
    for i in opcode:
        if not i.isnumeric() and i not in regs_binary.keys():
            errors.append(f"The input value '{i}' is wrong.")
    return errors

Rtype = {
    "add": ["0000000", "000", "0110011"],
    "sub": ["0100000", "000", "0110011"],
    "sll": ["0000000", "001", "0110011"],
    "slt": ["0000000", "010", "0110011"],
    "sltu": ["0000000", "011", "0110011"],
    "xor": ["0000000", "100", "0110011"],
    "srl": ["0000000", "101", "0110011"],
    "or": ["0000000", "110", "0110011"],
    "and": ["0000000", "111", "0110011"]
}

Stype={
    "sw": ["000","0110011"]
}

Jtype={
    "jal": ["1101111"]
}

Btype = {
    "beq":  ["000", "1100011"],
    "bne":  ["001", "1100011"],
    "blt":["100","1100011"]
}


Itype = {
    "addi":  ["000", "0010011"],
    "lw":   ["010", "0000011"],
    "jalr": ["000", "1100111"]
}

regs_binary = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
    "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "fp": "01000",
    "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101",
    "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010",
    "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111",
    "s8": "11000", "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100",
    "t4": "11101", "t5": "11110", "t6": "11111"
}

result=[]
filename=input("Enter the File Name:")
instructions, opcodes, labels = read_file(filename)

for a in range(len(instructions)):
    i = instructions[a]
    j = opcodes[a]
    instr_error=instruction_error(i)
    if instr_error:
        result.append(instr_error + f" (At Line {a+1})")
        continue
    errors=opcode_error(j)
    if errors:
        for error in errors:
            result.append(error + f" (At Line {a+1})")
        continue

    if i in Rtype.keys():
        rd, rs1, rs2 = j[0], j[1], j[2]
        rd, rs1, rs2 = regs_binary[rd], regs_binary[rs1], regs_binary[rs2]
        func7, func3, opcode = Rtype[i][0], Rtype[i][1], Rtype[i][2]
        answer = func7 + rs2 + rs1 + func3 + rd + opcode
        result.append(answer)
    elif i in Stype.keys():
        rs2, imm, rs1 = j[0], j[1], j[2]
        rs2, rs1 = regs_binary[rs2], regs_binary[rs1]
        imm_bin = format(int(imm), '012b')
        imm_high, imm_low = imm_bin[:7], imm_bin[7:]
        func3, opcode = Stype[i]
        answer = imm_high + rs2 + rs1 + func3 + imm_low + opcode
        result.append(answer)
    elif i in Jtype.keys():
        rd,imm=j[0],j[1]
        rd=regs_binary[rd]
        imm_bin=format(int(imm),'020b')
        imm_enc=imm_bin[0]+imm_bin[10:20]+imm_bin[9]+imm_bin[1:9]
        opcode=Jtype[i][0]
        answer=imm_enc+rd+opcode
        result.append(answer)
    elif i in Btype.keys():
        rs1, rs2, imm=j[0],j[1],j[2]
        rs2,rs1=regs_binary[rs2],regs_binary[rs1]
        imm_bin=format(int(imm),'012b')
        imm_high,imm_low=imm_bin[0]+imm_bin[2:8],imm_bin[8:12]+imm_bin[1]
        func3,opcode=Btype[i]
        answer=imm_high+rs2+rs1+func3+imm_low+opcode
        result.append(answer)
    elif i in Itype.keys():
        if i == 'lw':
            rd, imm, rs1=j[0],j[1],j[2]
            rd,rs1=regs_binary[rd],regs_binary[rs1]
            imm_bin=format(int(imm),'012b')
            func3,opcode=Btype[i]
            answer=imm_bin+rs1+func3+rd+opcode
            result.append(answer)
        else:
            rd, rs1, imm=j[0],j[1],j[2]
            rd,rs1=regs_binary[rd],regs_binary[rs1]
            imm_bin=format(int(imm),'012b')
            func3,opcode=Itype[i]
            answer=imm_bin+rs1+func3+rd+opcode
            result.append(answer)

with open("output.txt", 'a') as f:
    for i in result:
        final = i + '\n'
        f.write(final)