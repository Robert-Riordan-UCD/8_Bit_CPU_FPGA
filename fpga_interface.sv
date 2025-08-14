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
    input logic rst_n,

    /* Clock test */
    input logic clk_mode,
    input logic clk_pulse,
    input logic clk_halt,
    output logic clk_output,

    /* Program counter test */
    input logic pc_inc,
    input logic pc_jump,
    output logic [7:0] bus_output,

    output logic [5:0] led
);
    /* Debug LEDs */
    assign led = ~{1'b0, cpu_clk, ~bus_output[3:0]};
    
    /* Reset is onboard button */
    logic rst;
    assign rst = ~rst_n;

    /* Clock test */
    // Pin 69 - resistor - led - VCC (Output)
    // Pin 68 - slide switch center - VCC/GND (Mode)
    // Pin 57 - button - VCC (Pulse)
    // Pin 56 - button - VCC (Halt)
    logic cpu_clk;

    clock u_clock (
        .sys_clk(clk),
        .mode(clk_mode),
        .manual_toggle(clk_pulse),
        .halt(clk_halt),
        .cpu_clk(cpu_clk)
    );

    assign clk_output = ~cpu_clk;

    /* Program Counter test */
    // Pin 34 - button - VCC (INC)
    // Pin 33 - button - VCC (JMP)
    logic [7:0] pc_out;
    program_counter u_pc (
        .clk(cpu_clk),
        .rst(rst),
        .inc(pc_inc),
        .jump(pc_jump),
        .bus_in(8'b10101010),
        .bus_out(pc_out)
    );

    /* Bus output test */
    // Pins 40, 35, 41, 42, 51, 52, 53, 54, 55
    // Each pin - resistor - led - VCC
    assign bus_output = ~pc_out;

endmodule