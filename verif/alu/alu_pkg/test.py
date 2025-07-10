from pyuvm import uvm_test

from random import randint

from .seq_item import SeqItem
from .env import Env

class Test(uvm_test):
    def build_phase(self):
        self.logger.info("Build TEST")
        self.env = Env("env", self)
    
    async def run_phase(self):
        self.logger.info("Run TEST")
        self.raise_objection()

        ops = [SeqItem() for _ in range(1000)]
        for op in ops:
            op.rst = 1 if randint(0, 10) == 0 else 0 # Reset 1 in every 10 cycles randomly
            op.a = randint(0, 0xFF)
            op.b = randint(0, 0xFF)
            op.subtract = randint(0, 1)
            op.out = randint(0, 1)
            op.flags_in = randint(0, 1)

        for op in ops:
            self.logger.info(f"Run TEST: {op}")
            await self.env.sequencer.start_item(op)
            await self.env.sequencer.finish_item(op)

        self.drop_objection()