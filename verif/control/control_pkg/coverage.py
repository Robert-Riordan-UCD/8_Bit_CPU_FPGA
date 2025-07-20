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

        self.jump_carry = False
        self.jump_zero = False
        self.no_jump_carry = False
        self.no_jump_zero = False

        self.clk_halt = set()
        self.pc_inc = set()
        self.pc_jump = set()
        self.pc_out = set()
        self.a_reg_read_from_bus = set()
        self.a_reg_write_to_bus = set()
        self.b_reg_read_from_bus = set()
        self.b_reg_write_to_bus = set()
        self.i_reg_read_from_bus = set()
        self.i_reg_write_to_bus = set()
        self.mar_read_from_bus = set()
        self.ram_read_from_bus = set()
        self.ram_write_to_bus = set()
        self.alu_out = set()
        self.alu_subtract = set()
        self.alu_flags_in = set()
        self.out_en = set()

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
            if self.current_ins == 0b0111: # Jump carry
                if op.alu_carry == 1: self.jump_carry = True
                else:                 self.no_jump_carry = True
            elif self.current_ins == 0b1000: # Jump zero
                if op.alu_zero == 1: self.jump_zero = True
                else:                self.no_jump_zero = True
        elif self.current_ins == op.instruction.value:
            self.ins_count += 1

        if self.ins_count >= 5:
            self.ins_count = 0
            if not (i := intxz(op.instruction)) is None:
                self.instructions[i] = self.instructions.get(i, 0) + 1

        self.clk_halt.add(int(op.clk_halt.value))
        self.pc_inc.add(int(op.pc_inc.value))
        self.pc_jump.add(int(op.pc_jump.value))
        self.pc_out.add(int(op.pc_out.value))
        self.a_reg_read_from_bus.add(int(op.a_reg_read_from_bus.value))
        self.a_reg_write_to_bus.add(int(op.a_reg_write_to_bus.value))
        self.b_reg_read_from_bus.add(int(op.b_reg_read_from_bus.value))
        self.b_reg_write_to_bus.add(int(op.b_reg_write_to_bus.value))
        self.i_reg_read_from_bus.add(int(op.i_reg_read_from_bus.value))
        self.i_reg_write_to_bus.add(int(op.i_reg_write_to_bus.value))
        self.mar_read_from_bus.add(int(op.mar_read_from_bus.value))
        self.ram_read_from_bus.add(int(op.ram_read_from_bus.value))
        self.ram_write_to_bus.add(int(op.ram_write_to_bus.value))
        self.alu_out.add(int(op.alu_out.value))
        self.alu_subtract.add(int(op.alu_subtract.value))
        self.alu_flags_in.add(int(op.alu_flags_in.value))
        self.out_en.add(int(op.out_en.value))

    def report_phase(self):
        self.logger.info("Report COV")

        for i in range(0, 0x10):
            if i in self.instructions:
                self.logger.info(f"Coverage: Instruction {i} covered {self.instructions[i]} times")
            else:
                self.logger.error(f"Coverage MISS: Instruction {i} missed")

        assert self.jump_carry, "JUMP CARRY never called with ALU CARRY set"
        assert self.no_jump_carry, "JUMP CARRY never called without ALU CARRY set"
        assert self.jump_zero, "JUMP ZERO never called with ALU ZERO set"
        assert self.no_jump_zero, "JUMP ZERO never called without ALU ZERO set"

        assert 0 in self.clk_halt, "HALT never 0"
        assert 1 in self.clk_halt, "HALT never 1"
        
        assert 0 in self.pc_inc, "PC INC never 0"
        assert 1 in self.pc_inc, "PC INC never 1"
        
        assert 0 in self.pc_out, "PC OUT never 0"
        assert 1 in self.pc_out, "PC out never 1"
        
        assert 0 in self.pc_jump, "PC JUMP never 0"
        assert 1 in self.pc_jump, "PC JUMP never 1"
        
        assert 0 in self.a_reg_read_from_bus, "A READ never 0"
        assert 1 in self.a_reg_read_from_bus, "A READ never 1"
        
        assert 0 in self.a_reg_write_to_bus, "A WRITE never 0"
        assert 1 in self.a_reg_write_to_bus, "A WRITE never 1"
        
        assert 0 in self.b_reg_read_from_bus, "B READ never 0"
        assert 1 in self.b_reg_read_from_bus, "B READ never 1"
        
        assert 0 in self.b_reg_write_to_bus, "B WRITE never 0"
        # assert 1 in self.b_reg_write_to_bus, "B WRITE never 1"
        assert not 1 in self.b_reg_write_to_bus, "B WRITE 1 but no instruction to set B WRITE"
        
        assert 0 in self.i_reg_read_from_bus, "I READ never 0"
        assert 1 in self.i_reg_read_from_bus, "I READ never 1"

        assert 0 in self.i_reg_write_to_bus, "I WRITE never 0"
        assert 1 in self.i_reg_write_to_bus, "I WRITE never 1"

        assert 0 in self.mar_read_from_bus, "MAR READ never 0"
        assert 1 in self.mar_read_from_bus, "MAR READ never 1"

        assert 0 in self.ram_read_from_bus, "RAM READ never 0"
        assert 1 in self.ram_read_from_bus, "RAM READ never 1"
        
        assert 0 in self.ram_write_to_bus, "RAM WRITE never 0"
        assert 1 in self.ram_write_to_bus, "RAM WRITE never 1"
        
        assert 0 in self.alu_out, "ALU OUT never 0"
        assert 1 in self.alu_out, "ALU OUT never 1"
        
        assert 0 in self.alu_flags_in, "ALU FLAGS IN never 0"
        assert 1 in self.alu_flags_in, "ALU FLAGS IN never 1"
        
        assert 0 in self.alu_subtract, "ALU SUB never 0"
        assert 1 in self.alu_subtract, "ALU SUB never 1"
        
        assert 0 in self.out_en, "OUT EN never 0"
        assert 1 in self.out_en, "OUT EN never 1"
