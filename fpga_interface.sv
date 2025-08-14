`include "src/alu.sv"
`include "src/clock.sv"
`include "src/control.sv"
`include "src/display.sv"
`include "src/memory_address_register.sv"
`include "src/program_counter.sv"
`include "src/random_access_memory.sv"
`include "src/register.sv"
`include "src/top.sv"

module fpga_interface (
    input logic clk,

    /* Clock test */
    input logic clk_mode,
    input logic clk_pulse,
    input logic clk_halt,
    output logic clk_output,

    output logic [5:0] led
);
    assign led = ~'b0;
    
    /* Clock test */
    // Pin 69 - resistor - led - VCC
    // Pin 68 - slide switch center - VCC/GND
    // Pin 57 - button - VCC
    logic cpu_clk;

    clock u_clock (
        .sys_clk(clk),
        .mode(clk_mode),
        .manual_toggle(clk_pulse),
        .halt(clk_halt),
        .cpu_clk(cpu_clk)
    );

    assign clk_output = ~cpu_clk;

endmodule