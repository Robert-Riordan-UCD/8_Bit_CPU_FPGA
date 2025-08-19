`include "src/cpu_pkg.sv"

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
`include "src/bootloader.sv"

module fpga_interface (
    /* Onboard signals */
    input logic clk,
    input logic rst_n,

    /* Clock */
    input logic clk_mode,
    input logic clk_pulse,
    output logic clk_output,

    /* RAM programming */
    input logic ram_mode,
    input logic ram_pulse,
    input logic [7:0] ram_switches,
    input logic [3:0] mar_switches,

    /* Display */
    output logic [3:0] digit,
    output logic [7:0] segments,

    /* Debug leds */
    output logic [5:0] led
);
    /* Reset is onboard button */
    logic rst;
    assign rst = ~rst_n;

    logic cpu_clk;

    /* Control signals */
    logic alu_carry;
    logic alu_zero;
    logic bootload_address;
    logic bootload_ram;
    logic clk_halt;
    logic pc_inc;
    logic pc_jump;
    logic pc_out;
    logic a_reg_read_from_bus;
    logic a_reg_write_to_bus;
    logic b_reg_read_from_bus;
    logic b_reg_write_to_bus;
    logic i_reg_read_from_bus;
    logic i_reg_write_to_bus;
    logic mar_read_from_bus;
    logic ram_read_from_bus;
    logic ram_write_to_bus;
    logic alu_out;
    logic alu_subtract;
    logic alu_flags_in;
    logic out_en;
    logic boot_write_to_bus;

    /* Buses */
    logic [7:0] pc_bus_out;
    logic [7:0] i_bus_out;
    logic [7:0] ram_bus_out;
    logic [7:0] a_bus_out;
    logic [7:0] b_bus_out;
    logic [7:0] alu_bus_out;
    logic [7:0] boot_bus_out;
    
    /* Other data */
    logic [3:0] memory_address;
    logic [7:0] instruction;
    logic [7:0] a_reg_value;
    logic [7:0] b_reg_value;

    /* Clock */
    // Pin 69 - resistor - led - VCC (Output)
    // Pin 68 - slide switch center - VCC/GND (Mode)
    // Pin 57 - button - VCC (Pulse)
    clock u_clock (
        .sys_clk(clk),
        .mode(clk_mode),
        .manual_toggle(clk_pulse),
        .halt(clk_halt),
        .cpu_clk(cpu_clk)
    );

    assign clk_output = ~cpu_clk;

    /* Program counter */
    program_counter u_pc (
        .clk(cpu_clk),
        .rst(rst),
        .inc(pc_inc),
        .jump(pc_jump),
        .bus_in(bus_data),
        .bus_out(pc_bus_out)
    );

    /* Memory address register */
    // Pins 28, 29, 30, 33 (MAR switches)
    memory_address_register u_mar (
        .clk(cpu_clk),
        .rst(rst),
        .read_from_bus(mar_read_from_bus),
        .manual_mode(ram_mode),
        .manual_read(ram_pulse),
        .manual_switches(mar_switches),
        .bus(bus_data[3:0]),
        .address(memory_address)
    );

    /* Random access memory */
    random_access_memory u_ram(
        .clk(cpu_clk),
        .read_from_bus(ram_read_from_bus),
        .manual_mode(ram_mode),
        .manual_read(ram_pulse),
        .address(memory_address),
        .program_switches(ram_switches),
        .bus_in(bus_data),
        .bus_out(ram_bus_out)
    );

    /* A register */
    register u_a_reg (
        .clk(cpu_clk),
        .rst(rst),
        .read_from_bus(a_reg_read_from_bus),
        .bus_in(bus_data),
        .bus_out(a_bus_out),
        .value(a_reg_value)
    );

    /* B register */
    register u_b_reg (
        .clk(cpu_clk),
        .rst(rst),
        .read_from_bus(b_reg_read_from_bus),
        .bus_in(bus_data),
        .bus_out(b_bus_out),
        .value(b_reg_value)
    );

    /* Arithmetic logic unit */
    alu u_alu (
        .clk(cpu_clk),
        .rst(rst),
        .a(a_reg_value),
        .b(b_reg_value),
        .subtract(alu_subtract),
        .flags_in(alu_flags_in),
        .bus(alu_bus_out),
        .carry(alu_carry),
        .zero(alu_zero)
    );

    /* Instruction register */
    register #(8'h0F) u_i_reg (
        .clk(cpu_clk),
        .rst(rst),
        .read_from_bus(i_reg_read_from_bus),
        .bus_in(bus_data),
        .bus_out(i_bus_out),
        .value(instruction)
    );

    /* Control */
    control u_control(
        .clk(cpu_clk),
        .rst(rst),
        .instruction(instruction[7:4]),
        .alu_carry(alu_carry),
        .alu_zero(alu_zero),
        .bootload_address(bootload_address),
        .bootload_ram(bootload_ram),
        .clk_halt(clk_halt),
        .pc_inc(pc_inc),
        .pc_jump(pc_jump),
        .pc_out(pc_out),
        .a_reg_read_from_bus(a_reg_read_from_bus),
        .a_reg_write_to_bus(a_reg_write_to_bus),
        .b_reg_read_from_bus(b_reg_read_from_bus),
        .b_reg_write_to_bus(b_reg_write_to_bus),
        .i_reg_read_from_bus(i_reg_read_from_bus),
        .i_reg_write_to_bus(i_reg_write_to_bus),
        .mar_read_from_bus(mar_read_from_bus),
        .ram_read_from_bus(ram_read_from_bus),
        .ram_write_to_bus(ram_write_to_bus),
        .alu_out(alu_out),
        .alu_subtract(alu_subtract),
        .alu_flags_in(alu_flags_in),
        .out_en(out_en),
        .boot_write_to_bus(boot_write_to_bus)
    );

    /* Display */
    // Pins 40, 35, 41, 42, 51, 52, 53, 54, 55 (Segments)
    // Pins 32, 31, 49, 48 (Digit)
    // Each pin - resistor - led - VCC
    display u_display(
        .cpu_clk(cpu_clk),
        .sys_clk(clk),
        .rst(rst),
        .enable(out_en),
        .bus(bus_data),
        .segments(segments),
        .digit(digit)
    );

    /* Bootloader */
    bootloader u_bootloader(
        .clk(cpu_clk),
        .rst(rst),
        .program_select(2'b01),
        .enable_bootload(1'b1),
        .data(boot_bus_out),
        .bootload_address(bootload_address),
        .bootload_ram(bootload_ram)
    );

    /* Bus */
    localparam LANES = 7;
    localparam BUS_WIDTH = 8;
    logic [LANES-1:0] lane_select;
    logic [LANES*BUS_WIDTH-1:0] lane_data;

    assign lane_select = {
        boot_write_to_bus,
        alu_out,
        b_reg_write_to_bus,
        a_reg_write_to_bus,
        i_reg_write_to_bus,
        ram_write_to_bus,
        pc_out
    };

    assign lane_data = {
        boot_bus_out,
        alu_bus_out,
        b_bus_out,
        a_bus_out,
        i_bus_out,
        ram_bus_out,
        pc_bus_out
    };

    bus #(
        .WIDTH(BUS_WIDTH),
        .LANES(LANES)
    ) u_bus (
        .lane_select(lane_select),
        .lane_data(lane_data),
        .bus_data(bus_data)
    );

    logic [7:0] bus_data;

    /* Debug LEDs */
    assign led = ~{clk_halt, alu_zero, alu_carry, alu_flags_in, ram_read_from_bus, a_reg_write_to_bus};

endmodule