"""
    Coverage Goals
    All valid sements hit
    All valid digits hit
    All bus values in
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from .segments import Segments

def intxz(value):
    try:
        return int(value)
    except ValueError: # X and Z
        return

class Coverage(uvm_subscriber):
    def __init__(self, parent, name="coverage"):
        super().__init__(name, parent)
        self.logger.info("Init COV")

        self.segments = set()
        self.digits = set()
        self.bus_inputs = set()

    def write(self, op):
        # self.logger.info("Write COV")

        if (s := intxz(op.segments.value)): self.segments.add(s)
        if (d := intxz(op.digit.value)): self.digits.add(d)

        if op.enable == 1 and op.cpu_clk == 1 and op.rst == 0:
            if not (b := intxz(op.bus.value)) is None:
                self.bus_inputs.add(b)

        
    def report_phase(self):
        self.logger.info("Report COV")

        for i, s in enumerate(Segments):
            if not s in self.segments:
                self.logger.error(f"Coverage ERROR: Missed segments for {i} ({s:02x})")
        
        for i in range(1, 5):
            if not 2**1 in self.digits:
                self.logger.error(f"Coverage ERROR: Missed digit {i**2:04b} ({2**1})")

        bus_cov = len(self.bus_inputs)/0x100
        if bus_cov == 1.0:
            self.logger.info(f"Bus coverage: {bus_cov*100:0.1f}% ({len(self.bus_inputs)}/{0x100})")
        elif bus_cov > 0.8:
            self.logger.warning(f"Bus coverage: {bus_cov*100:0.1f}% ({len(self.bus_inputs)}/{0x100})")
            for i in range(0x100):
                if not i in self.bus_inputs:
                    self.logger.info(f"Bus input missed: 0x{i:02x}")
        else:
            self.logger.error(f"Bus coverage: {bus_cov*100:0.1f}% ({len(self.bus_inputs)}/{0x100})")
