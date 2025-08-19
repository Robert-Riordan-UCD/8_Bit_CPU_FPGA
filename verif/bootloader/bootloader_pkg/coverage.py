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

        self.program_select = set()
        self.enable = set()

        self.bootload_address = set()
        self.bootload_ram = set()

    def write(self, op):
        self.logger.info("Write COV")
        
        if op.rst.value == 0:
            self.program_select.add(int(op.program_select.value))
            self.enable.add(int(op.enable_bootload.value))

            self.bootload_address.add(int(op.bootload_address.value))
            self.bootload_ram.add(int(op.bootload_ram.value))

    def report_phase(self):
        self.logger.info("Report COV")

        for i in range(3):
            assert i in self.program_select, f"PROGRAM SELECT never set to {i}"

        assert 0 in self.enable, "ENABLE never 0"
        assert 1 in self.enable, "ENABLE never 1"

        assert 0 in self.bootload_address, "BOOT ADDRESS never 0"
        assert 1 in self.bootload_address, "BOOT ADDRESS never 1"

        assert 0 in self.bootload_ram, "BOOT RAM never 0"
        assert 1 in self.bootload_ram, "BOOT RAM never 1"