"""
Lowest abstraction in nand to tetris - Takes two binary inputs and returns 1.

1 + 1 -> 0
1 + 0 -> 1
0 + 0 -> 1
0 + 1 -> 1

An abastraction is logical behaviour without explanation.
We express binary in 0,1 (rather than True False). 

And, Not, Or are the fundamental gates. You buy these and use a soldering gun to make nand, xor etc.


Added the letter l where python has a predefind word for the gate name.

"""

def land(a,b):
    if (a == b and a == 1): return 1
    return 0

def lnot(a):
    if (a == 0): return 1
    if (a == 1): return 0

def lor(a,b):
    if (a != b and a == 1): return 1
    if (a != b and b == 1): return 1
    return 0

def xor(a,b):
    return lor(land(a, lnot(b)),land(lnot(a), b))

def nand(a,b):
    if (a == 1 and b == 1): return 0
    return 1


if __name__ == "__main__":
    #Testing possibilities here
    cases = [[0,0],[0,1],[1,0],[1,1]]

    nand_answers = [1,1,1,0]    
    print("testing nand")
    for i, case in enumerate(cases):
        if(nand(case[0],case[1]) == nand_answers[i]): print(f"{case[0]},{case[1]} Passed")
        else: print(f"{case[0]},{case[1]} Failed, output {nand(case[0],case[1])}")

    xor_answers = [0,1,1,0]    
    print("testing xor")
    for i, case in enumerate(cases):
        if(xor(case[0],case[1]) == xor_answers[i]): print(f"{case[0]},{case[1]} Passed")
        else: print(f"{case[0]},{case[1]} Failed")

    