from pyuvm import uvm_subscriber, uvm_analysis_export
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expected_carry = 'x'
        self.expected_zero = 'x'
    
    def write(self, op):
        self.logger.info("Write SCB")
        result = op.a.value - op.b.value if op.subtract.value == 1 else op.a.value + op.b.value
        expected_bus = result % 0x100

        if op.rst.value == 1:
            self.expected_carry = 0
            self.expected_zero = 0

        assert op.bus == expected_bus, f"Bus ERROR: got {op.bus} expected {expected_bus}"

        assert op.carry.value == self.expected_carry, f"Carry ERROR: Expected {self.expected_carry}, Actual {op.carry.value}"
        assert op.zero.value == self.expected_zero, f"Zero ERROR: Expected {self.expected_zero}, Actual {op.zero.value}"

        if op.flags_in.value == 1 and op.rst.value == 0:
            if op.subtract.value == 1:
                self.expected_carry = (int(op.a.value) < int(op.b.value))
            else:
                self.expected_carry = (result > 0xFF)
            self.expected_zero = ((result % 0x100) == 0)
