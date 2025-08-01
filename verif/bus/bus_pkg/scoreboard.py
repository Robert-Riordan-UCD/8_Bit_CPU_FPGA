from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue
import math

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
    
    def write(self, op):
        self.logger.info("Write SCB")

        # Max 1 lane is selected
        assert str(op.select).count('1') <= 1, f"ERROR: too many lanes selected ({op.select})"

        # 0 is output when no lane selected
        if op.select == 0:
            assert op.bus == 0, f"ERROR: No lane selected Expexted 0x00, Actual 0x{int(op.bus):x}"
            return

        # Correct data is output
        start = op.WIDTH*int(math.log2(int(op.select))) + 8
        end = op.WIDTH*int(math.log2(int(op.select)))
        if end == 0:
            expect = str(op.data)[-start:]    
        else:
            expect = str(op.data)[-start:-end]
        assert str(op.bus) == expect, f"ERROR: bus did not match Expected {expect}, Actual {str(op.bus)}"
