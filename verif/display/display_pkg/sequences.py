from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        # ops = AllOperations("all operations")
        # edge = EdgeCases("edge cases")
        random = Random("random")

        # await ops.start(self.sequencer)
        # await edge.start(self.sequencer)
        await random.start(self.sequencer)

"""
    All combinations of rst, read, write
"""
class AllOperations(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="read", bus_driver=0xAB, read_from_bus=1),
            SeqItem(name="write", write_to_bus=1),
            SeqItem(name="rst", rst=1),
            SeqItem(name="read & write", bus_driver=0xAB, read_from_bus=1, write_to_bus=1),
            SeqItem(name="read & rst", bus_driver=0xAB, read_from_bus=1, rst=1),
            SeqItem(name="write & rst", write_to_bus=1, rst=1),
            SeqItem(name="read & write & rst", bus_driver=0xAB, read_from_bus=1, write_to_bus=1, rst=1),
            SeqItem(name="noop"),
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
        rst = SeqItem(rst=1)
        await self.start_item(rst)
        await self.finish_item(rst)
        rst = SeqItem(rst=1)
        await self.start_item(rst)
        await self.finish_item(rst)

        ops = [SeqItem() for _ in range(200)]
        for op in ops:
            # op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.enable = randint(0, 1)
            op.bus = randint(0, 0xFF)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
