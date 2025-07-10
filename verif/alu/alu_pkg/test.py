from pyuvm import uvm_test

from random import randint

from .seq_item import SeqItem
from .env import Env
from .sequences import TestAllSeq

class Test(uvm_test):
    def build_phase(self):
        self.logger.info("Build TEST")
        self.env = Env("env", self)
    
    def end_of_elaboration_phase(self):
        self.logger.info("End of elaboration TEST")
        self.test_all = TestAllSeq.create("test all")
    
    async def run_phase(self):
        self.logger.info("Run TEST")
        self.raise_objection()

        await self.test_all.start(self.env.sequencer)

        self.drop_objection()