"""
Nand is the lowest abstraction in nand to tetris - Takes two binary inputs and returns 1.

1 + 1 -> 0
1 + 0 -> 1
0 + 0 -> 1
0 + 1 -> 1

An abastraction is logical behaviour without explanation.
We express binary in 0,1 (rather than True False).

Nand are the fundamental gates. You buy these and use a soldering gun to make and, or, xor, multiplexers etc.


Added the letter l where python has a predefind word for the gate name.

My data is represented as an array of bits. 
"""

def check_bit(a):
    """
    Adding this to check my objects are bits
    """
    if isinstance(a, int):
        if (a == 1 or a == 0): return True
    return False

def check_16bit(a):
    check = False
    if len(a) == 16:
        check = True
        for j, i in enumerate(a):
            if check_bit(i):
                continue
            print(f"False bit on step {j}: ", i)
            check = False
    return check

def nand(a,b):
    if (a == 1 and b == 1): return 0
    return 1

def andnand(a,b):
    """
    and from nands
    """
    return nand(nand(a,b), nand(a,b))

def ornand(a,b):
    """
    or from nands
    """
    return nand(nand(a,a), nand(b,b))

def notnand(a):
    """
    not from nands
    """
    return nand(a,a)

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

def xornand(a,b):
    """
    not or, can also be written if a!=b return 1 else 0.
    """
    return ornand(andnand(a, notnand(b)),andnand(notnand(a), b))

def mux(a,b,sel):
    """
    Short for multiplexer.
    The 3rd bit, sel, selects the output from the inputs a and b.
    """
    if sel == 0: return a
    return b

def muxnand(a,b,sel):
    return ornand(andnand(a, notnand(sel)),andnand(b, sel))

def dmux(a,sel):
    """
    Demulitplexer. returns 2 bits a and 0. The order is determined by sel.
    """
    if sel == 0: return a, 0
    return 0, a



def multilnot(lin):
    """
    N bit implementation of not (lnot).
    we'll use N = 16 later but its flexible here.
    """
    out = lin
    for i, a in enumerate(lin):
        out[i] = lnot(lin[i])
    return out

def multiland(ina, inb):
    """
    N bit implementation of and (land).
    """
    assert len(ina) == len(inb)
    out = ina
    for i, lin in enumerate(zip(ina, inb)):
        out[i] = land(lin[0], lin[1])
    return out

def multilor(ina, inb):
    """
    N bit or (lor).
    """
    assert len(ina) == len(inb)
    out = ina
    for i, lin in enumerate(zip(ina, inb)):
        out[i] = lor(lin[0], lin[1])
    return out


def multimux(a,b,sel):
    """
    Same as mux but with defined 2nd value, 1 bit selector
    """
    if sel == 0: return a, b
    return b, a

def mwaylor(ina):
    """
    Multi-way Or gate
    outputs 1 when at least 1 of the inputs is 1, 0 otherwise.
    #hardware typically needs 1 8mwaylor variant. We can leave it undetermined in python.

    """
    for i in ina:
        if i == 1:
             return 1
    return 0


def mux4way16(a,b,c,d,sel):
    """
    4 16 bit, numbers selected by a 2 bit selector.
    00,01,10,11 = a,b,c,d
    """
    if (sel[0] == 0 and sel[1] == 0): return a
    if (sel[0] == 0 and sel[1] == 1): return b
    if (sel[0] == 1 and sel[1] == 0): return c
    if (sel[0] == 1 and sel[1] == 1): return d

def mux8way16(a,b,c,d,e,f,g,h,sel):
    """
    8 16 bit, numbers selected by a 3 bit selector.
    000,001,010= a,b,c,d
    4 2bit selectors.
    """
    x = [a,b,c,d,e,f,g,h]
    return x[sel[0]*4+sel[1]*2+sel[2]]


def dmux4way(lin, sel):
    """
    2 bit selector can send input 1 of 4 ways.
    00,01,10,11 = a,b,c,d
    sel[0] x 2**0 + sel[1] x 2**1 = index, 0,1,2,3 = 00,01,10,11
    The number system right to left.
    """
    z = [0] * 4
    path = sel[0]*2 + sel[1]
    return [lin if i == path else z for i in range(4)]

def dmux8way(lin, sel):
    """
    3 bit selector. sent 1 of 8 ways.
    """
    z = [0] * 8
    path = sel[0]*4 + sel[1]*2 + sel[2]
    return [lin if i == path else z for i in range(8)]


if __name__ == "__main__":
    """
    testing is by no means exhaustive
    """

    m = [1,0,1,0,1,1,0,0,1,0,1,0,1,1,0,0] #random 16 bit array
    n = [1,0,1,0,1,1,0,0,1,0.0,1,0,1,1,0,0]
    print("checking 16 bit checker ")
    if (check_16bit(m) == True and check_16bit(n) == False): print("passed")
    else: print("Failed")

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

    print("testing xor nand")
    for i, case in enumerate(cases):
        if (xornand(case[0],case[1]) == xor_answers[i]): print(f"{case[0]},{case[1]} Passed")
        else: print(f"{case[0]},{case[1]} Failed, output {xornand(case[0],case[1])} should be {xor(case[0],case[1])}" )

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


    print("testing multi functions")

    if (multilnot(m) != [0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1]): print("multilnot failed")
    else: print("multilnot passed")

    if (multiland(m, m) != m): print("multiland failed")
    else: print("multiland passed")

    flipm = [1 - m[i] for i in m]
    if (multilor(m, m) == flipm): print("multilor failed")
    else: print("multilor passed")


    if multimux(m, flipm, 1) == m: print("multimux failed")
    if multimux(m, flipm, 1) == flipm: print("multimux passed")

    print("testing multiway functions")
    meight = [0,1,0,1,0,0,1,1]
    mone = [1,1,1,1,1,1,1,1]
    mz = [0,0,0,0,0,0,0,0]

    if (mwaylor(meight) == 1): print("mwaylor passed")
    else: print("mwaylor Failed")

    sel2 = [0,1]
    sel3 = [0,1,0]

    if (mux8way16(a,a,a,a,a,a,a,a,sel3) == a): print("mux8way16 passed")
    else: print("mux8way16 failed")

    if (dmux4way(a, sel2)[1] == a): print("dmux4way passed")
    else: print("dmux4wayfailed")

    if (dmux8way(a, sel3)[2] == a): print("dmux8way passed")
    else: print("dmux8way failed")
