"""
Hardware language translations.

These mainly are split into A operations (@ or address ops, managing data in the RAM)
and C operations (control, dictating what operations to perform with said addressess).

the Hack computer model runs on 3 addressess, D (data storage), A (address storage), M (selected storage)
note that D and A are independent registers while M is a RAM location.
i.e. D, A are registers. M = RAM[A]
"""

import RAMchip
from ALUchip import inttobit, twoscomp, hack


def init_reg(newRAM=None):
    """
    initializing the 3 registers on import

    leaving possibility of importing RAM - I imagine it will need to be integratable to one RAM unit
    when the whole computer is in use.
    """
    if newRAM == None:
        newRAM = RAMchip.RAM()

    newRAM.write(RAMchip.register(inttobit(0)), address = 0) #need to fill slot with null otherwise its an empty array.
    return RAMchip.register(inttobit(0)), RAMchip.register(inttobit(0)), newRAM.read(0)

def c_command_parser(command):
    """
    splits up the Cop string
    """
    dest = None
    jump = None

    if "=" in command:
        dest, command = command.split("=", 1)

    if ";" in command:
        comp, jump = command.split(";", 1)
    else:
        comp = command
    return dest, comp, jump

def prog_counter(jump):
    """
    This isn'nt meant to be run. just a sort of pseudo-example of how jump alters the functionality in a python script.
    """
    PC = 0
    while True:
        instruction = ROM[PC]
    # execute instruction
    ####!!!not sure this actually runs like this but the instruction should be excecuted here.
    #could use the dictionary binops_j
    # decide what happens to PC
        if jump_condition:
            PC = A
        else:
            PC += 1
    return PC #Execute instruction at the location

def Cop(x, RAM, A, D, M=None):
    """
    input symbolic language and return binary command.
    x = "dest=comp;jump"
    i = 111accccccdddjjj

    #RAM might be chamged (via M) depending on DEST.

    symbolic command library for CPU(ALU) instructions

    111accccccdddjjj (16bit)
    C operations are defined by the initial 111.

    cccccc are the ALU instructions (see ALUchip.py)
    a dictates where to use M or A with D. e.g. 1000000 is D&M while 0000000 is D&A.

    ddd are where to store.

    jjj condition where to jump to next instruction.
    """
    dest, comp, jump = c_command_parser(x)

    if M == None:
        M = RAM.read(address=twoscomp(A))

    binops_c = {
            "0":      [0,1,0,1,0,1,0],
            "1":      [0,1,1,1,1,1,1],
            "-1":     [0,1,1,1,0,1,0],
            "D":      [0,0,0,1,1,0,0],
            "A":      [0,1,1,0,0,0,0],
            "!D":     [0,0,0,1,1,0,1],
            "!A":     [0,1,1,0,0,0,1],
            "-D":     [0,0,0,1,1,1,1],
            "-A":     [0,1,1,0,0,1,1],
            "D+1":    [0,0,1,1,1,1,1],
            "A+1":    [0,1,1,0,1,1,1],
            "D-1":    [0,0,0,1,1,1,0],
            "A-1":    [0,1,1,0,0,1,0],
            "D+A":    [0,0,0,0,0,1,0],
            "D-A":    [0,0,1,0,0,1,1],
            "A-D":    [0,0,0,0,1,1,1],
            "D&A":    [0,0,0,0,0,0,0],
            "D|A":    [0,0,1,0,1,0,1],
            "0":      [1,1,0,1,0,1,0],
            "1":      [1,1,1,1,1,1,1],
            "-1":     [1,1,1,1,0,1,0],
            "D":      [1,0,0,1,1,0,0],
            "M":      [1,1,1,0,0,0,0],
            "!D":     [1,0,0,1,1,0,1],
            "!M":     [1,1,1,0,0,0,1],
            "-D":     [1,0,0,1,1,1,1],
            "-M":     [1,1,1,0,0,1,1],
            "D+1":    [1,0,1,1,1,1,1],
            "M+1":    [1,1,1,0,1,1,1],
            "D-1":    [1,0,0,1,1,1,0],
            "M-1":    [1,1,1,0,0,1,0],
            "D+M":    [1,0,0,0,0,1,0],
            "D-M":    [1,0,1,0,0,1,1],
            "M-D":    [1,0,0,0,1,1,1],
            "D&M":    [1,0,0,0,0,0,0],
            "D|M":    [1,0,1,0,1,0,1],
            }

    binops_d = {
            'null': [0,0,0], #notstored
            'M': [0,0,1], # Mreg = RAM[A]
            'D': [0,1,0], #D reg
            'DM': [0,1,1], #both D and M
            'A': [1,0,0], #A reg
            'AM': [1,0,1], # both A & M
            'AD': [1,1,0], # both A & D
            'ADM': [1,1,1] # all 3
            }

    binops_j = {
            'null': [0,0,0], #no jump
            'JGT': [0,0,1], #Jump if comp>0
            'JEQ': [0,1,0], #if comp = 0
            'JGE': [0,1,1], #comp >= 0
            'JLT': [1,0,0], #comp< 0
            'JNE': [1,0,1], #comp != 0
            'JLE': [1,1,0], #comp <= 0
            'JMP': [1,1,1], #always jump
            }
    ###Not sure what this actually does in a python version?

    c_bin = binops_c[comp]

    if c_bin[0] == 0:
        result = hack(c_bin[1],c_bin[2],c_bin[3],c_bin[4],c_bin[5],c_bin[6], D, A)[0]
    if c_bin[0] == 1:
        result = hack(c_bin[1],c_bin[2],c_bin[3],c_bin[4],c_bin[5],c_bin[6], D, M)[0]

    if dest is not None:
        d_bin = binops_d[dest]
        if d_bin[0] == 1:
            A = result
        if d_bin[1] == 1:
            D = result
        if d_bin[2] == 1:
            M = result

    RAM.write(M, address=twoscomp(A))

    if dest is None:
        d_bin = binops_d['null']

    if jump is not None:
        j_bin = binops_j[jump]
    if jump is None:
        j_bin = []

    i = [1,1,1] + c_bin + d_bin + j_bin

    return i, RAM, A, D, M


