module tb_display;
    
    logic sys_clk=0;
    always #1 sys_clk = ~sys_clk;

    logic cpu_clk;
    logic rst;
    logic enable;
    logic [7:0] bus;

    logic [7:0] segments;
    logic [3:0] digit;

    display dut (
        .cpu_clk(cpu_clk),
        .sys_clk(sys_clk),
        .rst(rst),
        .enable(enable),
        .bus(bus),
        .segments(segments),
        .digit(digit)
    );

    clock u_clock (
        .sys_clk(sys_clk),
        .mode(1'b0),
        .manual_toggle(1'b0),
        .halt(1'b0),
        .cpu_clk(cpu_clk)
    );

endmodule