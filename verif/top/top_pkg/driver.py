from pyuvm import uvm_driver
import cocotb

class Driver(uvm_driver):
    def __init__(self, parent, name="driver"):
        super().__init__(name, parent)
        self.logger.info("Init DRV")
        self.dut = None
    
    def build_phase(self):
        self.logger.info("Build DRV")
        self.dut = cocotb.top
    
    async def run_phase(self):
        self.logger.info("Run DRV")
        while True:
            self.logger.info("Run DRV: Get next OP")
            op = await self.seq_item_port.get_next_item()
            self.logger.info("Run DRV: OP recieved")

            self.dut.rst_n.value = op.rst_n
            self.dut.clk_mode.value = op.clk_mode
            self.dut.clk_pulse.value = op.clk_pulse
            self.dut.mar_switches.value = op.mar_switches
            self.dut.ram_switches.value = op.ram_switches
            self.dut.ram_mode.value = op.ram_mode
            self.dut.ram_pulse.value = op.ram_pulse
            self.dut.bootloader_program_select = op.bootloader_program_select
            self.dut.enable_bootloader = op.enable_bootloader

            await cocotb.triggers.FallingEdge(self.dut.clk)

            self.logger.info("Run DRV: OP complete")
            self.seq_item_port.item_done()