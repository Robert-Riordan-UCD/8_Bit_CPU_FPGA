from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        man = ManualMode("manual")
        man_long = ManualLong("manual long")
        cont = ContiniousMode("cont")
        halt_cont = HaltCont("halt continious")
        halt_man = HaltMan("halt manual")
        random = Random("random")

        await man.start(self.sequencer)
        await man_long.start(self.sequencer)
        await cont.start(self.sequencer)
        await halt_cont.start(self.sequencer)
        await halt_man.start(self.sequencer)
        await random.start(self.sequencer)

class ManualMode(uvm_sequence):
    async def body(self):
        clk = False
        for _ in range(100):
            op = SeqItem(mode=1, toggle=clk, halt=0)
            clk = not clk
            await self.start_item(op)
            await self.finish_item(op)

class ManualLong(uvm_sequence):
    async def body(self):
        clk = False
        for _ in range(10):
            for i in range(randint(1, 10)):
                op = SeqItem(mode=1, toggle=clk, halt=0)
                await self.start_item(op)
                await self.finish_item(op)
            clk = not clk

class HaltCont(uvm_sequence):
    async def body(self):
        for _ in range(100):
            op = SeqItem(halt=bool(randint(0, 3)))
            await self.start_item(op)
            await self.finish_item(op)

class HaltMan(uvm_sequence):
    async def body(self):
        clk = False
        for _ in range(100):
            op = SeqItem(mode=1, toggle=clk, halt=bool(randint(0, 3)))
            clk = not clk
            await self.start_item(op)
            await self.finish_item(op)

class ContiniousMode(uvm_sequence):
    async def body(self):
        for _ in range(100):
            op = SeqItem(mode=0, halt=0, toggle=randint(0, 1))
            await self.start_item(op)
            await self.finish_item(op)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(200)]
        for op in ops:
            op.mode = randint(0, 1)
            op.toggle = randint(0, 1)
            op.halt = randint(0, 1)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
