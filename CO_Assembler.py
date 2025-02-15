def read_file(file):
    with open(file,'r') as f:
        instructions=[]
        opcodes=[]
        lines=f.readlines()
    for i in lines:
        i=i.strip()
        if ':' in i:
            label,rest=i.split(':')
            label=label.strip()
            rest=rest.strip()
            instruction=rest.split()[0]
            rd,rs1,rs2=rest.split()[1].split(',')
            instructions.append(instruction)
            opcodes.append([rd,rs1,rs2])
        else:
            instruction=i.split()[0]
            rest=i.split()[1]
            rd,rs1,rs2=rest.split(',')
            instructions.append(instruction)
            opcodes.append([rd,rs1,rs2])
    return instructions,opcodes

Rtype={
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
instructions,opcodes=read_file(filename)

for a in range(len(instructions)):
    i=instructions[a]
    j=opcodes[a]
    if i in Rtype.keys():
        rd,rs1,rs2=j[0],j[1],j[2]
        rd,rs1,rs2=regs_binary[rd],regs_binary[rs1],regs_binary[rs2]
        func7,func3,opcode=Rtype[i][0],Rtype[i][1],Rtype[i][2]
        answer=func7+rs2+rs1+func3+rd+opcode
        result.append(answer)

with open("output.txt",'a') as f:
    for i in result:
        final=i+'\n'
        f.write(final)
