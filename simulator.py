reg = {'zero' : '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100', 't0':'00101', 't1': '00110', 't2': '00111','s0': '01000', 'fp': '01000', 's1': '01001','a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 'a4': '01110', 'a5': '01111','a6':'10000',  'a7':'10001', 's2': '10010', 's3': '10011', 's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011','t3': '11100', 't4': '11101', 't5':'11110', 't6': '11111'}
registers = {'zero' : '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100', 't0':'00101', 't1': '00110', 't2': '00111','s0': '01000', 'fp': '01000', 's1': '01001','a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 'a4': '01110', 'a5': '01111','a6':'10000',  'a7':'10001', 's2': '10010', 's3': '10011', 's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011','t3': '11100', 't4': '11101', 't5':'11110', 't6': '11111'}
bfncodes = {"beq": "000", "bne": "001", "bge":"101", "bgeu":"111", "blt": "100",  "bltu":"110"}
rfncodes = {"add": "000", "sub":"000", "sll":"001", "slt":"010", "sltu":"011", "xor":"100", "srl":"101", "or":"110","and":"111"}
acreg = {}
linecount = {}
value  = {}
memory = {}
findict = {}

for i in registers:
    value[reg[i]] = "0"*32

def addnum(a, b):
    sum = bin(int(a, 2) + int(b, 2))
    return(sum[2:])

def twoscp(a):
    cp = ''
    for i in range(len(str(a))):
        if a[i]=="1":
            cp+="0"
        else:
            cp+="1"
    b = ("0"*(len(str(a))-1))+"1"
    y = addnum(cp,b)
    return "1"*(32- len(y)) + y

def binarytoint(a):
    b = 0
    j = len(a)-1
    for i in range(len(a)):
        b += (int(a[i])) * (2 ** j)
        j-=1
    return b

def twoscptoint(a):
    new = ''
    if a[len(a)-1] == "1":
        for i in range(0, len(a)-1):
            if a[i] == "0":
                new+="1"
            else:
                new+="0"
        new+= "1"
        c = binarytoint(new)
        c = "-" +  str(c)
        return int(c)
    else:
        for i in range(0, len(a)):
            if a[i] == "0":
                new+="1"
            else:
                new+="0"
        d = addnum(new, "0"*(len(new)-1) + "1")
        c = binarytoint(d)
        c = "-" +  str(c)
        return int(c)

def inttobinary(a):
    sumn = ''
    if a == 0:
        return "0"*32
    while(a!=0):
        if (a == 1):
            a-=1
            sumn+="1"
        b = a%2
        sumn+=str(b)
        a = a//2
    return ("0" * (32 - len(sumn)) + sumn[::-1])

def convert(a,n):
    if (n==0):
        if a[0] == "1":
            return twoscptoint(a)
        else:
            return binarytoint(a)
    else:
        return binarytoint(a)

def converttohex(d):
    a = str(hex(int(d)))
    b = a[0:2] + "0"*(8 - len(a[2:])) + a[2:]
    return b
def a2bin(a, b):
    Sum = bin(int(a, 2) + int(b, 2))
    return (len(a) - len(Sum[2:]))* '0' + Sum[2:]
def sext(a):
    if a[0] == '0':
        return ((32 - len(a)) * '0') + a
    else:
        return ((32 - len(a)) * '1') + a
def twoc(a):
    cp = ''
    for i in range(len(str(a))):
        if a[i]=="1":
            cp+="0"
        else:
            cp+="1"
    b = "1"
    y = a2bin(cp,b)
    return sext(y)
def inttob(a):
    sumn = ''
    if a == 0:
        return "0"
    while(a!=0):
        if (a == 1):
            a-=1
            sumn+="1"
        b = a%2
        sumn+=str(b)
        a = a//2
    return sumn
def itb(a):
    if a >= 0:
        return sext(inttob(a))
    else:
        return twoc(inttob(a -(2*a)))

input_file=None
output_file=None
with open(input_file,'r') as f:
    lines=f.readlines()
with open (output_file,'w') as f:
    value['00010'] = "00000000000000000000000100000000"