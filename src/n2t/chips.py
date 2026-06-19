"""
Arithmetic logic unit. ALU is made from logic gates (gates.py) and is the key component in the central processing unit (cpu).
The ALU designed here is called HACK and is specific to the Nand2tetris programme.

This a user descretion desition on how to arrange the nand gates which are universal. Hack can only do integer arithmetic to keep it simple.


Adder chips combine bits. Once binary addition is defined all other mathematical functions can be dereived form it.

The two's compliment method represents negative numbers with binary as 2^n - x = -x in an n-bit binary system.
i.e. n = 4, left-most bit is a sign bit and then n<=3 are numbers up to 8 so we can write -8 to +7.

Subtraction is therefore (x - y = x + (-y) ) - Overflow bit is ignored (convention, fine if it is agreed to be the sign throughout).
i.e. -1 = 1111, = 16-1 => 7 - 1 = 0111 + 1111 = 0110 = 6

Mutliplcation is repeated addition.

Division with remainder is a combination of addition, comparison and then subtraction.

(Fractional division requires floating point arithmetic i.e. a more complex and expensive ALU)

"""

from gates import andnand, ornand

def halfadder(a,b):
    """
    adds 2 bit binary numbers
    outputs 2 bits => return carry, sum.
    00 01 10 11 => 00 01 01 10

    carry = and gate produces 00 01 10 11 => 0 0 0 1
    sum = or gate produces 00 01 10 11 => 0 1 1 0
    """
    return andnand(a,b), ornand(a,b)

def fulladder(a,b,c):
    """
    adds 3 bit binary numbers
    if a = 0, behaviour is halfadder b,c
    """


def adder():
    """
    can add 2 n-bit numebers (we'll use 16 bit)
    """

def incrementor():
    """
    Adds 1 to a given numbers. Ignores the overflow bit.
    """


if __name__ == "__main__":
    """
    testing is by no means exhaustive
    """
