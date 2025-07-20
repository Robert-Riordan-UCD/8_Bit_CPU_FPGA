from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem
from .control_signals import Signal

class TestAllSeq(uvm_sequence):
    async def body(self):
        # all_ins = AllInstructions("all instructions")
        reset = Reset("rst")
        load_a = LoadA("load A")
        store_a = StoreA("store A")
        add = Add("add")
        sub = Sub("sub")
        # random = Random("random")

        # await all_ins.start(self.sequencer)
        await reset.start(self.sequencer)
        await load_a.start(self.sequencer)
        await store_a.start(self.sequencer)
        await add.start(self.sequencer)
        await sub.start(self.sequencer)
        # await random.start(self.sequencer)

class Reset(uvm_sequence):
    async def body(self):
        rst = SeqItem(name="rst", rst=1)
        await self.start_item(rst)
        await self.finish_item(rst)

class LoadA(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="load A step 0", instruction=0b0001, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="load A step 1", instruction=0b0001, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
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
        seqs = [
            SeqItem(name="store A step 0", instruction=0b0100, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="store A step 1", instruction=0b0100, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
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
        seqs = [
            SeqItem(name="add step 0", instruction=0b0010, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="add step 1", instruction=0b0010, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
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
        seqs = [
            SeqItem(name="sub step 0", instruction=0b0011, expected_output=[Signal.PC_OUT, Signal.MAR_RD]),
            SeqItem(name="sub step 1", instruction=0b0011, expected_output=[Signal.RAM_WRT, Signal.I_RD, Signal.PC_INC]),
            SeqItem(name="sub step 2", instruction=0b0011, expected_output=[Signal.I_WRT, Signal.MAR_RD]),
            SeqItem(name="sub step 3", instruction=0b0011, expected_output=[Signal.RAM_WRT, Signal.B_RD]),
            SeqItem(name="sub step 4", instruction=0b0011, expected_output=[Signal.ALU_OUT, Signal.ALU_FLG, Signal.ALU_SUB, Signal.A_RD]),
            SeqItem(name="sub step 5", instruction=0b0011),
            SeqItem(name="sub step 6", instruction=0b0011),
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
