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

    /* Clock */
    input logic clk_mode,
    input logic clk_pulse,
    output logic clk_output,

    /* Bus output */
    output logic [7:0] bus_output,

    /* RAM programming */
    input logic ram_mode,
    input logic ram_pulse,
    input logic [3:0] mar_switches,

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

    /* Buses */
    logic [7:0] pc_bus_out;
    logic [7:0] i_bus_out;
    
    /* Other data */
    logic [3:0] memory_address;
    logic [7:0] instruction;

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
        .program_switches(program_switches),
        .bus_in(bus_data),
        .bus_out(ram_bus_out)
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
        .out_en(out_en)
    );

    /* Bus output */
    // Pins 40, 35, 41, 42, 51, 52, 53, 54, 55 (BUS)
    // Each pin - resistor - led - VCC
    // Pin 29 - button - VCC (PC write to bus)
    // Pin 28 - button - VCC (I write to bus)
    localparam LANES = 6;
    localparam BUS_WIDTH = 8;
    logic [LANES-1:0] lane_select;
    logic [LANES*BUS_WIDTH-1:0] lane_data;

    assign lane_select = {
        1'b0,
        1'b0,
        1'b0,
        i_reg_write_to_bus,
        ram_write_to_bus,
        pc_out
    };

    assign lane_data = {
        8'b10101010,
        8'b11001100,
        8'b11100010,
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
    // assign bus_output = ~bus_data;
    assign bus_output = ~bus_data;

    /* Debug LEDs */
    // assign led = ~{ram_pulse, cpu_clk, pc_bus_out[3:0]};
    // assign led = ~{cpu_clk, pc_inc, i_reg_read_from_bus, ram_write_to_bus, mar_read_from_bus, pc_out};
    assign led = ~{lane_select};

endmodule