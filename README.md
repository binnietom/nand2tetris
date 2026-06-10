# nand2tetris

Simulated computer from first principles all in python. Based on "Elements of Computing Systems" Nisan and Schocken.

Architecture is split into 2 layers:

  hardware (Logic gates -> ALU, RAM chips -> CPU)  
and
  software (Machine language -> VM Code -> high-level language)

Each level is planned to be an abstraction that relies on parts/objects from the last section.

## Hardware

### Chapter 1 - Boolean Logic
