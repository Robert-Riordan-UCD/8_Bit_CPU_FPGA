from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expected_value = 'xxxxxxxx'
    
    def write(self, op):
        self.logger.info("Write SCB")

        if op.rst == 1:
            self.expected_value = 0

        # Check value
        assert self.expected_value == op.value, f"ERROR value: expected {self.expected_value}, actual {op.value}"
    
        # Check bus
        if self.expected_value is int:
            assert op.reg_bus_out == self.expected_value, f"ERROR bus: expected {self.expected_value}, actual {op.reg_bus_out}"

        if op.read_from_bus == 1 and op.rst == 0:
            self.expected_value = op.bus.value
    