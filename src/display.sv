`ifndef WAIT_TIME
`define WAIT_TIME 0
`endif

module display (
    input cpu_clk,
    input sys_clk,
    input rst,
    input enable,
    input [7:0] bus
);

    // Latch input
    // Convert to BCD
    // Mux to 7 segment diplay with sys clk

endmodule