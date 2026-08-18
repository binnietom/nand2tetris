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

My counter is built into the clock class.
DFF can be built with nands but it needs a clock and feedback. it is therefore better to treat it as its own abstraction as is done here.

The register and ALU combine into the CPU, which will be able to record in the RAM chip when controlled by the machine language (machlang.py).
"""

from gates import notnand, muxnand, check_16bit, mux8way16, multimux
import time, threading

from ALUchip import inttobit, twoscomp

class clock:
    """
    Clock as a custom iterator object. (referred to as c)
    """
    def __init__(self, t=0):
        self.t = t
        self.run = False
        self._thread = None
        self.cycle = 0.01

    def tick(self):
        """
        Call it to progress the cycle. (this is the same as PC increment)
        """
        self.t += 1

    def reset(self, v = 0):
        """
        t is actually the output of counter i.e. the the program counter PC chip.
        This function will reset the clock by default but can be used to set the clock to a specific value v.
        """
        self.t = v

    def label(self):
        """
        Call to label timestep (or counter increment).
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

c = clock()
#c.update_cycle(cycle=0.000001) #Easy to speed it up here.
c.start()


def check_clock(c=c):
    print("checking clock t_cycle=", c.label())

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

def auto_dff(a, c=c):
    """
    Data Flip Flop that runs with the auto clock.
    start the clock and input a. clock c. the Auto dff will return a on the next tick.
    """
    t = c.label()
    next = t + 1
    while t != next:
        t = c.label()
    return a

def reg(input, output=None, load=0):
    """
    Single bit register, based on Mux into a DFF.
    In state is the out state unless there is an input load.
    Pretending that input is the old input, output is the new input. i.e. 0 (stays) 1 updates to new).
    If there is no new input, the reg will repeat regular input.
    """
    if output == None:
        output = input
    return muxnand(input, output, load)

def reg16(input, output=None, load=0):
    """
    multi bit register, based on reg() but for 16  bit.
    You need previous/differing state - since these are functions I'll have to manually keep track of that in the RAM class.
    """
    if output == None:
        output = input
    if check_16bit(input) == True and check_16bit(output) == True:
        return multimux(input, output, load)[0]

def register(input, output=None, c=c, load=0):
    """
    full register with clock (c) linked dff.
    ~somewhat artificial as it won't remember.
    """
    return auto_dff(reg16(input, output, load),c)

class RAM:
    """
    current is a previous RAM state. (so RAM_update(current=RAM_previous) )
    Read and write are selected with load = 0 (read) load = 1 (write).

    Based on registers. We have (size =) 16 registers.
    Address assigns which register to input information to.

    If the architecture is known (like in hardware) you can construct the address IDs using a combination of eg. mux8way16 and mux4way16.
    This enables us to make RAM8 - an 8 register ram chip which can be grouped iteratively. i.e. 8*RAM8 = RAM64.. etc until 8*64=512, 8*512=4096, 8*4096=16384 etc.
    Modern computers don't construct RAM this way as its innefficient, but it is intuitive.
    We are just using an array so we are directly listing size=16384, so we have 16bit * 16384 storage which is 32kb.

    Read & write function with load:
    So the feedback loop is needed again for read and write so we just have it written here as the class.
    In a real chip the out state of the RAM (or counters within the RAM) feebacks into 1 MUX input, new state into the other.
    Therefore load being 1 or 0 selects whether the output of the MUX is the new or old value. (the DFF then delays 1 cycle) and the next iteration begins with new->old, newnew->new.
    """
    def __init__(self, size = 16384, c=c):
        self.size = size
        self.c = c
        self.storage = size*[[]]

    def read(self, address):
        """
        load = 0.
        Address <= size
        """
        return self.storage[address]

    def write(self, input, address):
        """
        load = 1.
        Address <= size
        """
        self.storage[address] = register(input)

if __name__ == "__main__":
    print("starting clock for RAM tests")

    check_clock(c=c)

    testint = 13
    testbit = inttobit(13)

    print(f"testing auto_dff with {testint}, as bit {testbit}")
    dffbit = auto_dff(testbit, c=c)
    if dffbit == testbit:
        print("DFF passed")
    else:
        print(f"DFF failed {twoscomp(dffbit)} != {testint}")

    print("testing reg")
    tests = [[0,0,0], [0,1,1], [1,0,0], [1,0,1]]
    results = [0,1,1,0]
    answers = []
    for t in tests:
        answers.append(reg(input = t[0], output = t[1], load = t[2]))
    if answers == results:
        print("reg passed")
    else:
        print(f"reg failed {answers} != {results}")

    print("testing reg16")
    a = testbit
    b = inttobit(15)
    tests = [[a,a,0], [a,b,1], [b,a,0], [b,a,1]]
    results = [a,b,b,a]
    answers = []
    for t in tests:
        answers.append(reg16(input = t[0], output = t[1], load = t[2]))
    if answers == results:
        print("reg16 passed")
    else:
        print(f"reg16 failed {answers} != {results}")
        for i in len(answers):
            print(f"{twoscomp(answers[i])} != {twoscomp(results[i])}")

    print("testing register")
    answers = []
    for t in tests:
        answers.append(register(input = t[0], output = t[1], load = t[2]))
    if answers == results:
        print("register passed")
    else:
        print(f"register failed {answers} != {results}")
        for i in len(answers):
            print(f"{twoscomp(answers[i])} != {twoscomp(results[i])}")

    #RAM inputs are in bits
    print("testing RAM")
    RAM = RAM()
    print("constructed RAM")

    address = 19
    print(f"saving {testint} to RAM address {address}, as bit {testbit}")

    RAM.write(input = testbit, address = address)

    readbit = RAM.read(address = address)
    print(readbit)

    if testint == twoscomp(readbit):
        print(f"Passed {testint} == {twoscomp(RAM.read(address = address))}")
        print("RAM successfully stored and recalled a bit value within a clock cycle.")
    else:
        print("RAM error")
