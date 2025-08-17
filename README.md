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