def Aop(x, RAM):
    """
    @x = @0vvvvvvvvvvvvvvv
    input symbolic language, outputs binary operation and updated M register (M=RAM[A]).

    #RAM is unchanged, it just looks up an address

    A instruction
    @ RAM address register location

    0vvvvvvvvvvvvvvv
    A operations are defined by initial 0
    v's are the 15 bit binary location from 0-32767

    dest = comp ; jump
    (if dest is empty, compute ; jump i.e. do something and move on).
    (if jump is empty, destination = computation, compute and save).
    (can do both at the same time, save computation and move on dest = comp;jump).
    dest = D, comp = M jump
    """
    i = inttobit(x)

    #need to set a Null bit if there is nothing in RAM.
    M = RAM.read(address=x)
    if len(M) == 0:
        RAM.write(inttobit(0), address=x)
        M = RAM.read(address=x)
    return M, i, RAM


if __name__ == "__main__":
    """
    testing addition with 2 RAM locations
    """

    #set 2 numbers to be added form RAM locations
    x = 5
    y = 17
    print(f"testing the addition of {x} and {y} manually")

    print("initializing A, D, registers and M from the RAM.")
    RAM = RAMchip.RAM()
    print("@0 - A selects 0 address in RAM")
    A, D, M = init_reg(RAM)
    RAM.write(input = inttobit(x), address = 0)
    RAM.write(input = inttobit(y), address = 1)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")
    print("D=M - assigning data")
    D = RAM.read(0)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("@1 -")
    A = inttobit(1)
    M = RAM.read(address=twoscomp(A))
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print(f"D=D+M -D+M is a=1 cccccc = 000010")
    D = hack(0,0,0,0,1,0, D, M)[0]
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("@2 -")
    A = inttobit(2)
    M = RAM.read(address=twoscomp(A))
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("M=D -")
    RAM.write(input = D, address = twoscomp(A))
    answer = twoscomp(RAM.read(2))

    #Check output
    print(f" {x} + {y} = {answer}")
    z = x+y
    if z == answer:
        print("Passed!")
    if z != answer:
        print("failed.")

    print(f"\n\nTesting the addition of {x} and {y} with C & A operations")

    print("resetting RAM and registers")
    RAM = RAMchip.RAM()
    A, D, M = init_reg(RAM)
    RAM.write(input = inttobit(x), address = 0)
    RAM.write(input = inttobit(y), address = 1)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("@0 - A selects 0 address in RAM")
    M, A, RAM = Aop(0, RAM)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("D=M - assigning data")
    i, RAM, A, D, M = Cop("D=M", RAM, A, D, M)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("@1 -")
    M, A, RAM = Aop(1, RAM)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print(f"D=D+M -D+M is a=1 cccccc = 000010")
    i, RAM, A, D, M = Cop("D=D+M", RAM, A, D, M)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("@2 -")
    M, A, RAM = Aop(2, RAM)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    print("M=D -")
    i, RAM, A, D, M = Cop("M=D", RAM, A, D, M)
    print(f"A: {A}, \n D: {D}, \n M: {M}, \n")

    RAM.write(M, twoscomp(A))
    #Check output
    answer = twoscomp(RAM.read(2))
    z = x+y
    if z == answer:
        print("Passed!")
    if z != answer:
        print("failed.")
