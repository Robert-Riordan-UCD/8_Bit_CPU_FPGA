import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from cocotb.binary import BinaryValue

from pyuvm import *

import random

class PCSeqItem(uvm_sequence_item):
    def __init__(self, inc=False, jump=False, out=False, bus_value=0, expected_value=0):
        super().__init__("PCSeqItem")
        self.inc = inc
        self.jump = jump
        self.out = out
        self.bus_value = bus_value
        self.expected_value = expected_value

class PC_Driver(uvm_component):
    def build_phase(self):
        self.seq_item_port = uvm_seq_item_port("seq_item_port", self)

    async def run_phase(self):
        while True:
            next_item = await self.seq_item_port.get_next_item()

            self.dut.inc.value = next_item.inc
            self.dut.jump.value = next_item.jump
            self.dut.out.value = next_item.out

            if next_item.jump == 1 and next_item.out == 0:
                self.dut.bus_driver.setimmediatevalue(next_item.bus_value)
                self.dut.bus_driver._write = True
            else:
                self.dut.bus_driver.setimmediatevalue(BinaryValue(value="zzzzzzzz", n_bits=8))
                self.dut.bus_driver._write = False
            
            await RisingEdge(self.dut.clk)
            self.seq_item_port.item_done()

class PC_Seqence(uvm_sequence):
    async def body(self):
        tx = PCSeqItem()
        await self.start_item(tx)
        
        # Reset
        self.driver.dut.rst.value = 1
        await RisingEdge(self.driver.dut.clk)
        await RisingEdge(self.driver.dut.clk)
        await self.finish_item(tx)
        self.driver.dut.rst.value = 0

        # Increment
        for i in range(3):
            tx = PCSeqItem(inc=True)
            await self.start_item(tx)
            await self.finish_item(tx)

        tx = PCSeqItem(out=True)
        await self.start_item(tx)
        await self.finish_item(tx)

        tx = PCSeqItem(out=False)
        await self.start_item(tx)
        await self.finish_item(tx)

        # Jump
        tx = PCSeqItem(jump=True, bus_value=0xA)
        await self.start_item(tx)
        await self.finish_item(tx)

        # Output
        tx = PCSeqItem(out=True)
        await self.start_item(tx)
        await self.finish_item(tx)

        # 1000 Random tests
        tests = 1000
        while (tests := tests-1):
            tx = PCSeqItem(
                inc=random.randint(0, 1),
                jump=random.randint(0, 1),
                out=random.randint(0, 1),
                bus_value=random.randint(0, 0xF)
            )
            await self.start_item(tx)
            await self.finish_item(tx)


"""
    Compare current state with expectations and report errors
"""
class PC_Scoreboard(uvm_component):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.expected_count = 0
    
    def build_phase(self):
        self.dut = PC_Driver.dut

    async def run_phase(self):
        while True:
            await RisingEdge(self.dut.clk)

            # Count
            if self.dut.rst == 1:
                self.expected_count = 0
            elif self.dut.jump == 1:
                self.expected_count = self.dut.bus.value
            elif self.dut.inc == 1:
                self.expected_count = (self.expected_count+1)

            self.logger.info(f"Expected {self.expected_count}, Bus {self.dut.bus}")
            self.logger.info(f"RST {self.dut.rst}, INC {self.dut.inc}, JUMP {self.dut.jump}, OUT {self.dut.out}")

            # Bus
            if self.dut.out == 1:
                if self.dut.bus.value == self.expected_count:
                    self.logger.info("PC out matches expected")
                else:
                    self.logger.error(f"PC OUT: bus={self.dut.bus.value} - expected={self.expected_count}")

"""
    Test setup
"""
class PCTest(uvm_test):
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        self.driver = PC_Driver("driver", self)
        self.seq = PC_Seqence("seq")
        self.scoreboard = PC_Scoreboard("scoreboard", self)

    def connect_phase(self):
        self.seq.driver = self.driver
        self.seq.driver.dut = self.driver.dut
        self.seq.driver.seq_item_port.connect(self.seqr.seq_item_export)
    
    async def run_phase(self):
        self.raise_objection()
        await self.seq.start(self.seqr)
        self.drop_objection()

"""
    Test entry point
"""
@cocotb.test()
async def run(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    PC_Driver.dut = dut
    await uvm_root().run_test("PCTest")
    await Timer(200, units="ns")