`define CLK_HLT   18'b000000000000000001
`define PC_OUT    18'b000000000000000010
`define PC_INC    18'b000000000000000100
`define PC_JUMP   18'b000000000000001000
`define A_READ    18'b000000000000010000
`define A_WRITE   18'b000000000000100000
`define B_READ    18'b000000000001000000
`define B_WRITE   18'b000000000010000000
`define I_READ    18'b000000000100000000
`define I_WRITE   18'b000000001000000000
`define MAR_READ  18'b000000010000000000
`define RAM_READ  18'b000000100000000000
`define RAM_WRITE 18'b000001000000000000
`define ALU_OUT   18'b000010000000000000
`define ALU_SUB   18'b000100000000000000
`define ALU_FLAGS 18'b001000000000000000
`define OUT_EN    18'b010000000000000000
`define BOOT_OUT  18'b100000000000000000

module control (
    input clk,
    input rst,

    input [3:0] instruction,

    input alu_carry,
    input alu_zero,

    input bootload_address,
    input bootload_ram,

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

    output out_en,

    output boot_write_to_bus
);

    logic [17:0] control_signals;
    assign {
        boot_write_to_bus,
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

    always_ff @(negedge clk or posedge rst) begin
        if (rst) begin
            step_counter <= 0;
        end else if (step_counter == STEP_MAX) begin
            step_counter <= 0;
        end else begin
            step_counter <= step_counter + 1;
        end
    end

    /*
        Control instructions
    */
    task automatic fetch(input [2:0] step);
        case (step)
            0: control_signals = `PC_OUT | `MAR_READ;
            1: control_signals = `RAM_WRITE | `I_READ | `PC_INC;
            default: control_signals = 0;
        endcase
    endtask

    task automatic load_a(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `RAM_WRITE | `A_READ;
            default: control_signals = 0;
        endcase
    endtask

    task automatic store_a(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `A_WRITE | `RAM_READ;
            default: control_signals = 0;
        endcase
    endtask

    task automatic load_imediate(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `A_READ;
            default: control_signals = 0;
        endcase
    endtask

    task automatic add(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `RAM_WRITE | `B_READ;
            4: control_signals = `ALU_OUT | `ALU_FLAGS | `A_READ;
            default: control_signals = 0;
        endcase
    endtask

    task automatic sub(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `MAR_READ;
            3: control_signals = `RAM_WRITE | `B_READ;
            4: control_signals = `ALU_OUT | `ALU_FLAGS | `ALU_SUB | `A_READ;
            default: control_signals = 0;
        endcase
    endtask

    task automatic jump(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `I_WRITE | `PC_JUMP;
            default: control_signals = 0;
        endcase
    endtask

    task automatic jump_carry(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = alu_carry ? (`I_WRITE | `PC_JUMP) : 'b0;
            default: control_signals = 0;
        endcase
    endtask

    task automatic jump_zero(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = alu_zero ? (`I_WRITE | `PC_JUMP) : 'b0;
            default: control_signals = 0;
        endcase
    endtask

    task automatic output_en(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `A_WRITE | `OUT_EN;
            default: control_signals = 0;
        endcase
    endtask

    task automatic halt(input [2:0] step);
        case (step)
            0: fetch(step);
            1: fetch(step);
            2: control_signals = `CLK_HLT;
            default: control_signals = 0;
        endcase
    endtask

    always_comb begin
        if (bootload_address & bootload_ram) begin
            control_signals = 0;
        end else if (bootload_address) begin
            control_signals = `BOOT_OUT | `MAR_READ;
        end else if (bootload_ram) begin
            control_signals = `BOOT_OUT | `RAM_READ;
        end else begin
            case (instruction)
                `LOAD_A:  load_a(step_counter);
                `ADD:     add(step_counter);
                `SUB:     sub(step_counter);
                `STORE_A: store_a(step_counter);
                `LOAD_IM: load_imediate(step_counter);
                `JUMP:    jump(step_counter);
                `JUMPC:   jump_carry(step_counter);
                `JUMPZ:   jump_zero(step_counter);
                `OUT:     output_en(step_counter);
                `HALT:    halt(step_counter);
                default:  fetch(step_counter);
            endcase
        end
    end

endmodule