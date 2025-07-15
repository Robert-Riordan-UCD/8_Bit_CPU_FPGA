`include "src/clock.sv"
`include "src/program_counter.sv"
`include "src/memory_address_register.sv"
`include "src/register.sv"
`include "src/alu.sv"

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

    logic pc_inc, pc_out, pc_jump;
    logic [7:0] pc_bus;
    assign pc_inc = ~btn1_n;
    assign pc_out = ~btn2_n;
    assign pc_jump = 0;

    logic [7:0] bus;
    assign bus = pc_out ? pc_bus : 8'b0;

    logic [7:0] a_reg_value;
    logic [7:0] b_reg_value;

    // Core modules
    clock u_clock (
        .sys_clk(clk),
        .mode(clk_mode),
        .manual_toggle(clk_toggle),
        .cpu_clk(cpu_clk)
    );

    program_counter u_pc (
        .clk(cpu_clk),
        .rst(reset),
        .inc(pc_inc),
        .jump(pc_jump),
        .out(pc_out),
        .bus(pc_bus)
    );

    memory_address_register u_mar (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(),
        .manual_mode(),
        .manual_read(),
        .manual_switches(),
        .bus(),
        .address()
    );

    register u_a_reg (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(),
        .write_to_bus(),
        .bus(),
        .value(a_reg_value)
    );

    // ram u_ram();

    alu u_alu (
        .clk(cpu_clk),
        .rst(reset),
        .a(a_reg_value),
        .b(b_reg_value),
        .out(),
        .subtract(),
        .flags_in(),
        .bus(),
        .carry(),
        .zero()
    );

    register #(8'h0F) u_i_reg (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(),
        .write_to_bus(),
        .bus(),
        .value()
    );
    
    register u_b_reg (
        .clk(cpu_clk),
        .rst(reset),
        .read_from_bus(),
        .write_to_bus(),
        .bus(),
        .value(b_reg_value)
    );
    
    // control u_control();
    // output_module u_output();

    // FPGA IO connections
    assign led = ~{bus[3:0], 1'b0, cpu_clk};
endmodule