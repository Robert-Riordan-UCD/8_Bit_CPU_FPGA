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

            self.dut.mode.value = op.mode
            self.dut.toggle.value = op.toggle
            self.dut.halt.value = op.halt

            await cocotb.triggers.Edge(self.dut.sys_clk)

            self.logger.info("Run DRV: OP complete")
            self.seq_item_port.item_done()