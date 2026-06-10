"""
Nand is the lowest abstraction in nand to tetris - Takes two binary inputs and returns 1.

1 + 1 -> 0
1 + 0 -> 1
0 + 0 -> 1
0 + 1 -> 1

An abastraction is logical behaviour without explanation.
We express binary in 0,1 (rather than True False). 

Nand are the fundamental gates. You buy these and use a soldering gun to make nand, xor etc.


Added the letter l where python has a predefind word for the gate name.

"""

def land(a,b):
    if (a == b and a == 1): return 1
    return 0

def lnot(a):
    if (a == 0): return 1
    if (a == 1): return 0

def lor(a,b):
    if (a == 0 and b == 0): return 0
    return 1

def xor(a,b):
    """
    not or, can also be written if a!=b return 1 else 0.
    """
    return lor(land(a, lnot(b)),land(lnot(a), b))

def nand(a,b):
    if (a == 1 and b == 1): return 0
    return 1

def mux(a,b,sel):
    """
    Short for multiplexer.
    The 3rd bit, sel, selects the output from the inputs a and b.
    """
    if sel == 0: return a
    return b

def dmux(a,sel):
    """
    Demulitplexer. returns 2 bits a and 0. The order is determined by sel. 
    """
    if sel == 0: return a, 0
    return 0, a

if __name__ == "__main__":
    cases = [[0,0],[0,1],[1,0],[1,1]]

    nand_answers = [1,1,1,0]    
    print("testing nand")
    for i, case in enumerate(cases):
        if (nand(case[0],case[1]) == nand_answers[i]): print(f"{case[0]},{case[1]} Passed")
        else: print(f"{case[0]},{case[1]} Failed, output {nand(case[0],case[1])}")

    xor_answers = [0,1,1,0]    
    print("testing xor")
    for i, case in enumerate(cases):
        if (xor(case[0],case[1]) == xor_answers[i]): print(f"{case[0]},{case[1]} Passed")
        else: print(f"{case[0]},{case[1]} Failed")

    mux_answers = [0,0,1,1,0,1,0,1]
    sel = [0,1]
    print("testing multiplexer")
    for s in sel:
        for i, case in enumerate(cases):
            if (mux(case[0],case[1], s) == mux_answers[s*4 + i]): print(f"{case[0]},{case[1]}, {s} Passed")
            else: print(f"{case[0]},{case[1]}, {s} Failed, output {mux(case[0],case[1], s)} ")

    a = 2 #dummy variable (not a bit).
    dmux_answers = [[a,0],[0,a]]
    print("testing Demultiplexer")
    for s in sel:
        if (list(dmux(a, s)) == dmux_answers[s]): print(f"{s} Passed")
        else: print(f"{s} Failed, output {dmux(a, s)} ")

    
    
    