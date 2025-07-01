`include "src/clock.sv"
`include "src/program_counter.sv"

/* This module connects each of the major CPU components together
 * and provides an inteface to the FPGA IO
 */
module top (
    // Onboard IO
    input logic clk,
    input logic btn1_n,
    input logic btn2_n,
    output logic [5:0] led

    // GPIO
);
    // Internal signals
    logic cpu_clk;

    logic reset;
    assign reset = 0;

    logic clk_mode, clk_toggle;
    assign clk_mode = 0;
    assign clk_toggle = 0;

    logic pc_inc, pc_out, pc_jump;
    logic [7:0] pc_bus;
    assign pc_inc = ~btn1_n;
    assign pc_out = ~btn2_n;
    assign pc_jump = 0;

    logic [7:0] bus;
    assign bus = pc_out ? pc_bus : 8'b0;

    // Core modules
    clock u_clock (
        .sys_clk(clk),
        .mode(clk_mode),
        .manual_toggle(clk_toggle),
        .cpu_clk(cpu_clk)
    );

    program_counter u_pc(
        .clk(cpu_clk),
        .rst(reset),
        .inc(pc_inc),
        .jump(pc_jump),
        .out(pc_out),
        .bus(pc_bus)
    );

    // FPGA IO connections
    assign led = ~{bus[3:0], 1'b0, cpu_clk};
endmodule