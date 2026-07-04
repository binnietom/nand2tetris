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
"""

import time

def bit_time(a):
    """
    converts a bit or bit array to object + timestamp
    """
    t = 0 #probably needs to read a value to assign?
    return [a,t]


def clock_wait(t):
    """
    Clock built with a variable wait between tocks and ticks.
    """
    t = t/10**6 #t in micro s

    time.sleep(t)


def clock_iter():
    """
    Clock as an iterator object.
    Call it to change from tock to tick.
    """

def dff(a):
    """
    Data Flip Flop
    In bit a(t) = out(t+1)
    """

def address():

def register():

def RAM():

def counter():
