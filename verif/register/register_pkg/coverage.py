"""
    Coverage Goals
"""

from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from cocotb_coverage.coverage import  CoverPoint, coverage_db

@CoverPoint(
    "top.bus_in",
    xf=lambda op: op.bus,
    bins = [i for i in range(0x100)]
)
def point_bus_in(op): pass

@CoverPoint(
    "top.value",
    xf=lambda op: op.value,
    bins = [i for i in range(0x100)]
)
def point_value(op): pass

@CoverPoint(
    "top.bus_out",
    xf=lambda op: op.reg_bus_out,
    bins = [i for i in range(0x100)]
)
def point_bus_out(op): pass

class Coverage(uvm_subscriber):
    def write(self, op):
        if op.read_from_bus.value == 1:
            point_bus_in(op)
        
        point_value(op)
        point_bus_out(op)
        
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