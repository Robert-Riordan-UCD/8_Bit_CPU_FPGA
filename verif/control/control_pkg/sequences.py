from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        load_a = LoadA("load A")
        add = Add("add")
        random = Random("random")

        await load_a.start(self.sequencer)
        await add.start(self.sequencer)
        await random.start(self.sequencer)

class LoadA(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="load A rst", rst=1),
            SeqItem(name="load A step 0", instruction=0b0001),
            SeqItem(name="load A step 1", instruction=0b0001),
            SeqItem(name="load A step 2", instruction=0b0001),
            SeqItem(name="load A step 3", instruction=0b0001),
            SeqItem(name="load A step 4", instruction=0b0001),
            SeqItem(name="load A step 5", instruction=0b0001),
            SeqItem(name="load A step 6", instruction=0b0001),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Add(uvm_sequence):
    async def body(self):
        seqs = [
            SeqItem(name="add rst", rst=1),
            SeqItem(name="add step 0", instruction=0b0010),
            SeqItem(name="add step 1", instruction=0b0010),
            SeqItem(name="add step 2", instruction=0b0010),
            SeqItem(name="add step 3", instruction=0b0010),
            SeqItem(name="add step 4", instruction=0b0010),
            SeqItem(name="add step 5", instruction=0b0010),
            SeqItem(name="add step 6", instruction=0b0010),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(200)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.instruction = randint(0, 0xF)
            op.alu_carry = randint(0, 1)
            op.alu_zero = randint(0, 1)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
