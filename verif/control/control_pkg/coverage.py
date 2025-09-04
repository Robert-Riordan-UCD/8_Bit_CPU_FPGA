"""
    Coverage Goals
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from cocotb_coverage.coverage import  CoverPoint, CoverCross, CoverCheck, coverage_db

@CoverPoint(
    "top.clk_halt",
    xf=lambda op: int(op.clk_halt),
    bins = [0, 1]
)
def point_clk_halt(op): pass

@CoverPoint(
    "top.pc_inc",
    xf=lambda op: int(op.pc_inc),
    bins = [0, 1]
)
def point_pc_inc(op): pass

@CoverPoint(
    "top.pc_jump",
    xf=lambda op: int(op.pc_jump),
    bins = [0, 1]
)
def point_pc_jump(op): pass

@CoverPoint(
    "top.pc_out",
    xf=lambda op: int(op.pc_out),
    bins = [0, 1]
)
def point_pc_out(op): pass

@CoverPoint(
    "top.a_reg_read_from_bus",
    xf=lambda op: int(op.a_reg_read_from_bus),
    bins = [0, 1]
)
def point_a_reg_read_from_bus(op): pass

@CoverPoint(
    "top.a_reg_write_to_bus",
    xf=lambda op: int(op.a_reg_write_to_bus),
    bins = [0, 1]
)
def point_a_reg_write_to_bus(op): pass

@CoverPoint(
    "top.b_reg_read_from_bus",
    xf=lambda op: int(op.b_reg_read_from_bus),
    bins = [0, 1]
)
def point_b_reg_read_from_bus(op): pass

@CoverCheck(
    "top.b_reg_write_to_bus",
    f_fail=lambda op: int(op.b_reg_write_to_bus) == 1,
    f_pass=lambda op: int(op.b_reg_write_to_bus) == 0
)
def check_b_reg_write_to_bus(op): pass

@CoverPoint(
    "top.i_reg_read_from_bus",
    xf=lambda op: int(op.i_reg_read_from_bus),
    bins = [0, 1]
)
def point_i_reg_read_from_bus(op): pass

@CoverPoint(
    "top.i_reg_write_to_bus",
    xf=lambda op: int(op.i_reg_write_to_bus),
    bins = [0, 1]
)
def point_i_reg_write_to_bus(op): pass

@CoverPoint(
    "top.mar_read_from_bus",
    xf=lambda op: int(op.mar_read_from_bus),
    bins = [0, 1]
)
def point_mar_read_from_bus(op): pass

@CoverPoint(
    "top.ram_read_from_bus",
    xf=lambda op: int(op.ram_read_from_bus),
    bins = [0, 1]
)
def point_ram_read_from_bus(op): pass

@CoverPoint(
    "top.ram_write_to_bus",
    xf=lambda op: int(op.ram_write_to_bus),
    bins = [0, 1]
)
def point_ram_write_to_bus(op): pass

@CoverPoint(
    "top.alu_out",
    xf=lambda op: int(op.alu_out),
    bins = [0, 1]
)
def point_alu_out(op): pass

@CoverPoint(
    "top.alu_subtract",
    xf=lambda op: int(op.alu_subtract),
    bins = [0, 1]
)
def point_alu_subtract(op): pass

@CoverPoint(
    "top.alu_flags_in",
    xf=lambda op: int(op.alu_flags_in),
    bins = [0, 1]
)
def point_alu_flags_in(op): pass

@CoverPoint(
    "top.out_en",
    xf=lambda op: int(op.out_en),
    bins = [0, 1]
)
def point_out_en(op): pass

@CoverPoint(
    "top.boot_write_to_bus",
    xf=lambda op: int(op.boot_write_to_bus),
    bins = [0, 1]
)
def point_boot_write_to_bus(op): pass

@CoverCheck(
    "top.check_bus_drivers",
    f_fail=lambda op: sum([
        int(op.pc_out),
        int(op.a_reg_write_to_bus),
        int(op.b_reg_write_to_bus),
        int(op.i_reg_write_to_bus),
        int(op.ram_write_to_bus),
        int(op.alu_out),
        int(op.boot_write_to_bus),
    ]) > 1
)
def check_only_one_bus_driver(op): pass

@CoverPoint(
    "top.instruction",
    xf=lambda op: int(op.instruction),
    bins = [i for i in range(16)]
)
def point_instruction(op): pass

@CoverPoint(
    "top.alu_zero",
    xf=lambda op: int(op.alu_zero),
    bins = [0, 1]
)
def point_alu_zero(op): pass

@CoverPoint(
    "top.jump_zero",
    xf=lambda op: int(op.instruction) == 0b1000,
    bins = [0, 1]
)
def point_jump_zero(op): pass

@CoverCross(
    "top.cross_jump_zero",
    items=["top.alu_zero", "top.jump_zero"],
    ign_bins = [(0,0)]
)
def cross_jump_zero(op): pass

@CoverPoint(
    "top.alu_carry",
    xf=lambda op: int(op.alu_carry),
    bins = [0, 1]
)
def point_alu_carry(op): pass

@CoverPoint(
    "top.jump_carry",
    xf=lambda op: int(op.instruction) == 0b0111,
    bins = [0, 1]
)
def point_jump_carry(op): pass

@CoverCross(
    "top.cross_jump_carry",
    items=["top.alu_carry", "top.jump_carry"],
    ign_bins = [(0,0)]
)
def cross_jump_carry(op): pass

class Coverage(uvm_subscriber):
    def __init__(self, parent, name="coverage"):
        super().__init__(name, parent)
        self.logger.info("Init COV")

        self.counter = 0
        self.current_ins = None
        self.ins_count = 0

    def write(self, op):
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
            point_instruction(op)

        point_clk_halt(op)
        point_pc_inc(op)
        point_pc_jump(op)
        point_pc_out(op)
        point_a_reg_read_from_bus(op)
        point_a_reg_write_to_bus(op)
        point_b_reg_read_from_bus(op)
        check_b_reg_write_to_bus(op)
        point_i_reg_read_from_bus(op)
        point_i_reg_write_to_bus(op)
        point_mar_read_from_bus(op)
        point_ram_read_from_bus(op)
        point_ram_write_to_bus(op)
        point_alu_out(op)
        point_alu_subtract(op)
        point_alu_flags_in(op)
        point_out_en(op)
        point_boot_write_to_bus(op)
        check_only_one_bus_driver(op)

        point_alu_zero(op)
        point_jump_zero(op)
        cross_jump_zero(op)
        point_alu_carry(op)
        point_jump_carry(op)
        cross_jump_carry(op)

    def report_phase(self):
        coverage_db.export_to_yaml("coverage.yaml")

        for name, coverpoint in coverage_db.items():
            if coverpoint.cover_percentage <= 0:
                self.logger.error(f"COVER MISS: {name} {coverpoint.cover_percentage}%")
            elif coverpoint.cover_percentage < 100:
                self.logger.warning(f"COVER GAP: {name} {coverpoint.cover_percentage}%")
                self.logger.warning(f"                  {coverpoint.detailed_coverage}")
            else:
                self.logger.info(f"{name} {coverpoint.cover_percentage}%")

        self.logger.info("Coverage saved to coverage.yaml")
