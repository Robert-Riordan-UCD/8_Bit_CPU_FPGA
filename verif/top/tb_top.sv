`define WAIT_TIME 16

module tb_top;
    
    logic clk=0;
    always #1 clk = ~clk;

    /* Onboard signals */
    logic rst_n;

    /* Clock */
    logic clk_mode;
    logic clk_pulse;

    /* RAM programming */
    logic ram_mode;
    logic ram_pulse;
    logic [7:0] ram_switches;
    logic [3:0] mar_switches;

    /* Bootloader */
    logic [3:0] bootloader_program_select;
    logic enable_bootloader;

    /* Display */
    logic [3:0] digit;
    logic [7:0] segments;

    /* Debug leds */
    logic [5:0] led;

    top dut(
        .clk(clk),
        .rst_n(rst_n),
        .clk_mode(clk_mode),
        .clk_pulse(clk_pulse),
        .mar_switches(mar_switches),
        .ram_switches(ram_switches),
        .ram_mode(ram_mode),
        .ram_pulse(ram_pulse),
        .bootloader_switches(bootloader_program_select),
        .enable_bootloader(enable_bootloader),
        .digit(digit),
        .segments(segments),
        .led(led)
    );

endmodule