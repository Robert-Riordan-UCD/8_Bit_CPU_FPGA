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

            self.dut.read_from_bus.value = op.read_from_bus
            self.dut.manual_mode.value = op.manual_mode
            self.dut.manual_read.value = op.manual_read
            self.dut.address.value = op.address
            self.dut.program_switches.value = op.program_switches
            self.dut.bus.value = op.bus

            await cocotb.triggers.FallingEdge(self.dut.clk)

            self.logger.info("Run DRV: OP complete")
            self.seq_item_port.item_done()