`include "src/alu.sv"
`include "src/bus.sv"
`include "src/clock.sv"
`include "src/control.sv"
`include "src/display.sv"
`include "src/memory_address_register.sv"
`include "src/program_counter.sv"
`include "src/random_access_memory.sv"
`include "src/register.sv"
`include "src/top.sv"

module fpga_interface (
    /* Onboard signals */
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
    /* I register */
    input i_read_from_bus,

    /* Bus output */
    input logic pc_out,
    input logic i_write_to_bus,
    output logic [7:0] bus_output,

    output logic [5:0] led
);
    /* Debug LEDs */
    assign led = ~{pc_out, cpu_clk, pc_bus_out[3:0]};
    
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

    /* Program counter test */
    // Pin 34 - button - VCC (INC)
    // Pin 33 - button - VCC (JMP)
    logic [7:0] pc_bus_out;
    program_counter u_pc (
        .clk(cpu_clk),
        .rst(rst),
        .inc(pc_inc),
        .jump(pc_jump),
        .bus_in(bus_out),
        .bus_out(pc_bus_out)
    );

    /* Instruction register test */
    // Pin 30 - button - VCC (READ)
    logic [7:0] i_bus_out;
    logic [7:0] instruction;
    register #(8'h0F) u_i_reg (
        .clk(cpu_clk),
        .rst(rst),
        .read_from_bus(i_read_from_bus),
        .bus_in(bus_out),
        .bus_out(i_bus_out),
        .value(instruction)
    );

    /* Bus output test */
    // Pins 40, 35, 41, 42, 51, 52, 53, 54, 55 (BUS)
    // Each pin - resistor - led - VCC
    // Pin 29 - button - VCC (PC write to bus)
    // Pin 28 - button - VCC (I write to bus)
    bus #(
        .WIDTH(8),
        .LANES(2)
    ) u_bus (
        .lane_select({
            pc_out,
            i_write_to_bus
        }),
        .lane_data({
            pc_bus_out,
            i_bus_out
        }),
        .bus_data(bus_out)
    );

    logic [7:0] bus_out;
    assign bus_output = ~bus_out;

endmodule