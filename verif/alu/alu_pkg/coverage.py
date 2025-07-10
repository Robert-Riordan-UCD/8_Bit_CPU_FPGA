"""
    Coverage Goals
    Input 
        All operations (ADD/SUB/OUT/Flags in/Reset)
        All inputs value (A/B 0x00 -> 0xFF)
    Output
        All flags hit and not hit (CARRY/ZERO)
        All outputs (0x00 -> 0xFF and 0xZZ)
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error

class Coverage(uvm_subscriber):
    def __init__(self, parent, name="coverage"):
        super().__init__(name, parent)
        self.logger.info("Init COV")

        self.operations = {}
        self.out = {0: 0, 1: 0}
        self.flags_in = {0: 0, 1: 0}
        self.reset = {0: 0, 1: 0}

        self.a = set()
        self.b = set()
        
        self.zero = {0: 0, 1: 0}
        self.carry = {0: 0, 1: 0}
        self.bus = set()
        self.bus_z = 0
    
    def write(self, op):
        self.logger.info("Write COV")
        
        self.operations[int(op.subtract)] = self.operations.get(int(op.subtract), 0) + 1
        self.out[int(op.out)] = self.out.get(int(op.out), 0) + 1
        self.flags_in[int(op.flags_in)] = self.flags_in.get(int(op.flags_in), 0) + 1
        self.reset[int(op.rst)] = self.reset.get(int(op.rst), 0) + 1

        self.a.add(int(op.a))
        self.b.add(int(op.b))

        try:
            self.zero[int(op.zero)] = self.zero.get(int(op.zero), 0) + 1
        except ValueError:
            self.logger.info(f"ValueError: {op.zero} detected in ZERO flag")

        try:
            self.carry[int(op.carry)] = self.carry.get(int(op.carry), 0) + 1
        except ValueError:
            self.logger.info(f"ValueError: {op.carry} detected in CARRY flag")
        
        try:
            b = int(op.bus)
            self.bus.add(b)
        except ValueError:
            if op.bus == "zzzzzzzz":
                self.bus_z += 1
            else:
                self.logger.info(f"ValueError: {op.bus} detected in bus")
    
    def report_phase(self):
        self.logger.info("Report COV")
        
        # Check for all operations
        for op in self.operations:
            try:
                self.logger.info(f"{"SUBTRACT" if op else "ADD"} hit {self.operations[op]} times")
            except KeyError:
                self.logger.error(f"Coverage MISS: {"SUBTRACT" if op else "ADD"} never reached")
        else:
            self.logger.info("All operation hit")

        # Check for output enabled and disabled
        for en in self.out:
            if self.out[en]:
                self.logger.info(f"Output {"enabled" if en else "disabled"} {self.out[en]} times")
            else:
                self.logger.error(f"Coverage MISS: Output {"enabled" if en else "disabled"} never reached")

        # Check for flags enabled and disabled
        for en in self.flags_in:
            if self.flags_in[en]:
                self.logger.info(f"Flags {"enabled" if en else "disabled"} {self.flags_in[en]} times")
            else:
                self.logger.error(f"Coverage MISS: Flags {"enabled" if en else "disabled"} never reached")

        # Check for reset active and inactive
        for rst in self.reset:
            if self.reset[rst]:
                self.logger.info(f"Reset {"active" if rst else "inactive"} {self.reset[rst]} times")
            else:
                self.logger.error(f"Coverage MISS: Reset never {"active" if rst else "inactive"}")
        self.logger.info(f"Reset {self.reset} times")

        # Check A and B hit all values
        a_cov = len(self.a)/0x100
        if a_cov > 0.8:
            self.logger.info(f"A coverage: {a_cov*100:0.1f}% ({len(self.a)}/{0x100})")
        elif a_cov > 0.5:
            self.logger.warning(f"A coverage: {a_cov*100:0.1f}% ({len(self.a)}/{0x100})")
        else:
            self.logger.error(f"A coverage: {a_cov*100:0.1f}% ({len(self.a)}/{0x100})")

        b_cov = len(self.b)/0x100
        if b_cov > 0.8:
            self.logger.info(f"B coverage: {b_cov*100:0.1f}% ({len(self.b)}/{0x100})")
        elif b_cov > 0.5:
            self.logger.warning(f"B coverage: {b_cov*100:0.1f}% ({len(self.b)}/{0x100})")
        else:
            self.logger.error(f"B coverage: {b_cov*100:0.1f}% ({len(self.b)}/{0x100})")

        # Check A and B edge cases
        if not 0 in self.a: self.logger.error(f"A coverage edge case: A never set to 0")
        if not 0xFF in self.a: self.logger.error(f"A coverage edge case: A never set to 0xFF")
        if not 0 in self.b: self.logger.error(f"B coverage edge case: B never set to 0")
        if not 0xFF in self.b: self.logger.error(f"B coverage edge case: B never set to 0xFF")
        
        # Check for ZERO
        for value in self.zero:
            if self.zero[value]:
                self.logger.info(f"ZERO {"set" if value else "unset"} {self.zero[value]} times")
            else:
                self.logger.error(f"Coverage MISS: ZERO never {"set" if value else "unset"}")
        
        # Check for CARRY
        for value in self.carry:
            if self.carry[value]:
                self.logger.info(f"CARRY {"set" if value else "unset"} {self.carry[value]} times")
            else:
                self.logger.error(f"Coverage MISS: CARRY never {"set" if value else "unset"}")

        # Check bus hit all values
        bus_cov = len(self.bus)/0x100
        if bus_cov > 0.8:
            self.logger.info(f"BUS coverage: {bus_cov*100:0.1f}% ({len(self.bus)}/{0x100})")
        elif bus_cov > 0.5:
            self.logger.warning(f"BUS coverage: {bus_cov*100:0.1f}% ({len(self.bus)}/{0x100})")
        else:
            self.logger.error(f"BUS coverage: {bus_cov*100:0.1f}% ({len(self.bus)}/{0x100})")
        
        # Check bus edge cases
        if not 0 in self.bus: self.logger.error(f"BUS coverage edge case: BUS never set to 0")
        if not 0xFF in self.bus: self.logger.error(f"BUS coverage edge case: BUS never set to 0xFF")
        if not self.bus_z: self.logger.error("BUS coverage edge case: BUS never set to 0xZZ")
        else: self.logger.info(f"BUS set to 0xZZ {self.bus_z} times")