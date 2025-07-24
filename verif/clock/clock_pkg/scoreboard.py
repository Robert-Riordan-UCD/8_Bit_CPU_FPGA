from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

# FIXME: Assuming `WAIT_TIME is 0
class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expected_cont = False
    
    def write(self, op):
        self.logger.info("Write SCB")

        if op.sys_clk.value == 1:
            self.expected_cont = not self.expected_cont

        if op.halt.value == 1:
            assert op.cpu_clk.value == 0, f"ERROR halt: Expected {0}, Actual {op.cpu_clk.value}"
            return

        if op.mode.value == 1:
            assert op.toggle.value == op.cpu_clk.value, f"ERROR manual clk: Expected {op.toggle.value}, Actual {op.cpu_clk.value}"
        else:
            assert self.expected_cont == op.cpu_clk.value, f"ERROR continious clk: Expected {self.expected_cont}, Actual {op.cpu_clk.value}"
