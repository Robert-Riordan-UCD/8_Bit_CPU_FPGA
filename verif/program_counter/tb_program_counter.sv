module tb_program_counter;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;
    logic inc;
    logic jump;
    logic out;

    logic [7:0] bus;
    logic [7:0] pc_out;

    program_counter dut (
        .clk(clk),
        .rst(rst),
        .inc(inc),
        .jump(jump),
        .bus_in(bus),
        .bus_out(pc_out)
    );

endmodule