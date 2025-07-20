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

        self.counter = 0
        self.current_ins = None
        self.ins_count = 0
        self.instructions = {}

    def write(self, op):
        self.logger.info("Write COV")
        
        # Only add instruction to coverage if it is maintained for the full duration after the fetch cycle
        if op.rst == 1 or self.counter == 6:
            self.counter = 0
        else:
            self.counter += 1

        if self.counter == 3:
            self.current_ins = op.instruction.value
            self.ins_count = 1
        elif self.current_ins == op.instruction.value:
            self.ins_count += 1

        if self.ins_count >= 5:
            self.ins_count = 0
            if not (i := intxz(op.instruction)) is None:
                self.instructions[i] = self.instructions.get(i, 0) + 1



    def report_phase(self):
        self.logger.info("Report COV")

        for i in range(0, 0x10):
            if i in self.instructions:
                self.logger.info(f"Coverage: Instruction {i} covered {self.instructions[i]} times")
            else:
                self.logger.error(f"Coverage MISS: Instruction {i} missed")
