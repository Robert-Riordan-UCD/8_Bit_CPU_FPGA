from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        carry = CarryFlag("carry flag")
        zero = ZeroFlag("zero flag")
        edga = EdgeCases("edge cases")
        random = Random("random")

        await carry.start(self.sequencer)
        await zero.start(self.sequencer)
        await edga.start(self.sequencer)
        await random.start(self.sequencer)

"""
    Force a carry to occur
"""
class CarryFlag(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="carry with flag", a=0xFF, b=0x01, flags_in=1),
            SeqItem(name="carry without flag", a=0xFF, b=0x01),
            SeqItem(name="carry and subtract with flag", a=0x00, b=0x01, flags_in=1, subtract=1),
            SeqItem(name="carry and subtract without flag", a=0x00, b=0x01, subtract=1),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)
            rst = SeqItem(rst=1)
            await self.start_item(rst)
            await self.finish_item(rst)

"""
    Force a zero to occur
"""
class ZeroFlag(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="zero with flag", a=0xFF, b=0x01, flags_in=1),
            SeqItem(name="zero without flag", a=0xFF, b=0x01),
            SeqItem(name="zero and subtract with flag", a=0x01, b=0x01, flags_in=1, subtract=1),
            SeqItem(name="zero and subtract without flag", a=0x01, b=0x01, subtract=1),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)
            rst = SeqItem(rst=1)
            await self.start_item(rst)
            await self.finish_item(rst)

"""
    Cases with A, B, or BUS at 0 or 0xFF
"""
class EdgeCases(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="a=0 b=0", a=0, b=0, flags_in=1),
            SeqItem(name="a=0xFF b=0", a=0xFF, b=0, flags_in=1),
            SeqItem(name="a=0 b=0xFF", a=0, b=0xFF, flags_in=1),
            SeqItem(name="a=0xFF b=0xFF", a=0xFF, b=0xFF, flags_in=1),
            
            SeqItem(name="subtract a=0 b=0", a=0, b=0, flags_in=1, subtract=1),
            SeqItem(name="subtract a=0xFF b=0", a=0xFF, b=0, flags_in=1, subtract=1),
            SeqItem(name="subtract a=0 b=0xFF", a=0, b=0xFF, flags_in=1, subtract=1),
            SeqItem(name="subtract a=0xFF b=0xFF", a=0xFF, b=0xFF, flags_in=1, subtract=1),
            
            SeqItem(name="bus=0", a=0, b=0, flags_in=1),
            SeqItem(name="bus=0xFF", a=0xF0, b=0x0F, flags_in=1),
            
            SeqItem(name="subtract bus=0", a=1, b=1, flags_in=1, subtract=1),
            SeqItem(name="subtract bus=0xFF", a=0, b=1, flags_in=1, subtract=1),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(10000)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.a = randint(0, 0xFF)
            op.b = randint(0, 0xFF)
            op.subtract = randint(0, 1)
            op.flags_in = randint(0, 1)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
