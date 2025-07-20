from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem
from .control_signals import Signal

class TestAllSeq(uvm_sequence):
    async def body(self):
        reset = Reset("rst")

        load_a = LoadA("load A")
        store_a = StoreA("store A")
        add = Add("add")
        sub = Sub("sub")
        load_im = LoadIm("load imediate")
        jump = Jump("jump")
        jump_carry_not_set = JumpCarryWithoutCarry("jump carry not set")
        jump_carry_set = JumpCarryWithCarry("jump carry set")
        jump_zero_not_set = JumpZeroWithoutZero("jump zero not set")
        jump_zero_set = JumpZeroWithZero("jump zero set")
        out = Out("out")
        halt = Halt("halt")
        # random = Random("random")

        await reset.start(self.sequencer)
        await load_a.start(self.sequencer)
        await store_a.start(self.sequencer)
        await add.start(self.sequencer)
        await sub.start(self.sequencer)
        await load_im.start(self.sequencer)
        await jump.start(self.sequencer)
        await jump_carry_not_set.start(self.sequencer)
        await jump_carry_set.start(self.sequencer)
        await jump_zero_not_set.start(self.sequencer)
        await jump_zero_set.start(self.sequencer)
        await out.start(self.sequencer)
        await halt.start(self.sequencer)
        # await random.start(self.sequencer)

class Reset(uvm_sequence):
    async def body(self):
        rst = SeqItem(name="rst", rst=1)
        await self.start_item(rst)
        await self.finish_item(rst)

