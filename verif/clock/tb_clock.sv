module tb_clock;
    
    logic sys_clk=0;
    always #1 sys_clk = ~sys_clk;

    logic mode;
    logic toggle;
    logic halt;

    logic cpu_clk;

    clock dut (
        .sys_clk(sys_clk),
        .mode(mode),
        .manual_toggle(toggle),
        .halt(halt),
        .cpu_clk(cpu_clk)
    );

endmodule