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
            op.rst_n = self.dut.rst_n
            op.clk_mode = self.dut.clk_mode
            op.clk_pulse = self.dut.clk_pulse
            op.mar_switches = self.dut.mar_switches
            op.ram_switches = self.dut.ram_switches
            op.ram_mode = self.dut.ram_mode
            op.ram_pulse = self.dut.ram_pulse
            op.bootloader_program_select = self.dut.bootloader_program_select
            op.enable_bootloader = self.dut.enable_bootloader
            
            op.segments = self.dut.segments
            op.digit = self.dut.digit
            op.led = self.dut.led
            
            self.analysis_port.write(op)
            # self.logger.info("Run MON: Cycle monitored")