module tb_memory_address_register;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;
    logic read_from_bus;
    
    logic manual_mode;

    logic [3:0] manual_switches;
    logic [3:0] bus;
    
    logic [3:0] address;

    memory_address_register dut (
        .clk(clk),
        .rst(rst),
        .read_from_bus(read_from_bus),
        .manual_mode(manual_mode),
        .manual_switches(manual_switches),
        .bus(bus),
        .address(address)
    );

endmodule