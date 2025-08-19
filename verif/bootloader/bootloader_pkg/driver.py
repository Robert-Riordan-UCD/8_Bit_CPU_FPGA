from pyuvm import uvm_driver
import cocotb

class Driver(uvm_driver):
    def __init__(self, parent, name="driver"):
        super().__init__(name, parent)
        self.logger.info("Init DRV")
        self.dut = None
        self.monitor = None
    
    def build_phase(self):
        self.logger.info("Build DRV")
        self.dut = cocotb.top
    
    async def run_phase(self):
        self.logger.info("Run DRV")
        while True:
            self.logger.info("Run DRV: Get next OP")
            op = await self.seq_item_port.get_next_item()
            self.logger.info("Run DRV: OP recieved")

            self.dut.rst.value = op.rst
            self.dut.program_select.value = op.program_select
            self.dut.enable_bootload = op.enable_bootload

            await cocotb.triggers.FallingEdge(self.dut.clk)

            self.logger.info("Run DRV: OP complete")
            self.seq_item_port.item_done()