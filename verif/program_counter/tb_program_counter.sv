module tb_program_counter;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;
    logic inc;
    logic jump;
    logic out;

    logic [7:0] bus_driver;
    tri [7:0] bus;
    assign bus = (jump && !out) ? bus_driver : 'bz;

    program_counter dut (
        .clk(clk),
        .rst(rst),
        .inc(inc),
        .jump(jump),
        .out(out),
        .bus(bus)
    );

endmodule