from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        no_driver = NoDriver("no driver")
        random = Random("random")

        await no_driver.start(self.sequencer)
        await random.start(self.sequencer)

"""
    All combinations of rst, read, write
"""
class NoDriver(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="no driver"),
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
            SeqItem(name="read 0", bus_driver=0, read_from_bus=1),
            SeqItem(name="write 0", write_to_bus=1),
            SeqItem(name="read 0xFF", bus_driver=0xFF, read_from_bus=1),
            SeqItem(name="write 0xFF", write_to_bus=1),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(20000)]
        for op in ops:
            op.select = 2**randint(0, op.LANES-1)
            op.data = randint(0, 2**(op.LANES*op.WIDTH)-1)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
