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

"""

from gates import andnand, ornand, notnand, xornand, muxnand, check_16bit

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
    if check_16bit(a) and check_16bit(b):
        out = []
        overflow = 0
        for bi, ai in zip(reversed(a), reversed(b):
            overflow, bit = fulladder(overflow, ai, bi)
            out.append(bit)
    return reversed(out)

def incrementor(a):
    """
    Adds 1 to a given numbers. Ignores the overflow bit.
    """
    return adder(1,a)

def hack(zx, nx, zy, ny, f, no, x, y):
    """
    The ALU has 6 control bits as well as 2 numerical inputs (x,y).
    There is a main output and 2 specific flag output bits zr (if out = zero zr=1) and ng ( if out = negative, ng = 1) (else 0).

    zx => if zx = 1, set x = 0
    zy => if zy = 1, set y = 0
    nx => if nx = 1, x = bitwisenot(x) = !x  (in the book bitwise not is represented as !)
    ny => if ny = 1, y = !y    (NOTE: that this is a bitwise negation in the two's compliment).
    f => if f = 1, out = x+y, else and(x,y)
    no => if no = 1, out = !out.

    so possible function outputs are 0, 1, -1, x, y, !x, !y, -x, -y, x+1, y+1, x-1, y-1, x+y, x-y, y-x, x&y, x|y.
    """
    



if __name__ == "__main__":
    """
    testing is by no means exhaustive
    """
