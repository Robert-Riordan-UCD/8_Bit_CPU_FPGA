from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.expected_address = 'xxxx'
    
    def write(self, op):
        if op.rst == 1:
            self.expected_address = 0

        # Check value        
        if op.manual_mode == 1:
            assert op.address.value == op.manual_switches.value, f"ERROR value (MANUAL): expected {op.manual_switches.value}, actual {op.address.value}"
        else:
            assert self.expected_address == op.address.value, f"ERROR value: expected {self.expected_address}, actual {op.address.value}"
    
        if op.rst == 0 and op.manual_mode == 0 and op.read_from_bus == 1:
            self.logger.warning("READ")
            self.expected_address = op.bus.value
    