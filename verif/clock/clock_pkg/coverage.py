"""
    Coverage Goals
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from cocotb_coverage.coverage import  CoverPoint, CoverCross, coverage_db

@CoverPoint(
    "top.cpu_clk",
    xf=lambda op: int(op.cpu_clk),
    bins = [0, 1]
)
def point_cpu_clk(op): pass

@CoverPoint(
    "top.mode",
    xf=lambda op: int(op.mode),
    bins = [0, 1]
)
def point_mode(op): pass

@CoverPoint(
    "top.toggle",
    xf=lambda op: int(op.toggle),
    bins = [0, 1]
)
def point_toggle(op): pass

@CoverPoint(
    "top.halt",
    xf=lambda op: int(op.halt),
    bins = [0, 1]
)
def point_halt(op): pass

@CoverCross(
    "top.cross_mode_toggle_halt",
    items=["top.mode", "top.toggle", "top.halt"]
)
def cross_cover(op): pass

class Coverage(uvm_subscriber):
    def write(self, op):
        point_cpu_clk(op)
        point_mode(op)
        point_toggle(op)
        point_halt(op)
        cross_cover(op)
        
    def report_phase(self):
        # coverage_db.report_coverage(self.logger.info, bins=True)
        coverage_db.export_to_yaml("coverage.yaml")

        for name, coverpoint in coverage_db.items():
            if coverpoint.cover_percentage <= 0:
                self.logger.error(f"COVER MISS: {name} {coverpoint.cover_percentage}%")
            elif coverpoint.cover_percentage < 100:
                self.logger.warning(f"COVER GAP: {name} {coverpoint.cover_percentage}%")
            else:
                self.logger.info(f"{name} {coverpoint.cover_percentage}%")

        self.logger.info("Coverage saved to coverage.yaml")