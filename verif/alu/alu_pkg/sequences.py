from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        random = Random("random")
        await random.start(self.sequencer)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(1000)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.a = randint(0, 0xFF)
            op.b = randint(0, 0xFF)
            op.subtract = randint(0, 1)
            op.out = randint(0, 1)
            op.flags_in = randint(0, 1)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)

# class CarryFlag(uvm_sequence): pass
# class ZeroFlag: pass
# class Output: pass
# class EdgeCases: pass
