from pyuvm import uvm_monitor, uvm_analysis_port
import cocotb
from .seq_item import SeqItem

class Monitor(uvm_monitor):
    def __init__(self, parent, name="monitor"):
        super().__init__(name, parent)
        self.logger.info("Init MON")
        self.dut = None
        self.analysis_port = uvm_analysis_port("ap", self)
        self.previous_value = 0

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
            op.read_from_bus = self.dut.read_from_bus
            op.write_to_bus = self.dut.write_to_bus
            op.bus_driver = self.dut.bus_driver
            
            op.bus = self.dut.bus
            op.value = self.dut.value
            op.previous_value = self.previous_value

            self.previous_value = self.dut.value

            self.analysis_port.write(op)
            # self.logger.info("Run MON: Cycle monitored")