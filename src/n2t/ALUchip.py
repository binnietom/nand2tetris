"""
Arithmetic logic unit. ALU is made from logic gates (gates.py) and is the key component in the central processing unit (cpu).
The ALU designed here is called HACK and is specific to the Nand2tetris programme.

This a user descretion desition on how to arrange the nand gates which are universal. Hack can only do integer arithmetic to keep it simple.


Adder chips combine bits. Once binary addition is defined all other mathematical functions can be dereived form it.

The two's compliment method represents negative numbers with binary as 2^n - x = -x in an n-bit binary system.
i.e. n = 4, left-most bit is a sign bit and then n<=3 are numbers up to 8 so we can write -8 to +7.

Subtraction is therefore (x - y = x + (-y) ) - Overflow bit is ignored (convention, fine if it is agreed to be the sign throughout).
i.e. -1 = 1111, = 16-1 => 7 - 1 = 0111 + 1111 = 0110 = 6

Mutliplcation is repeated addition. Division with remainder is a combination of addition, comparison and then subtraction.
(Fractional division requires floating point arithmetic i.e. a more complex and expensive ALU)
These & more complex functions will be handled at the OS level.

Note that each operation doesn't overwrite, these are signal flows. they therefore all exist simultaneously. Operationsa are all assumed to be well within 1 clock cycle.

MSB & LSB are most & least significant bit respectively.
MSB is leftmost, out[15] *python array element [0]. this is the sign bit.
LSB is rightmost (2^0 = 1 digit)

A bug i ran into was Ripple-carry order. The adder calculation must be LSB to MSB. (hence the x[::-1] reversing slice notation in the adder function.
"""

from gates import andnand, ornand, notnand, xornand, muxnand, check_16bit, multimux

def inttobit(x, n=16):
    """
    integer value to binary python array of length 16
    """
    #twoscomp part
    if x < 0:
        x += 2**n
    #shift x by i bits (>>), bitwise and (&) with 1,
    return [(x >> i) & 1 for i in range(n-1, -1, -1)]

def bittoint(b):
    """
    takes python array and produces integer value
    """
    x = 0
    n = len(b)
    for pow, on  in enumerate(b):
        x += on*2**(n-pow-1)
    return x

def twoscomp(b):
    """
    bit to int including negatives with the twos comp method
    """
    n = len(b)
    x = -b[0] * 2**(n-1)
    for i in range(1, n):
        x += b[i] * 2**(n-i-1)
    return x

def halfadder(a,b):
    """
    adds 2 bit binary numbers
    outputs 2 bits => return carry, sum.
    00 01 10 11 => 00 01 01 10

    carry = and gate produces 00 01 10 11 => 0 0 0 1
    sum = or gate produces 00 01 10 11 => 0 1 1 0
    """
    return andnand(a,b), xornand(a,b)

def fulladder(a,b,c):
    """
    adds 3 bit binary numbers
    i.e. 000 001 010 011 => 00 10 10 01
         100 101 110 111 => 01 10 10 11

    halfadder (b,c)      00 01 10 11 => 00 01 01 10  x2
    halfadder2 01100110 and 00001111 => 00 01 01 00 01 10 10 01
    (sum2 = 01101001)
    or(carry1, carry2) = or(00010001, 00000110) = 00010111)
    """
    carry1, sum1 = halfadder(b,c)
    carry2, sum2 = halfadder(sum1, a)
    return ornand(carry1, carry2), sum2

def adder(a,b):
    """
    can add 2 n-bit numebers (we'll use 16 bit)
    (referred to as add16 in the book in some places).

    uses the fulladder becuase 3 bits are required (2 that are being added and the carry from the last column).
    going bitwise is sufficiently fast to be completed 16 times in 1 clock cycle.
    """
    #if check_16bit(a) and check_16bit(b):
    out = []
    carry = 0

    for ai, bi in zip(a[::-1],b[::-1]):
        carry, sum = fulladder(ai, bi, carry)
        out.append(sum)
    return out[::-1]

def incrementor(a):
    """
    Adds 1 to a given numbers. Ignores the overflow bit.
    """
    return adder(1,a)

def hack_singlebit(zx, nx, zy, ny, f, no, x, y):
    """
    basic architecture for 1 bit x,y
    """
    #zx, zy use the mux selecting 0 or input
    x1 = muxnand(x, 0, zx)
    y1 = muxnand(y, 0, zy)

    #nx, ny is also mux selecting
    x2 = muxnand(x1, notnand(x1), nx)
    y2 = muxnand(y1, notnand(y1), ny)

    #Mux selects use of adder or and.
    fout = muxnand(adder(x2,y2), andnand(x2,y2), f)

    #mux selects not previous depending on no..
    out = muxnand(fout, notnand(fout), no)

    #setting flag-bits - doesn't really make sense in 1bit..
    #zr = notnand(ornand(out[:]))   or ( ) = 0 and or so 0 if all zero, 1 if any 1s,  then not this = zr.
    #ng = out[0] #twos compliment
    return out

def selfor(x):
    """
    checks a 16 bit number, and or any bits.
    """
    for i in x:
        if i == 1: return 1
    return 0

