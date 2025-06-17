`include "src/clock.sv"

module top (
    input logic clk,
    input logic key_i,
    input logic rst_i,
    output logic [5:0] led
);

    logic cpu_clk;

    logic mode, button;
    assign mode = ~key_i;
    assign button = ~rst_i;

    clock u_clock (
        .sys_clk(clk),
        .mode(mode),
        .button(button),
        .cpu_clk(cpu_clk)
    );

    assign led = ~{5'b0, cpu_clk};
endmodule