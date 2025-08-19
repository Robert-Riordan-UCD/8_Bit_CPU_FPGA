from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        reset = Reset("rst")
        disable = Disable("disable")
        all_prog = AllPrograms("all programs")
        random = Random("random")

        await reset.start(self.sequencer)
        await disable.start(self.sequencer)
        await all_prog.start(self.sequencer)
        await random.start(self.sequencer)

class Reset(uvm_sequence):
    async def body(self):
        rst = SeqItem(name="rst", rst=1)
        await self.start_item(rst)
        await self.finish_item(rst)

class Disable(uvm_sequence):
    async def body(self):
        for _ in range(100):
            seq = SeqItem(program_select=randint(0, 3), enable_bootload=0)

            await self.start_item(seq)
            await self.finish_item(seq)

class AllPrograms(uvm_sequence):
    async def body(self):
        for prog in range(4):
            reset = Reset("reset")    
            await reset.start(self.sequencer)

            for _ in range(randint(32, 100)):
                seq = SeqItem(program_select=prog, enable_bootload=1)

                await self.start_item(seq)
                await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        for _ in range(2000):
            seq = SeqItem(rst=randint(0, 20) == 0, program_select=randint(0, 1), enable_bootload=randint(0, 1))

            await self.start_item(seq)
            await self.finish_item(seq)