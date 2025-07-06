module tb_program_counter;
    
    logic clk;
    always #1 clk = ~clk;

    logic rst;
    logic inc;
    logic jump;
    logic out;

    logic [7:0] bus_driver;
    tri [7:0] bus;
    assign bus = (!out || jump) ? bus_driver : 'bz;

    program_counter dut (
        .clk(clk),
        .rst(rst),
        .inc(inc),
        .jump(jump),
        .out(out),
        .bus(bus)
    );

endmodule