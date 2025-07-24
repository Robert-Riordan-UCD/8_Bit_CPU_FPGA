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
            await cocotb.triggers.Edge(self.dut.sys_clk)
            await cocotb.triggers.Timer(0.1, units="ns")

            op = SeqItem()
            op.mode = self.dut.mode
            op.toggle = self.dut.toggle
            op.halt = self.dut.halt

            op.cpu_clk = self.dut.cpu_clk
            op.sys_clk = self.dut.sys_clk

            self.analysis_port.write(op)
            # self.logger.info("Run MON: Cycle monitored")