class LoadA(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="load A step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="load A step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="load A step 2", instruction=0b0001, expected_output=[Signal.I_WRT, Signal.MAR_RD]),
            SeqItem(name="load A step 3", instruction=0b0001, expected_output=[Signal.RAM_WRT, Signal.A_RD]),
            SeqItem(name="load A step 4", instruction=0b0001),
            SeqItem(name="load A step 5", instruction=0b0001),
            SeqItem(name="load A step 6", instruction=0b0001),  
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class StoreA(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="store A step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="store A step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="store A step 2", instruction=0b0100, expected_output=[Signal.I_WRT, Signal.MAR_RD]),
            SeqItem(name="store A step 3", instruction=0b0100, expected_output=[Signal.A_WRT, Signal.RAM_RD]),
            SeqItem(name="store A step 4", instruction=0b0100),
            SeqItem(name="store A step 5", instruction=0b0100),
            SeqItem(name="store A step 6", instruction=0b0100),  
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Add(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="add step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="add step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="add step 2", instruction=0b0010, expected_output=[Signal.I_WRT, Signal.MAR_RD]),
            SeqItem(name="add step 3", instruction=0b0010, expected_output=[Signal.RAM_WRT, Signal.B_RD]),
            SeqItem(name="add step 4", instruction=0b0010, expected_output=[Signal.ALU_OUT, Signal.ALU_FLG, Signal.A_RD]),
            SeqItem(name="add step 5", instruction=0b0010),
            SeqItem(name="add step 6", instruction=0b0010),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Sub(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="sub step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="sub step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="sub step 2", instruction=0b0011, expected_output=[Signal.I_WRT, Signal.MAR_RD]),
            SeqItem(name="sub step 3", instruction=0b0011, expected_output=[Signal.RAM_WRT, Signal.B_RD]),
            SeqItem(name="sub step 4", instruction=0b0011, expected_output=[Signal.ALU_OUT, Signal.ALU_FLG, Signal.ALU_SUB, Signal.A_RD]),
            SeqItem(name="sub step 5", instruction=0b0011),
            SeqItem(name="sub step 6", instruction=0b0011),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class LoadIm(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="load imediate step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="load imediate step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="load imediate step 2", instruction=0b0101, expected_output=[Signal.I_WRT, Signal.A_RD]),
            SeqItem(name="load imediate step 3", instruction=0b0101),
            SeqItem(name="load imediate step 4", instruction=0b0101),
            SeqItem(name="load imediate step 5", instruction=0b0101),
            SeqItem(name="load imediate step 6", instruction=0b0101),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Jump(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="jump step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="jump step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="jump step 2", instruction=0b0110, expected_output=[Signal.I_WRT, Signal.PC_JMP]),
            SeqItem(name="jump step 3", instruction=0b0110),
            SeqItem(name="jump step 4", instruction=0b0110),
            SeqItem(name="jump step 5", instruction=0b0110),
            SeqItem(name="jump step 6", instruction=0b0110),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class JumpCarryWithoutCarry(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="jump carry (carry not set) step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="jump carry (carry not set) step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="jump carry (carry not set) step 2", instruction=0b0111),
            SeqItem(name="jump carry (carry not set) step 3", instruction=0b0111),
            SeqItem(name="jump carry (carry not set) step 4", instruction=0b0111),
            SeqItem(name="jump carry (carry not set) step 5", instruction=0b0111),
            SeqItem(name="jump carry (carry not set) step 6", instruction=0b0111),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class JumpCarryWithCarry(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="jump carry (carry set) step 0", alu_carry=1, instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="jump carry (carry set) step 1", alu_carry=1, instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="jump carry (carry set) step 2", alu_carry=1, instruction=0b0111, expected_output=[Signal.I_WRT, Signal.PC_JMP]),
            SeqItem(name="jump carry (carry set) step 3", alu_carry=1, instruction=0b0111),
            SeqItem(name="jump carry (carry set) step 4", alu_carry=1, instruction=0b0111),
            SeqItem(name="jump carry (carry set) step 5", alu_carry=1, instruction=0b0111),
            SeqItem(name="jump carry (carry set) step 6", alu_carry=1, instruction=0b0111),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class JumpZeroWithoutZero(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="jump zero (zero not set) step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="jump zero (zero not set) step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="jump zero (zero not set) step 2", instruction=0b1000),
            SeqItem(name="jump zero (zero not set) step 3", instruction=0b1000),
            SeqItem(name="jump zero (zero not set) step 4", instruction=0b1000),
            SeqItem(name="jump zero (zero not set) step 5", instruction=0b1000),
            SeqItem(name="jump zero (zero not set) step 6", instruction=0b1000),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class JumpZeroWithZero(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="jump zero (zero set) step 0", alu_zero=1, instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="jump zero (zero set) step 1", alu_zero=1, instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="jump zero (zero set) step 2", alu_zero=1, instruction=0b1000, expected_output=[Signal.I_WRT, Signal.PC_JMP]),
            SeqItem(name="jump zero (zero set) step 3", alu_zero=1, instruction=0b1000),
            SeqItem(name="jump zero (zero set) step 4", alu_zero=1, instruction=0b1000),
            SeqItem(name="jump zero (zero set) step 5", alu_zero=1, instruction=0b1000),
            SeqItem(name="jump zero (zero set) step 6", alu_zero=1, instruction=0b1000),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Out(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="out step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="out step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="out step 2", instruction=0b1110, expected_output=[Signal.A_WRT, Signal.OUT_EN]),
            SeqItem(name="out step 3", instruction=0b1110),
            SeqItem(name="out step 4", instruction=0b1110),
            SeqItem(name="out step 5", instruction=0b1110),
            SeqItem(name="out step 6", instruction=0b1110),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Halt(uvm_sequence):
    async def body(self):
        prev_ins = randint(0, 0xF)
        seqs = [
            SeqItem(name="halt step 0", instruction=prev_ins, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="halt step 1", instruction=prev_ins, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="halt step 2", instruction=0b1111, expected_output=[Signal.CLK_HLT]),
            SeqItem(name="halt step 3", instruction=0b1111),
            SeqItem(name="halt step 4", instruction=0b1111),
            SeqItem(name="halt step 5", instruction=0b1111),
            SeqItem(name="halt step 6", instruction=0b1111),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)


class AllInstructions(uvm_sequence):
    async def body(self):
        # seqs = [SeqItem(instruction=i) for i in range(0xF)]
        for instruction in range(0x10):
            rst = SeqItem(name="rst", rst=1)
            await self.start_item(rst)
            await self.finish_item(rst)
            for step in range(7):
                seq = SeqItem(name=f"step {step}", instruction=instruction)
                await self.start_item(seq)
                await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(200)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.instruction = randint(0, 0xF)
            op.alu_carry = randint(0, 1)
            op.alu_zero = randint(0, 1)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
