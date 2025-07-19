// OP Codes
`define LOADA   4'b0001
`define ADD     4'b0010
`define SUB     4'b0011
`define STOREA  4'b0100
`define LOAD_IM 4'b0101
`define JUMP    4'b0110
`define OUT     4'b1110
`define HALT    4'b1111

`define CLK_HLT   17'b00000000000000001
`define PC_OUT    17'b00000000000000010
`define PC_INC    17'b00000000000000100
`define PC_JUMP   17'b00000000000001000
`define A_READ    17'b00000000000010000
`define A_WRITE   17'b00000000000100000
`define B_READ    17'b00000000001000000
`define B_WRITE   17'b00000000010000000
`define I_READ    17'b00000000100000000
`define I_WRITE   17'b00000001000000000
`define MAR_READ  17'b00000010000000000
`define RAM_READ  17'b00000100000000000
`define RAM_WRITE 17'b00001000000000000
`define ALU_OUT   17'b00010000000000000
`define ALU_SUB   17'b00100000000000000
`define ALU_FLAGS 17'b01000000000000000
`define OUT_EN    17'b10000000000000000

module control (
    input clk,
    input rst,

    input [3:0] instruction,

    input alu_carry,
    input alu_zero,

    output clk_halt,
    
    output pc_inc,
    output pc_jump,
    output pc_out,
    
    output a_reg_read_from_bus,
    output a_reg_write_to_bus,

    output b_reg_read_from_bus,
    output b_reg_write_to_bus,

    output i_reg_read_from_bus,
    output i_reg_write_to_bus,

    output mar_read_from_bus,

    output ram_read_from_bus,
    output ram_write_to_bus,

    output alu_out,
    output alu_subtract,
    output alu_flags_in,

    output out_en
);

    logic [16:0] control_signals;
    assign {
        out_en,
        alu_flags_in,
        alu_subtract,
        alu_out,
        ram_write_to_bus,
        ram_read_from_bus,
        mar_read_from_bus,
        i_reg_write_to_bus,
        i_reg_read_from_bus,
        b_reg_write_to_bus,
        b_reg_read_from_bus,
        a_reg_write_to_bus,
        a_reg_read_from_bus,
        pc_jump,
        pc_inc,
        pc_out,
        clk_halt
    } = control_signals;

    /*
        Micro code counter
        Counts 0 to 6 before reseting to 0
        Used to to determine which step in an instruciton is currently needed
    */
    localparam STEP_MAX = 6;
    logic [2:0] step_counter;

    always_ff @(negedge clk) begin
        if (rst || step_counter == STEP_MAX) begin
            step_counter <= 0;
        end else begin
            step_counter <= step_counter + 1;
        end
    end

    /*
        Control instructions
    */
    function fetch(input [2:0] step);
        case (step)
            0: control_signals = `PC_OUT | `MAR_READ;
            1: control_signals = `RAM_WRITE | `I_READ | `PC_INC;
            default: control_signals = 0;
        endcase
    endfunction

    function load_a(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `RAM_WRITE | `A_READ;
            default: control_signals = 0;
        endcase
    endfunction

    function store_a(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `A_WRITE | `RAM_READ;
            default: control_signals = 0;
        endcase
    endfunction

    function load_imediate(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `A_READ;
            default: control_signals = 0;
        endcase
    endfunction

    function add(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `RAM_WRITE | `B_READ;
            4: control_signals = `ALU_OUT | `ALU_FLAGS | ``A_READ;
            default: control_signals = 0;
        endcase
    endfunction

    function sub(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `RAM_WRITE | `B_READ;
            4: control_signals = `ALU_OUT | `ALU_FLAGS | `ALU_SUB | ``A_READ;
            default: control_signals = 0;
        endcase
    endfunction

    function jump(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `PC_JUMP;
            default: control_signals = 0;
        endcase
    endfunction

    function output_en(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `A_WRITE | `OUT_EN;
            default: control_signals = 0;
        endcase
    endfunction

    function halt(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `CLK_HLT;
            default: control_signals = 0;
        endcase
    endfunction

    always_comb begin
        case (instruction)
            `LOADA:   load_a(step_counter);
            `ADD:     add(step_counter);
            `SUB:     sub(step_counter);
            `STOREA:  store_a(step_counter);
            `LOAD_IM: load_imediate(step_counter);
            `JUMP:    jump(step_counter);
            `OUT:     output_en(step_counter);
            `HALT:    halt(step_counter);
            default:  fetch(step_counter);
        endcase
    end

endmodule