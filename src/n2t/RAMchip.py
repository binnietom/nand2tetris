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

In a real CPU the clock isn't build from nands. Current is measured from a quartz crystalline clock or modern ones use a small cpu chip.
"""

from gates import notnand, muxnand, check_16bit, mux8way16
import time, threading

class clock:
    """
    Clock as a custom iterator object.
    """
    def __init__(self, t=0):
        self.t = t
        self.run = False
        self._thread = None
        self.cycle = 1

    def tick(self):
        """
        Call it to progress the cycle.
        """
        self.t += 1

    def label(self):
        """
        Call to label bits.
        """
        return self.t

    def update_cycle(self, cycle = 10**6):
        """
        default cycle is 1s, update it to microsecond value here.
        """
        self.cycle = cycle/10**6

    def auto_iter(self):
        """
        run the clock automatically, for t micro-seconds (default 1s).
        """
        while self.run:
            time.sleep(self.cycle)
            self.t += 1

    def start(self):
        """
        Start running the clock automatically in the background
        """
        if self.run:
            return

        self.run = True
        self._thread = threading.Thread(
            target=self.auto_iter,
            daemon=True
        )
        self._thread.start()

    def stop(self):
        """
        stops auto_iter
        """
        self.run = False

def bit_time(a):
    """
    converts a bit or bit array to object + timestamp
    """
    t = cpu_clock.label()
    c = [a,t]
    return c

def dff(a):
    """
    Data Flip Flop
    In bit a(t) = out(t+1)
    c is [a, t] like in bit_time.
    """
    c = bit_time(a)
    c[1] += 1
    return c

def reg(input, load=0):
    """
    Single bit register, based on DFFs.
    In state is the out state unless there is an input load.
    """
    return muxnand(input, notnand(input), load)

def reg16(input, load=0):
    """
    multi bit register, based on reg(). 16  bit, is organised in arrays so its the same here(?).
    """
    if check_16bit(input) == True:
        return reg(input, load)

def RAM(input, address, current=None,  size = 16):
    """
    Based on registers. We have (size =) 16 registers.
    Address assigns which register to input information to.

    If the architecture is known (like in hardware) you can construct the address IDs using a combination of eg. mux8way16 and mux4way16.
    """
    if current == None:
        storage = size*[[]]
    assert len(current) == size
    storage[address] = input
    return storage

def counter():
    """
    Based on registers.
    """

def running_RAM():
    """
    I need to update everything inbetween each clock cycle. (which can now run in the background.
    """

cpu_clock = clock()
cpu_clock.start()

if __name__ == "__main__":
    print("starting RAM tests")
