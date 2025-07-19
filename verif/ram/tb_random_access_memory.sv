module tb_random_access_memory;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic read_from_bus;
    logic write_to_bus;
    logic manual_mode;
    logic manual_read;

    logic [3:0] address;
    logic [7:0] program_switches;
    
    logic [7:0] bus_driver;
    tri [7:0] bus;
    assign bus = (!write_to_bus && read_from_bus) ? bus_driver : 'bz;

    random_access_memory dut (
        .clk(clk),
        .read_from_bus(read_from_bus),
        .write_to_bus(write_to_bus),
        .manual_mode(manual_mode),
        .manual_read(manual_read),
        .address(address),
        .program_switches(program_switches),
        .bus(bus)
    );

endmodule