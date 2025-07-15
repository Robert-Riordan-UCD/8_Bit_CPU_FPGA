from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expected_address = 'xxxx'
    
    def write(self, op):
        self.logger.info("Write SCB")

        if op.rst == 1:
            self.expected_address = 0

        # Check value
        assert self.expected_address == op.address, f"ERROR value: expected {self.expected_address}, actual {op.address}"
    
        if op.rst == 0:
            if op.manual_mode == 1 and op.manual_read == 1:
                self.expected_address = op.manual_switches.value
            elif op.manual_mode == 0 and op.read_from_bus == 1:
                self.expected_address = op.bus.value
    