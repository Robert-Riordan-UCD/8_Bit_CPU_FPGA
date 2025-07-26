from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        rst = Reset("rst")
        run = Run("run")
        # random = Random("random")

        await rst.start(self.sequencer)
        await run.start(self.sequencer)
        # await random.start(self.sequencer)

class Run(uvm_sequence):
    async def body(self):
        for _ in range(100):
            op = SeqItem()
            await self.start_item(op)
            await self.finish_item(op)

class Reset(uvm_sequence):
    async def body(self):
        op = SeqItem(reset=1)
        await self.start_item(op)
        await self.finish_item(op)

# class Random(uvm_sequence):
#     async def body(self):
#         ops = [SeqItem() for _ in range(5000)]
#         for op in ops:
#             op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
#             op.enable = randint(0, 1)
#             op.bus = randint(0, 0xFF)

#         for op in ops:
#             await self.start_item(op)
#             await self.finish_item(op)
