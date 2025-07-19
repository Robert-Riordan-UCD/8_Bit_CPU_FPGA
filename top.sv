`include "src/clock.sv"
`include "src/program_counter.sv"
`include "src/memory_address_register.sv"
`include "src/register.sv"
`include "src/alu.sv"
`include "src/random_access_memory.sv"
`include "src/control.sv"

/* This module connects each of the major CPU components together
 * and provides an inteface to the FPGA IO
 */
module top (
    // Onboard IO
    input logic clk, // Internal system clock
    input logic btn1_n,
    input logic btn2_n,
    output logic [5:0] led,

    // GPIO
    input logic gpio_slide_switch, // clock mode
    input logic gpio_button // clock trigger FIXME: Needs debouncing
);
    // Internal signals
    logic cpu_clk;

    logic reset;
    assign reset = 0;

    logic clk_mode, clk_toggle;
    assign clk_mode = gpio_slide_switch;
    assign clk_toggle = gpio_button;

    tri [7:0] bus;

    logic [7:0] a_reg_value;
    logic [7:0] b_reg_value;
    logic [3:0] memory_address;
    logic [7:0] instruction;

    logic alu_carry;
    logic alu_zero;

    // Control signals
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

    // Core modules
    clock u_clock (
        .sys_clk(clk),
        .mode(clk_mode),
        .manual_toggle(clk_toggle),
        .halt(clk_halt),
        .cpu_clk(cpu_clk)
    );

    program_counter u_pc (
        .clk(cpu_clk),
        .rst(reset),
        .inc(pc_inc),
        .jump(pc_jump),
        .out(pc_out),
        .bus()
    );

    memory_address_register u_mar (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(mar_read_from_bus),
        .manual_mode(),
        .manual_read(),
        .manual_switches(),
        .bus(),
        .address(memory_address)
    );

    register u_a_reg (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(a_reg_read_from_bus),
        .write_to_bus(a_reg_write_to_bus),
        .bus(),
        .value(a_reg_value)
    );

    random_access_memory u_ram(
        .clk(cpu_clk),
        .read_from_bus(ram_read_from_bus),
        .write_to_bus(ram_write_to_bus),
        .manual_mode(),
        .manual_read(),
        .address(memory_address),
        .program_switches(),
        .bus()
    );

    alu u_alu (
        .clk(cpu_clk),
        .rst(reset),
        .a(a_reg_value),
        .b(b_reg_value),
        .out(alu_out),
        .subtract(alu_subtract),
        .flags_in(alu_flags_in),
        .bus(),
        .carry(alu_carry),
        .zero(alu_zero)
    );

    register #(8'h0F) u_i_reg (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(i_reg_read_from_bus),
        .write_to_bus(i_reg_write_to_bus),
        .bus(),
        .value(instruction)
    );
    
    register u_b_reg (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(b_reg_read_from_bus),
        .write_to_bus(b_reg_write_to_bus),
        .bus(),
        .value(b_reg_value)
    );
    
    control u_control(
        .clk(cpu_clk),
        .rst(reset),
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

    // output_module u_output();

    // FPGA IO connections
    assign led = ~{bus[3:0], 1'b0, cpu_clk};
endmodule