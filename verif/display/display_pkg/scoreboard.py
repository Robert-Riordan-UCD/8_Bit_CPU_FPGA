from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue
from .segments import Segments

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expected_segments = 'xxxxxxxx'
        self.expected_digit = 'xxxx'
    
    def write(self, op):
        # self.logger.info("Write SCB")

        if op.rst == 1:
            self.expected_digit = 0b0001
            self.expected_segments = {
                0b0001: Segments[0],
                0b0010: Segments[0],
                0b0100: Segments[0],
                0b1000: Segments[0]
            }
        else:
            # FIXME: I should only be updating on the rising edge of the clk but I'm not sure how. This should work because the signals only change on the falling edge so enable should remain constant throughout the clk high period
            if (op.enable == 1) and op.cpu_clk == 1:
                self.expected_segments = {
                    0b0001: Segments[ int(op.bus.value) % 10],
                    0b0010: Segments[(int(op.bus.value) // 10) % 10],
                    0b0100: Segments[(int(op.bus.value) // 100) % 10],
                    0b1000: Segments[(int(op.bus.value) // 1000) % 10]
                }
        
        if self.expected_digit == "xxxx": return

        # Check correct digit is displayed
        assert op.digit.value == self.expected_digit, f"ERROR wrong digit selected: Expected {self.expected_digit}, Actual {op.digit.value}"

        # Check correct segments are displayed
        assert op.segments.value == self.expected_segments[self.expected_digit], f"ERROR wrong segments: Expected {self.expected_segments[self.expected_digit]:02x}, Actual {int(op.segments.value):02x}"

        if op.rst == 0:
            self.expected_digit *= 2
            if self.expected_digit > 8:
                self.expected_digit = 0b0001

