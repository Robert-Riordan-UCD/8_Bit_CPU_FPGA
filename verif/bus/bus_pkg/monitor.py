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
            op.select = self.dut.lane_select
            op.data = self.dut.lane_data
            
            op.bus = self.dut.bus_data
            
            self.analysis_port.write(op)
            # self.logger.info("Run MON: Cycle monitored")