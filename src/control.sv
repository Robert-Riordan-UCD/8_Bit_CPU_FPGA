module control (
    input clk,
    input rst,

    input [3:0] instruction,

    input alu_carry,
    input alu_zero,

    output clk_halt,
    
    output pc_inc,
    output pc_jump,
    output pc_out,
    
    output a_reg_read_from_bus,
    output a_reg_write_to_bus,

    output b_reg_read_from_bus,
    output b_reg_write_to_bus,

    output i_reg_read_from_bus,
    output i_reg_write_to_bus,

    output mar_read_from_bus,

    output ram_read_from_bus,
    output ram_write_to_bus,

    output alu_out,
    output alu_subtract,
    output alu_flags_in,

    output out_en
);

    localparam STEP_MAX = 6;
    logic [2:0] step_counter;

    always_ff @(negedge clk) begin
        if (rst || step_counter == STEP_MAX) begin
            step_counter <= 0;
        end else begin
            step_counter <= step_counter + 1;
        end
    end

    // Fetch Cycle
    // PC out, MAR in
    // RAM out, I in, PC inc
    assign pc_out = step_counter == 0;
    assign mar_read_from_bus = step_counter == 0;

    assign ram_write_to_bus = step_counter == 1;
    assign i_reg_read_from_bus = step_counter == 1;
    assign pc_inc = step_counter == 1;
endmodule