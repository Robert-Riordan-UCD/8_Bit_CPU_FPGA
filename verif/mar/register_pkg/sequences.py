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
            SeqItem(name="bus read", read_from_bus=1, bus=0xA),
            SeqItem(name="manual read", manual_mode=1, manual_read=1, manual_switches=0xB),
            SeqItem(name="rst", rst=1),
            SeqItem(name="bus & manual read (bus mode)", read_from_bus=1, bus=0xA, manual_read=1, manual_switches=0xB),
            SeqItem(name="bus & manual read (manual mode)", read_from_bus=1, bus=0xA, manual_mode=1, manual_read=1, manual_switches=0xB),
            SeqItem(name="bus read & rst", read_from_bus=1, bus=0xA, rst=1),
            SeqItem(name="manual read & rst", manual_mode=1, manual_read=1, manual_switches=0xB, rst=1),
            SeqItem(name="bus read & manual read & rst (bus mode)", read_from_bus=1, bus=0xA, manual_read=1, manual_switches=0xB, rst=1),
            SeqItem(name="bus read & manual read & rst (manual mode)", read_from_bus=1, bus=0xA, manual_mode=1, manual_read=1, manual_switches=0xB, rst=1),
            SeqItem(name="noop"),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(1000)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.read_from_bus = randint(0, 1)
            op.manual_mode = randint(0, 1)
            op.manual_read = randint(0, 1)
            op.manual_switches = randint(0, 0x0F)
            op.bus = randint(0, 0x0F)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
