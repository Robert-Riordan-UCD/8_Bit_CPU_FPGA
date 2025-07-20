from enum import Enum

class Signal(Enum):
    CLK_HLT=0
    PC_OUT=1
    PC_INC=2
    PC_JMP=3
    A_RD=4
    A_WRT=5
    B_RD=6
    B_WRT=7
    I_RD=8
    I_WRT=9
    MAR_RD=10
    RAM_RD=11
    RAM_WRT=12
    ALU_OUT=13
    ALU_SUB=14
    ALU_FLG=15
    OUT_EN=16
