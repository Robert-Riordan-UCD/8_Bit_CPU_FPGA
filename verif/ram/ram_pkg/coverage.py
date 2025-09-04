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
    "top.switches_in",
    xf=lambda op: op.program_switches,
    bins = [i for i in range(0x100)]
)
def point_switches_in(op): pass

@CoverPoint(
    "top.addr_read",
    xf=lambda op: op.address,
    bins = [i for i in range(0x10)]
)
def point_addr_read(op): pass

@CoverPoint(
    "top.addr_write",
    xf=lambda op: op.address,
    bins = [i for i in range(0x10)]
)
def point_addr_write(op): pass

@CoverPoint(
    "top.bus_write",
    xf=lambda op: op.ram_bus_out,
    bins = [i for i in range(0x100)]
)
def point_bus_write(op): pass

class Coverage(uvm_subscriber):
    def write(self, op):
        # Manual read
        if op.manual_read.value == 1 and op.read_from_bus.value == 0:
            point_switches_in(op)
            point_addr_read(op)

        # Bus read
        if op.manual_read.value == 0 and op.read_from_bus.value == 1:
            point_bus_in(op)
            point_addr_read(op)

        # Writes
        point_addr_write(op)
        point_bus_write(op)
        
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