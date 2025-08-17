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

        self.bus_outputs = set()
        self.jump_input = set()

    def write(self, op):
        self.logger.info("Write COV")

        if op.jump.value == 0:
            if not (o := intxz(op.pc_out)) is None:
                self.bus_outputs.add(intxz(o))
        
        if op.jump.value == 1:
            if not (j := intxz(op.bus)) is None:
                self.jump_input.add(intxz(j))
        
    def report_phase(self):
        self.logger.info("Report COV")
        
        output_cov = len(self.bus_outputs)/0x10
        if output_cov == 1:
            self.logger.info(f"Coverage: All bus outputs covered")
        elif output_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*output_cov:0.1f}% bus outputs covered ({len(self.bus_outputs)}/{0x10})")
        else:
            self.logger.error(f"Coverage MISS: {100*output_cov:0.1f}% bus outputs covered ({len(self.bus_outputs)}/{0x10})")            

        jump_cov = len(self.jump_input)/0x100
        if jump_cov == 1:
            self.logger.info(f"Coverage: All jump inputs covered")
        elif jump_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*jump_cov:0.1f}% jump inputs covered ({len(self.jump_input)}/{0x100})")
            for i in range(0x100):
                if not i in self.jump_input:
                    self.logger.warning(f"MISSED: 0x{i:02x}")
        else:
            self.logger.error(f"Coverage MISS: {100*jump_cov:0.1f}% jump inputs covered ({len(self.jump_input)}/{0x100})")
