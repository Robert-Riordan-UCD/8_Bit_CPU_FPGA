`define WAIT_TIME 16

module tb_top;
    
    logic sys_clk=0;
    always #1 sys_clk = ~sys_clk;

    logic reset=0;
    logic clk_mode=0;
    logic clk_pulse=0;

    logic [3:0] mar_address=0;
    logic [7:0] ram_data=0;
    logic ram_mode=0;
    logic ram_pulse=0;

    logic [3:0] digit;
    logic [7:0] segments;

    top dut(
        .sys_clk(sys_clk),
        .reset(reset),
        .clk_mode(clk_mode),
        .clk_pulse(clk_pulse),
        .mar_address(mar_address),
        .ram_data(ram_data),
        .ram_mode(ram_mode),
        .ram_pulse(ram_pulse),
        .digit(digit),
        .segments(segments)
    );

endmodule