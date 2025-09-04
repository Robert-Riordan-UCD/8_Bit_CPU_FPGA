"""
    Coverage Goals
    All valid sements hit
    All valid digits hit
    All bus values in
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from cocotb_coverage.coverage import  CoverPoint, coverage_db
from .segments import Segments

@CoverPoint(
    "top.bus_in",
    xf=lambda op: op.bus,
    bins = [i for i in range(0x100)]
)
def point_bus_in(op): pass

@CoverPoint(
    "top.digit",
    xf=lambda op: op.digit,
    bins = [2**(i) for i in range(4)]
)
def point_digit(op): pass

@CoverPoint(
    "top.segments",
    xf=lambda op: op.segments,
    bins = [s for s in Segments]
)
def point_segments(op): pass

class Coverage(uvm_subscriber):
    def write(self, op):
        if op.enable == 1 and op.cpu_clk == 1 and op.rst == 0:
            point_bus_in(op)
        
        point_digit(op)
        point_segments(op)
        
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