def hack(zx, nx, zy, ny, f, no, x, y):
    """
    The ALU has 6 control bits as well as 2 numerical inputs (x,y) both 16 bit inputs.
    There is a main output and 2 specific flag output bits zr (if out = zero zr=1) and ng ( if out = negative, ng = 1) (else 0).

    zx => if zx = 1, set x = 0
    zy => if zy = 1, set y = 0
    nx => if nx = 1, x = bitwisenot(x) = !x  (in the book bitwise not is represented as !)
    ny => if ny = 1, y = !y    (NOTE: that this is a bitwise negation in the two's compliment).
    f => if f = 1, out = x+y, else and(x,y)
    no => if no = 1, out = !out.

    so possible function outputs are:
    0,      101010
    1,      111111
    -1,     111010
    x,      001100
    y,      110000
    !x,     001101
    !y,     110001
    -x,     001111
    -y,     110011
    x+1,    011111
    y+1,    110111
    x-1,    001110
    y-1,    110010
    x+y,    000010
    x-y,    010011
    y-x,    000111
    x&y,    000000
    x|y,    010101
    wrt to the order of the input bits.

    Using multimux.
    """
    #print(f" x = {x} , y = {y}")
    if check_16bit(x) and check_16bit(y):
        zeros = [0]*len(x)
        #print(f" zeros = {zeros}")
        #zx, zy use the mux selecting [0]*16 or input x or y
        x1 = multimux(x, zeros, zx)[0]
        y1 = multimux(y, zeros, zy)[0]
        #print(f" x1 = {x1} , y1 = {y1}")

        negx = [notnand(i) for i in x1]
        negy = [notnand(i) for i in y1]
        #print(f" negx = {negx} , negy = {negy}")
        #nx, ny is also mux selecting
        x2 = multimux(x1, negx, nx)[0]
        y2 = multimux(y1, negy, ny)[0]
        #print(f" x2 = {x2} , y2 = {y2}")

        andxy = [andnand(xi, yi) for (xi, yi) in zip(x2, y2)]
        addxy = adder(x2,y2)
        #print(f" andxy = {andxy} , addxy = {addxy}")

        #Mux selects use of adder or and.
        fout = multimux(andxy, addxy, f)[0]
        notfout = [notnand(fi) for fi in fout]
        #print(f" fout = {fout}, notfout = {fout}")
        #mux selects not previous depending on no..
        out = multimux(fout, notfout, no)[0]
        #print("out = ",  out)

        #setting flag-bits
        zr = notnand(selfor(out))
        ng = out[0] #twos compliment
        #print("zr", zr)
        #print("ng", ng)
    return out, zr, ng



if __name__ == "__main__":
    """
    testing is by no means exhaustive
    """

    print("checking adder")
    a = 23
    b = 59
    check = a + b
    abin = inttobit(a)
    bbin = inttobit(b)
    ansbin = adder(abin, bbin)
    ans = twoscomp(ansbin)
    if ans == check: print("passed.")
    else: print(f"adder Failed, trying {a}+{b} = {check} \n in binary thats {abin} + {bbin} \n = {ansbin} \n coverted back to {ans}")



    print("checking ALU")
     #zx, nx, zy, ny, f, no , x, y
    input_array = [[1,0,1,0,1,0,2,3],
              [1,1,1,1,1,1,2,3],
              [1,1,1,0,1,0,2,3],
              [0,0,1,1,0,0,2,3],
              [1,1,0,0,0,0,2,3],
              [0,0,1,1,0,1,2,3],
              [1,1,0,0,0,1,2,3],
              [0,0,1,1,1,1,2,3],
              [1,1,0,0,1,1,2,3],
              [0,1,1,1,1,1,2,3],
              [1,1,0,1,1,1,2,3],
              [0,0,1,1,1,0,2,3],
              [1,1,0,0,1,0,2,3],
              [0,0,0,0,1,0,2,3],
              [0,1,0,0,1,1,2,3],
              [0,0,0,1,1,1,2,3],
              [0,0,0,0,0,0,2,3],
              [0,1,0,1,0,1,2,3]]

    expected = [
                [ 0, 1, 0],
                [ 1, 0, 0],
                [-1, 0, 1],
                [ 2, 0, 0],
                [ 3, 0, 0],
                [-3, 0, 1],
                [-4, 0, 1],
                [-2, 0, 1],
                [-3, 0, 1],
                [ 3, 0, 0],
                [ 4, 0, 0],
                [ 1, 0, 0],
                [ 2, 0, 0],
                [ 5, 0, 0],
                [-1, 0, 1],
                [ 1, 0, 0],
                [ 2, 0, 0],
                [ 3, 0, 0]
                ]


    for i, inputs in enumerate(input_array):
        #note that 2, 3 in binary is an array [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
        out, zr, ng = hack(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1])

        if ( [twoscomp(out), zr, ng] == expected[i]):
            print("ALU Passed!")
        else:
            print(f"\n ALU Failed with values: {inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7]} ")
            print(f"Got {[twoscomp(out), zr, ng]}, expected {expected[i]} \n")
