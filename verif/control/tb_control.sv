module tb_control;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;

    logic [3:0] instruction;
    logic alu_carry;
    logic alu_zero;

    logic clk_halt;
    logic pc_inc;
    logic pc_jump;
    logic pc_out;
    logic a_reg_read_from_bus;
    logic a_reg_write_to_bus;
    logic b_reg_read_from_bus;
    logic b_reg_write_to_bus;
    logic i_reg_read_from_bus;
    logic i_reg_write_to_bus;
    logic mar_read_from_bus;
    logic ram_read_from_bus;
    logic ram_write_to_bus;
    logic alu_out;
    logic alu_subtract;
    logic alu_flags_in;
    logic out_en;

    control dut (
        .clk(clk),
        .rst(rst),
        .instruction(instruction),
        .alu_carry(alu_carry),
        .alu_zero(alu_zero),
        .clk_halt(clk_halt),
        .pc_inc(pc_inc),
        .pc_jump(pc_jump),
        .pc_out(pc_out),
        .a_reg_read_from_bus(a_reg_read_from_bus),
        .a_reg_write_to_bus(a_reg_write_to_bus),
        .b_reg_read_from_bus(b_reg_read_from_bus),
        .b_reg_write_to_bus(b_reg_write_to_bus),
        .i_reg_read_from_bus(i_reg_read_from_bus),
        .i_reg_write_to_bus(i_reg_write_to_bus),
        .mar_read_from_bus(mar_read_from_bus),
        .ram_read_from_bus(ram_read_from_bus),
        .ram_write_to_bus(ram_write_to_bus),
        .alu_out(alu_out),
        .alu_subtract(alu_subtract),
        .alu_flags_in(alu_flags_in),
        .out_en(out_en)
    );

endmodule