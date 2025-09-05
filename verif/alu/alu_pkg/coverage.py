"""
    Coverage Goals
    Input 
        All operations (ADD/SUB/OUT/Flags in/Reset)
        All inputs value (A/B 0x00 -> 0xFF)
    Output
        All flags hit and not hit (CARRY/ZERO)
        All outputs (0x00 -> 0xFF and 0xZZ)
"""

    # input subtract,
    # input flags_in,

    # output logic carry,
    # output logic zero

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from cocotb_coverage.coverage import  CoverPoint, CoverCross, coverage_db

@CoverPoint(
    "top.a",
    xf=lambda op: op.a,
    bins = [i for i in range(0x100)]
)
def point_a(op): pass

@CoverPoint(
    "top.b",
    xf=lambda op: op.b,
    bins = [i for i in range(0x100)]
)
def point_b(op): pass

@CoverPoint(
    "top.bus",
    xf=lambda op: op.bus,
    bins = [i for i in range(0x100)]
)
def point_bus(op): pass

@CoverPoint(
    "top.subtract",
    xf=lambda op: op.subtract,
    bins = [0, 1]
)
def point_subtract(op): pass

@CoverPoint(
    "top.flags_in",
    xf=lambda op: op.flags_in,
    bins = [0, 1]
)
def point_flags_in(op): pass

@CoverPoint(
    "top.carry",
    xf=lambda op: op.carry,
    bins = [0, 1]
)
def point_carry(op): pass

@CoverPoint(
    "top.zero",
    xf=lambda op: op.zero,
    bins = [0, 1]
)
def point_zero(op): pass

@CoverCross(
    "top.cross_sub_fi_carry_zero",
    items=["top.subtract", "top.flags_in", "top.carry", "top.zero"]
)
def cross_sub_fi_carry_zero(op): pass

class Coverage(uvm_subscriber):
    def write(self, op):
        point_a(op)
        point_b(op)
        point_bus(op)
        point_subtract(op)
        point_flags_in(op)
        point_carry(op)
        point_zero(op)
        cross_sub_fi_carry_zero(op)
            
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