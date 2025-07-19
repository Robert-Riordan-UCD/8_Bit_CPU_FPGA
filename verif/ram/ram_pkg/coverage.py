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

        self.address_read = set()
        self.address_writes = set()
        self.bus_reads = set()
        self.bus_writes = set()
        self.manual_reads = set()

    def write(self, op):
        self.logger.info("Write COV")

        # Manual read
        if op.manual_read.value == 1 and op.read_from_bus.value == 0 and op.write_to_bus.value == 0:
            if not (a := intxz(op.address)) is None:
                self.address_read.add(intxz(a))
            if not (p := intxz(op.program_switches)) is None:
                self.manual_reads.add(intxz(p))

        # Bus read
        if op.manual_read.value == 0 and op.read_from_bus.value == 1 and op.write_to_bus.value == 0:
            if not (a := intxz(op.address)) is None:
                self.address_read.add(intxz(a))
            if not (b := intxz(op.bus)) is None:
                self.bus_reads.add(intxz(b))

        # Writes
        if op.manual_read.value == 0 and op.read_from_bus.value == 0 and op.write_to_bus.value == 1:
            if not (a := intxz(op.address)) is None:
                self.address_writes.add(intxz(a))
            if not (b := intxz(op.bus)) is None:
                self.bus_writes.add(intxz(b))

        
    def report_phase(self):
        self.logger.info("Report COV")
        
        addr_read_cov = len(self.address_read)/0x10
        if addr_read_cov == 1:
            self.logger.info(f"Coverage: All address values read")
        elif addr_read_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*addr_read_cov:0.1f}% address read covered ({len(self.address_read)}/{0x10})")
        else:
            self.logger.error(f"Coverage MISS: {100*addr_read_cov:0.1f}% address read covered ({len(self.address_read)}/{0x10})")            

        addr_write_cov = len(self.address_writes)/0x10
        if addr_write_cov == 1:
            self.logger.info(f"Coverage: All address values write")
        elif addr_write_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*addr_write_cov:0.1f}% address write covered ({len(self.address_writes)}/{0x10})")
        else:
            self.logger.error(f"Coverage MISS: {100*addr_write_cov:0.1f}% address write covered ({len(self.address_writes)}/{0x10})")            

        bus_read_cov = len(self.bus_reads)/0x100
        if bus_read_cov == 1:
            self.logger.info(f"Coverage: All bus values read")
        elif bus_read_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*bus_read_cov:0.1f}% bus read covered ({len(self.bus_reads)}/{0x100})")
        else:
            self.logger.error(f"Coverage MISS: {100*bus_read_cov:0.1f}% bus read covered ({len(self.bus_reads)}/{0x100})")  

        bus_write_cov = len(self.bus_writes)/0x100
        if bus_write_cov == 1:
            self.logger.info(f"Coverage: All bus values write")
        elif bus_write_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*bus_write_cov:0.1f}% bus write covered ({len(self.bus_writes)}/{0x100})")
        else:
            self.logger.error(f"Coverage MISS: {100*bus_write_cov:0.1f}% bus write covered ({len(self.bus_writes)}/{0x100})")
        
        man_read_cov = len(self.manual_reads)/0x100
        if man_read_cov == 1:
            self.logger.info(f"Coverage: All program switch values read")
        elif man_read_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*man_read_cov:0.1f}% program switch read covered ({len(self.manual_reads)}/{0x100})")
        else:
            self.logger.error(f"Coverage MISS: {100*man_read_cov:0.1f}% program switch read covered ({len(self.manual_reads)}/{0x100})")  
