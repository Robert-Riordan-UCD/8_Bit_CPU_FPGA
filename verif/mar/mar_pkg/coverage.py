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
        self.manual_inputs = set()
        self.addresses = set()

    def write(self, op):
        self.logger.info("Write COV")

        if op.read_from_bus.value == 1 and op.manual_mode == 0:
            if not (i := intxz(op.bus)) is None:
                self.bus_inputs.add(intxz(i))
        
        if op.manual_read == 1 and op.manual_mode == 1:
            if not (s := intxz(op.manual_switches)) is None:
                self.manual_inputs.add(intxz(s))

        if not (a := intxz(op.address)) is None:
            self.addresses.add(a)

    def report_phase(self):
        self.logger.info("Report COV")
        
        bus_cov = len(self.bus_inputs)/0x10
        if bus_cov == 1:
            self.logger.info(f"Coverage: All bus inputs covered")
        elif bus_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*bus_cov:0.1f}% bus inputs covered ({len(self.bus_inputs)}/{0x10})")
        else:
            self.logger.error(f"Coverage MISS: {100*bus_cov:0.1f}% bus inputs covered ({len(self.bus_inputs)}/{0x10})")            

        switch_cov = len(self.manual_inputs)/0x10
        if switch_cov == 1:
            self.logger.info(f"Coverage: All manual inputs covered")
        elif switch_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*switch_cov:0.1f}% manual inputs covered ({len(self.manual_inputs)}/{0x10})")
        else:
            self.logger.error(f"Coverage MISS: {100*switch_cov:0.1f}% manual inputs covered ({len(self.manual_inputs)}/{0x10})")

        addr_cov = len(self.addresses)/0x10
        if addr_cov == 1:
            self.logger.info(f"Coverage: All addresses covered")
        elif addr_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*addr_cov:0.1f}% of addresses covered ({len(self.addresses)}/{0x10})")
        else:
            self.logger.error(f"Coverage MISS: {100*addr_cov:0.1f}% of addresses covered ({len(self.addresses)}/{0x10})")
