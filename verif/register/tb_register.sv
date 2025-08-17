module tb_register;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;
    logic read_from_bus;
    
    logic [7:0] value;

    logic [7:0] bus;
    logic [7:0] reg_bus_out;

    register dut (
        .clk(clk),
        .rst(rst),
        .read_from_bus(read_from_bus),
        .bus_in(bus),
        .bus_out(reg_bus_out),
        .value(value)
    );

endmodule