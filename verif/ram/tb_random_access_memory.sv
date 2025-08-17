module tb_random_access_memory;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic read_from_bus;
    logic manual_mode;
    logic manual_read;

    logic [3:0] address;
    logic [7:0] program_switches;
    
    logic [7:0] bus;
    logic [7:0] ram_bus_out;

    random_access_memory dut (
        .clk(clk),
        .read_from_bus(read_from_bus),
        .manual_mode(manual_mode),
        .manual_read(manual_read),
        .address(address),
        .program_switches(program_switches),
        .bus_in(bus),
        .bus_out(ram_bus_out)
    );

endmodule