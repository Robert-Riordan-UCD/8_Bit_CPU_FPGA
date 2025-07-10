from pyuvm import uvm_component, uvm_analysis_export
from cocotb.binary import BinaryValue

class Scoreboard(uvm_component):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        # self.analysis_export = uvm_analysis_export("analysis export", self)
    
    def write(self, op):
        self.logger.info("Write SCB")
        result = op.a - op.b if op.subtract else op.a + op.b
        expected_bus = result % 0xFF if op.out else BinaryValue(value="zzzzzzzz", n_bits=8)

        assert op.bus == expected_bus, f"Bus ERROR: got {op.bus} expected {expected_bus}"

        if op.flags_in:
            assert op.carry == (result > 0xFF), "Carry ERROR"
            assert op.zero == (expected_bus == 0), "Zero ERROR"
    
    # def connect_phase(self):
    #     self.logger.info("Connect SCB")
    #     self.analysis_export.write = self.write