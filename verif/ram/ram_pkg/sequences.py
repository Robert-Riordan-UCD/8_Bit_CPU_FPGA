from pyuvm import uvm_sequence
from random import randint

from .seq_item import SeqItem

class TestAllSeq(uvm_sequence):
    async def body(self):
        ops = AllOperations("all operations")
        random_operations = RandomOperations("random operations")
        random = Random("random")

        await ops.start(self.sequencer)
        await random_operations.start(self.sequencer)
        await random.start(self.sequencer)

class AllOperations(uvm_sequence):
    async def body(self):
        seqs = [
            # Expected control signals
            SeqItem(name="read bus", address=0x1, bus=0xAB, read_from_bus=1),
            SeqItem(name="read manual", address=0x2, manual_mode=1, manual_read=1, program_switches=0xCD),
            
            # Valid control signals with ignorable signals
            SeqItem(name="manual and bus read, bus mode", manual_read=1, read_from_bus=1, bus=0x67, program_switches=0x89, address=0x5),
            SeqItem(name="manual and bus read, manual mode", manual_read=1, manual_mode=1, read_from_bus=1, bus=0xAB, program_switches=0xCD, address=0x6),
            
            # Invalid control signals
            SeqItem(name="noop"),
            SeqItem(name="manual mode noop", manual_mode=1),
            SeqItem(name="manual mode read from bus noop", manual_mode=1, read_from_bus=1, bus=0x12, address=0x3),
            SeqItem(name="bus mode manual read noop", manual_read=1, program_switches=0x34, address=0x4),
        ]

        for seq in seqs:
            await self.start_item(seq)
            await self.finish_item(seq)

class RandomOperations(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(20000)]
        for op in ops:
            r = randint(0, 1)
            if r == 0: # Read bus
                op.read_from_bus = 1
                op.address = randint(0, 0x0F)
                op.bus = randint(0, 0xFF)
            elif r == 1: # Read manual
                op.manual_mode = 1
                op.manual_read = 1
                op.address = randint(0, 0x0F)
                op.program_switches = randint(0, 0xFF)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)

class Random(uvm_sequence):
    async def body(self):
        ops = [SeqItem() for _ in range(20000)]
        for op in ops:
            op.read_from_bus = randint(0, 1)
            op.manual_mode = randint(0, 1)
            op.manual_read = randint(0, 1)
            op.address = randint(0, 0xF)
            op.program_switches = randint(0, 0xFF)
            op.bus = randint(0, 0xFF)

        for op in ops:
            await self.start_item(op)
            await self.finish_item(op)
