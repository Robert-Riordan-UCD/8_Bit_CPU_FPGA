module tb_bootloader;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;

    logic [1:0] program_select;
    logic enable_bootload;

    logic [7:0] data;
    logic bootload_address;
    logic bootload_ram;

    bootloader dut (
        .clk(clk),
        .rst(rst),
        .program_select(program_select),
        .enable_bootload(enable_bootload),
        .data(data),
        .bootload_address(bootload_address),
        .bootload_ram(bootload_ram)
    );

endmodule