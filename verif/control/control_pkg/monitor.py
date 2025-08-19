from pyuvm import uvm_monitor, uvm_analysis_port
import cocotb
from .seq_item import SeqItem

class Monitor(uvm_monitor):
    def __init__(self, parent, name="monitor"):
        super().__init__(name, parent)
        self.logger.info("Init MON")
        self.dut = None
        self.analysis_port = uvm_analysis_port("ap", self)
        self.expected_output = None

    def build_phase(self):
        self.logger.info("Build MON")
        self.dut = cocotb.top
    
    async def run_phase(self):
        self.logger.info("Run MON")
        while True:
            # self.logger.info("Run MON: Wait for CLK")
            await cocotb.triggers.RisingEdge(self.dut.clk)

            op = SeqItem()
            op.rst = self.dut.rst
            op.instruction = self.dut.instruction
            op.alu_carry = self.dut.alu_carry
            op.alu_zero = self.dut.alu_zero
            op.bootload_address = self.dut.bootload_address
            op.bootload_ram = self.dut.bootload_ram
            
            op.clk_halt = self.dut.clk_halt
            op.pc_inc = self.dut.pc_inc
            op.pc_jump = self.dut.pc_jump
            op.pc_out = self.dut.pc_out
            op.a_reg_read_from_bus = self.dut.a_reg_read_from_bus
            op.a_reg_write_to_bus = self.dut.a_reg_write_to_bus
            op.b_reg_read_from_bus = self.dut.b_reg_read_from_bus
            op.b_reg_write_to_bus = self.dut.b_reg_write_to_bus
            op.i_reg_read_from_bus = self.dut.i_reg_read_from_bus
            op.i_reg_write_to_bus = self.dut.i_reg_write_to_bus
            op.mar_read_from_bus = self.dut.mar_read_from_bus
            op.ram_read_from_bus = self.dut.ram_read_from_bus
            op.ram_write_to_bus = self.dut.ram_write_to_bus
            op.alu_out = self.dut.alu_out
            op.alu_subtract = self.dut.alu_subtract
            op.alu_flags_in = self.dut.alu_flags_in
            op.out_en = self.dut.out_en
            op.boot_write_to_bus = self.dut.boot_write_to_bus
            
            op.expected_output = self.expected_output

            self.analysis_port.write(op)
            # self.logger.info("Run MON: Cycle monitored")