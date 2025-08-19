from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue
from .control_signals import Signal

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
    
    def write(self, op):
        self.logger.info("Write SCB")

        if op.rst == 1: return

        if Signal.CLK_HLT in op.expected_output: assert op.clk_halt == 1, f"ERROR: expceted HALT"
        else:                                    assert op.clk_halt == 0, f"ERROR: unexpected HALT"

        if Signal.PC_OUT in op.expected_output:  assert op.pc_out == 1, f"ERROR: expceted PC OUT"
        else:                                    assert op.pc_out == 0, f"ERROR: unexpected PC OUT"

        if Signal.PC_INC in op.expected_output:  assert op.pc_inc == 1, f"ERROR: expceted PC INC"
        else:                                    assert op.pc_inc == 0, f"ERROR: unexpected PC INC"

        if Signal.PC_JMP in op.expected_output:  assert op.pc_jump == 1, f"ERROR: expceted JUMP"
        else:                                    assert op.pc_jump == 0, f"ERROR: unexpected JUMP"

        if Signal.A_RD in op.expected_output:    assert op.a_reg_read_from_bus == 1, f"ERROR: expceted A READ"
        else:                                    assert op.a_reg_read_from_bus == 0, f"ERROR: unexpected A READ"

        if Signal.A_WRT in op.expected_output:   assert op.a_reg_write_to_bus == 1, f"ERROR: expceted A WRITE"
        else:                                    assert op.a_reg_write_to_bus == 0, f"ERROR: unexpected A WRITE"

        if Signal.B_RD in op.expected_output:    assert op.b_reg_read_from_bus == 1, f"ERROR: expceted B READ"
        else:                                    assert op.b_reg_read_from_bus == 0, f"ERROR: unexpected B READ"

        if Signal.B_WRT in op.expected_output:   assert op.b_reg_write_to_bus == 1, f"ERROR: expceted B WRITE"
        else:                                    assert op.b_reg_write_to_bus == 0, f"ERROR: unexpected B WRITE"

        if Signal.I_RD in op.expected_output:    assert op.i_reg_read_from_bus == 1, f"ERROR: expceted I READ"
        else:                                    assert op.i_reg_read_from_bus == 0, f"ERROR: unexpected I READ"

        if Signal.I_WRT in op.expected_output:   assert op.i_reg_write_to_bus == 1, f"ERROR: expceted I WRITE"
        else:                                    assert op.i_reg_write_to_bus == 0, f"ERROR: unexpected I WRITE"

        if Signal.MAR_RD in op.expected_output:  assert op.mar_read_from_bus == 1, f"ERROR: expceted MAR READ"
        else:                                    assert op.mar_read_from_bus == 0, f"ERROR: unexpected MAR READ"

        if Signal.RAM_RD in op.expected_output:  assert op.ram_read_from_bus == 1, f"ERROR: expceted RAM READ"
        else:                                    assert op.ram_read_from_bus == 0, f"ERROR: unexpected RAM READ"

        if Signal.RAM_WRT in op.expected_output: assert op.ram_write_to_bus == 1, f"ERROR: expceted RAM WRITE"
        else:                                    assert op.ram_write_to_bus == 0, f"ERROR: unexpected RAM WRITE"

        if Signal.ALU_OUT in op.expected_output: assert op.alu_out == 1, f"ERROR: expceted ALU OUT"
        else:                                    assert op.alu_out == 0, f"ERROR: unexpected ALU OUT"

        if Signal.ALU_SUB in op.expected_output: assert op.alu_subtract == 1, f"ERROR: expceted ALU SUB"
        else:                                    assert op.alu_subtract == 0, f"ERROR: unexpected ALU SUB"

        if Signal.ALU_FLG in op.expected_output: assert op.alu_flags_in == 1, f"ERROR: expceted ALU FLAGS IN"
        else:                                    assert op.alu_flags_in == 0, f"ERROR: unexpected ALU FLAGS IN"

        if Signal.OUT_EN in op.expected_output:  assert op.out_en == 1, f"ERROR: expceted OUTPUT EN"
        else:                                    assert op.out_en == 0, f"ERROR: unexpected OUTPUT EN"

        if Signal.BOOT in op.expected_output:    assert op.boot_write_to_bus == 1, f"ERROR: expceted BOOT WRITE TO BUS"
        else:                                    assert op.boot_write_to_bus == 0, f"ERROR: unexpected BOOT WRITE TO BUS"
