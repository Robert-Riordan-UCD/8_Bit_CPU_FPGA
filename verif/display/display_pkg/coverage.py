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

        self.bus_inputs = set()
        self.values = set()
        self.bus_outputs = set()

    def write(self, op):
        self.logger.info("Write COV")

        # if op.read_from_bus.value == 1 and op.write_to_bus.value == 0:
        #     if not (i := intxz(op.bus)) is None:
        #         self.bus_inputs.add(intxz(i))
        
        # if not (v := intxz(op.value)) is None:
        #     self.values.add(v)

        # if op.write_to_bus == 1 and op.read_from_bus == 0:
        #     if not (o := intxz(op.bus)) is None:
        #         self.bus_outputs.add(intxz(o))
        
    def report_phase(self):
        self.logger.info("Report COV")
        
        # input_cov = len(self.bus_inputs)/0x100
        # if input_cov == 1:
        #     self.logger.info(f"Coverage: All bus inputs covered")
        # elif input_cov > 0.8:
        #     self.logger.warning(f"Coverage MISS: {100*input_cov:0.1f}% bus inputs covered ({len(self.bus_inputs)}/{0x100})")
        # else:
        #     self.logger.error(f"Coverage MISS: {100*input_cov:0.1f}% bus inputs covered ({len(self.bus_inputs)}/{0x100})")            

        # value_cov = len(self.values)/0x100
        # if value_cov == 1:
        #     self.logger.info(f"Coverage: All bus inputs covered")
        # elif value_cov > 0.8:
        #     self.logger.warning(f"Coverage MISS: {100*value_cov:0.1f}% of values covered ({len(self.values)}/{0x100})")
        # else:
        #     self.logger.error(f"Coverage MISS: {100*value_cov:0.1f}% of values covered ({len(self.values)}/{0x100})")

        # output_cov = len(self.bus_outputs)/0x100
        # if output_cov == 1:
        #     self.logger.info(f"Coverage: All bus outputs covered")
        # elif output_cov > 0.8:
        #     self.logger.warning(f"Coverage MISS: {100*output_cov:0.1f}% bus outputs covered ({len(self.bus_outputs)}/{0x100})")
        # else:
        #     self.logger.error(f"Coverage MISS: {100*output_cov:0.1f}% bus outputs covered ({len(self.bus_outputs)}/{0x100})")
