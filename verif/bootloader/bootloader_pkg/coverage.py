from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
from cocotb_coverage.coverage import  CoverPoint, CoverCross, coverage_db

@CoverPoint(
    "top.select",
    xf=lambda op: op.program_select,
    bins = [i for i in range(4)]
)
def point_select(op): pass

@CoverPoint(
    "top.enable",
    xf=lambda op: op.enable_bootload,
    bins = [0, 1]
)
def point_enable(op): pass

@CoverPoint(
    "top.boot_addr",
    xf=lambda op: op.bootload_address,
    bins = [0, 1]
)
def point_boot_addr(op): pass

@CoverPoint(
    "top.boot_data",
    xf=lambda op: op.bootload_ram,
    bins = [0, 1]
)
def point_boot_data(op): pass

@CoverCross(
    "top.cross_enable_select",
    items=["top.enable", "top.select"]
)
def cross_enable_select(op): pass

class Coverage(uvm_subscriber):
    def write(self, op):
        if op.rst.value == 0:
            point_enable(op)
            point_select(op)
            point_boot_addr(op)
            point_boot_data(op)
            cross_enable_select(op)

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