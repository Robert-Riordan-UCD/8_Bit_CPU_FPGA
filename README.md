# 8 Bit FPGA CPU

This is an 8-bit CPU design running on a Tang Nano 9k FPGA. The CPU design is based on [Ben Eaters Breadboard CPU](https://eater.net/8bit), which is based on the [Simple As Possible Computer](https://en.wikipedia.org/wiki/Simple-As-Possible_computer).

The CPU is made of 11 modules, which are designed in SystemVerilog and verified using [pyuvm](https://github.com/pyuvm/pyuvm).

# Getting Started

This project is not fully complete yet and is currently only tested on my personal laptop and raspberry pi. However, this is the current process. (I am developing on Ubuntu 24 and used [this](https://www.geeklan.co.uk/?p=2919) guide to get up and running using an open source toolchain)

## Installation and Setup

The following programs are required:
1. ```yosys``` for synthisis.
2. ```nextpnr``` for place and route, and bitstream generation.
3. ```openFPGALoader``` for loading the bitstream.

```sudo apt insatll yosys nextpnr-gowin openfpgaloader```

Clone and navigate to the repository

```
git clone https://github.com/Robert-Riordan-UCD/8_Bit_CPU_FPGA
cd ./8_Bit_CPU_FPGA/
```

## Running

```make all upload```

## Testing

```pyuvm``` is required for testing.

```sudo apt install pyuvm```

To test each module navigate to the verif directory for that module and run make.

```
cd ./verif/<module>/
make
```

# Current Design Status

| Module                  | RTL | Verified | Runs on FPGA |
| :---------------------- | :-: | :-: | :-: |
| Clock                   |✅|✅|✅|
| Program Counter         |✅|✅|✅|
| A register              |✅|✅|✅|
| B Register              |✅|✅|✅|
| Memory Address Register |✅|✅|✅|
| Instruction Register    |✅|✅|✅|
| Random Access Memory    |✅|✅|✅|
| Arithmetic Logic Unit   |✅|✅|✅|
| Control                 |✅|✅|✅|
| Output                  |✅|〰️|✅|
| Bus                     |✅|✅|✅|
||||
| Top                     |✅|❌|✅|

I had to redesign the bus to avoid tristate logic, so all modules that write to the bus need to be re-verified. But it's working on the FPGA right now!

The output is currently in hexadecimal, because there was not enough LUTs on the Tang Nano 9k to implement a naive approach to decimal conversion using division. I will hopefully update this to a better approach soon.
