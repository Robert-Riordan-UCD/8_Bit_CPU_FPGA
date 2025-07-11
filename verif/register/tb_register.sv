module tb_register;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;
    logic read_from_bus;
    logic write_to_bus;
    
    logic [7:0] value;

    logic [7:0] bus_driver;
    tri [7:0] bus;
    assign bus = (!write_to_bus && read_from_bus) ? bus_driver : 'bz;

    register dut (
        .clk(clk),
        .rst(rst),
        .read_from_bus(read_from_bus),
        .write_to_bus(write_to_bus),
        .bus(bus),
        .value(value)
    );

endmodule