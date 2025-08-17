from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        ops = AllOperations("all operations")
        edge = EdgeCases("edge cases")
        random = Random("random")

        await ops.start(self.sequencer)
        await edge.start(self.sequencer)
        await random.start(self.sequencer)

"""
    All combinations of rst, read, write
"""
class AllOperations(uvm_sequence):
    async def body(self):
        seqs = [
            # Valid operations
            SeqItem(name="rst", rst=1),
            SeqItem(name="inc", inc=1),
            SeqItem(name="out", out=1),
            SeqItem(name="jump", bus=0xAB, jump=1),
            SeqItem(name="noop"),
            
            # Invalid operations
            SeqItem(name="inc and jump", inc=1, jump=1, bus=0x12),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)


"""
    Cases with 0 or 0xFF
"""
class EdgeCases(uvm_sequence):
    async def body(self):
        seqs = [
            # INC overflow
            SeqItem(name="jump to 0x0F", bus=0x0F, jump=1),
            SeqItem(name="inc to 0", inc=1),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(20000)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.inc = randint(0, 1)
            op.jump = randint(0, 1)
            op.bus = randint(0, 0xFF)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
