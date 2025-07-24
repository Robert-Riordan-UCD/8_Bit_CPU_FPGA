"""
    Coverage Goals
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error

def intxz(value):
    try:
        return int(value)
    except ValueError: # X and Z
        return

class Coverage(uvm_subscriber):
    def __init__(self, parent, name="coverage"):
        super().__init__(name, parent)
        self.logger.info("Init COV")

        self.cpu_clk = set()
        self.mode = set()
        self.toggle = set()
        self.halt = set()

    def write(self, op):
        self.logger.info("Write COV")

        self.cpu_clk.add(int(op.cpu_clk))
        self.mode.add(int(op.mode))
        self.toggle.add(int(op.toggle))
        self.halt.add(int(op.halt))
        
    def report_phase(self):
        self.logger.info("Report COV")
        
        assert 0 in self.cpu_clk, "CPU CLK never 0"
        assert 1 in self.cpu_clk, "CPU CLK never 1"

        assert 0 in self.mode, "MODE never continious"
        assert 1 in self.mode, "MODE never manual"

        assert 0 in self.toggle, "TOGGLE never 0"
        assert 1 in self.toggle, "TOGGLE never 1"

        assert 0 in self.halt, "HALT never 0"
        assert 1 in self.halt, "HALT never 1"
