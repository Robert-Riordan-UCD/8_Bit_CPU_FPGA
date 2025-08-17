from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.stored_values = ['xxxxxxxx' for _ in range(0x10)]
    
    def write(self, op):
        self.logger.info("Write SCB")

        # Check write to bus
        if self.stored_values[int(op.address.value)] is int:
            assert op.ram_bus_out == self.stored_values[int(op.address.value)], f"ERROR write: expected {self.stored_values[int(op.address.value)]}, actual {op.ram_bus_out} (address {op.address})"

        if op.read_from_bus == 1 and op.manual_mode == 0:
            self.stored_values[int(op.address.value)] = op.bus.value
        elif op.manual_read == 1 and op.manual_mode == 1:
            self.stored_values[int(op.address.value)] = op.program_switches.value

        # Check read from bus
        if op.read_from_bus == 1 and op.manual_mode == 0:
            assert op.bus == self.stored_values[int(op.address.value)], f"ERROR read from bus: expected {self.stored_values[int(op.address.value)]}, actual {op.bus.value}"

        # Check manual read
        if op.manual_mode == 1 and op.manual_read == 1:
            assert op.program_switches == self.stored_values[int(op.address.value)], f"ERROR manual read: expected {self.stored_values[int(op.address.value)]}, actual {op.program_switches.value}"
