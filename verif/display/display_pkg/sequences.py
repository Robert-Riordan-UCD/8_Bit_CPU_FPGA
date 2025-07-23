from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        ops = AllOperations("all operations")
        random = Random("random")

        await ops.start(self.sequencer)
        await random.start(self.sequencer)

"""
    All combinations of rst, read, write
"""
class AllOperations(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="rst", rst=1),
            SeqItem(name="enable", bus=0xAB, enable=1),
            SeqItem(name="enable and rst", rst=1, bus=0xCD, enable=1),
            SeqItem(name="noop"),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(5000)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.enable = randint(0, 1)
            op.bus = randint(0, 0xFF)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
