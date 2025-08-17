from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expected_value = '0000xxxx'
    
    def write(self, op):
        self.logger.info("Write SCB")

        self.logger.info(f"PREVIOUS: {self.expected_value}")
        self.logger.info(op)

        if op.rst == 1:
            self.expected_value = 0

        # Check value
        assert self.expected_value == op.pc_out, f"ERROR: expected {self.expected_value}, actual {op.pc_out}"
    
        if op.jump == 1 and op.inc == 0 and op.rst == 0:
            self.expected_value = op.bus.value % 0x10
        elif self.expected_value == '0000xxxx':
            return
        elif op.inc == 1 and op.jump == 0 and op.rst == 0:
            self.expected_value = (self.expected_value + 1) % 0x10
        