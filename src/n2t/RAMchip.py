"""
The ALU chip processes are time independent.
Here we introduce time dependency. Memory is the the ability to use info from past time steps (previous).
Time independency is defined by being within 1 time step (current).

A time step is defined by one cycle of the Clock.
The Clock outputs binary signals called tick & tock that alternate (beginning of tick to end of tock .._|^_|^_|^..) for every 1 clock cycle.
Modern CPUs can do billions of cycles per s.

Flip-flop is the fundamental time dependent logic gate that all memory devices are constructed form.
Its key property is stability accross many time-steps.
Data flip flop (DFF) is the building block of the register which is the building block of RAM.

Within a cycle, nothing changes. Changes only occur between cycles.
Clock length must be longer than current flow changes in the circuits.

We must build functions that can handle time states as booleans.
#its not actually time its iterations of the cycle.
"""

from gates import notnand, muxnand

class clock:
    """
    Clock as a custom iterator object.
    """
    def __init__(self, t=0):
        self.t = 0
    def iter(self):
        """
        Call it to progress the cycle.
        """
        self.t += 1
        return self.t
    def label(self):
        """
        Call to label bits.
        """
        return self.t

cpu_clock = clock()

def bit_time(a):
    """
    converts a bit or bit array to object + timestamp
    """
    t = cpu_clock.label()
    c = [a,t]
    return c

def dff(c):
    """
    Data Flip Flop
    In bit a(t) = out(t+1)
    c is [a, t] like in bit_time.
    """
    #cpu_clock.iter()
    #c[1] = cpu_clock.label()  ####will this iterate the clock every dff call? maybe...
    return [c[0], c[1]+1]

def reg(in, load=0):
    """
    Single bit register, based on DFFs.
    In state is the out state unless there is an input load.
    """
    return muxnand(in, notnand(in), load)

def reg16():
    """
    multi bit register, based on reg().
    """



def RAM():
    """
    Based on registers.
    """

def counter():
    """
    Based on registers.
    """

def address():
    """
    ?
    """
