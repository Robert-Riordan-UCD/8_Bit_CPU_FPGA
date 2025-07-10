from pyuvm import uvm_monitor, uvm_analysis_port
import cocotb
from .seq_item import SeqItem

class Monitor(uvm_monitor):
    def __init__(self, parent, name="monitor"):
        super().__init__(name, parent)
        self.logger.info("Init MON")
        self.dut = None
        self.analysis_port = uvm_analysis_port("ap", self)

    def build_phase(self):
        self.logger.info("Build MON")
        self.dut = cocotb.top
    
    async def run_phase(self):
        self.logger.info("Run MON")
        while True:
            # self.logger.info("Run MON: Wait for CLK")
            await cocotb.triggers.RisingEdge(self.dut.clk)

            op = SeqItem()
            op.rst = self.dut.rst
            op.a = self.dut.a
            op.b = self.dut.b
            op.out = self.dut.out
            op.subtract = self.dut.subtract
            op.flags_in = self.dut.flags_in

            op.bus = self.dut.bus
            op.carry = self.dut.carry
            op.zero = self.dut.zero

            self.analysis_port.write(op)
            # self.logger.info("Run MON: Cycle monitored")