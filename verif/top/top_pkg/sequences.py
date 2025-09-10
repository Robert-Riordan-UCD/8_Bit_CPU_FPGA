from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        rst = Reset("rst")
        boot0 = Bootload("boot")
        boot1 = Bootload("boot", 1)
        run = Run("run")
        # random = Random("random")

        await rst.start(self.sequencer)
        await boot0.start(self.sequencer)
        await rst.start(self.sequencer)
        await boot1.start(self.sequencer)
        await run.start(self.sequencer)
        # await random.start(self.sequencer)

class Bootload(uvm_sequence):
    def __init__(self, name, program=0):
        super().__init__(name)
        self.prog = program

    async def body(self):
        for _ in range(1000):
            op = SeqItem(enable_bootloader=1, bootloader_program_select=self.prog)
            await self.start_item(op)
            await self.finish_item(op)

class Run(uvm_sequence):
    async def body(self):
        for _ in range(1000):
            op = SeqItem()
            await self.start_item(op)
            await self.finish_item(op)

class Reset(uvm_sequence):
    async def body(self):
        op = SeqItem(rst_n=0)
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
