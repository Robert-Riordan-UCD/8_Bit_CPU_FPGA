`define LOADA   4'b0001
`define ADD     4'b0010
`define SUB     4'b0011
`define STOREA  4'b0100
`define LOAD_IM 4'b0101
`define JUMP    4'b0110
`define JUMPC   4'b0111
`define JUMPZ   4'b1000
`define OUT     4'b1110
`define HALT    4'b1111

module random_access_memory (
    input clk,

    input read_from_bus,

    input manual_mode,
    input manual_read,

    input [3:0] address,

    input [7:0] program_switches,

    input [7:0] bus_in,
    output [7:0] bus_out
);

    logic [7:0] data [16];

    initial begin        
        /* Alternate between 8 and 1 */
        // data[0] = 8'b01011000; // LOAD IM 8
        // data[1] = 8'b11100000; // OUT
        // data[2] = 8'b01010001; // LOAD IM 1
        // data[3] = 8'b11100000; // OUT
        
        // data[4] = 8'b01100000; // JMP 0
    
        /* Add 1 */
        // data[0] = 8'b01010001; // LOAD IM 1
        // data[1] = 8'b00101111; // ADD 15
        // data[2] = 8'b11100000; // OUT
        // data[3] = 8'b01100001; // JMP 1
        
        // data[15] = 8'b00000001; // 1

        /* Fibonacci */
        // data[0] = 8'b01010000; // LOAD IM 0
        // data[1] = 8'b00101111; // ADD 15

        // data[2] = 8'b01111100; // JMPC 12

        // data[3] = 8'b11100000; // OUT

        // data[4] = 8'b01001101; // STORE A 13
        // data[5] = 8'b00011110; // LOAD A 14
        // data[6] = 8'b01001111; // STORE A 15
        // data[7] = 8'b00011101; // LOAD A 13
        // data[8] = 8'b01001110; // STORE A 14
        
        // data[9] = 8'b01100001; // JMP 1

        // data[12] = 8'b11110000; // HALT
        
        // data[14] = 8'b00000001; // 1
        // data[15] = 8'b00000001; // 0

        /* Multiply 6 by 11 */
        data[0] = {`LOADA,  4'd15};
        data[1] = {`STOREA, 4'd13};
        
        data[2] = {`LOADA,  4'd13};
        data[3] = {`OUT,    4'b0};
        data[4] = {`ADD,    4'd15};
        data[5] = {`STOREA, 4'd13};
        
        data[6] = {`LOADA,  4'd14};
        data[7] = {`SUB,    4'd12};
        data[8] = {`JUMPZ,  4'd11};
        
        data[9] = {`STOREA, 4'd14};
        data[10] = {`JUMP,  4'd2};
        
        data[11] = {`HALT,  4'b0};
        
        data[12] = 8'b1; // 1
        data[13] = 8'b0; // SUM
        data[14] = 8'd11; // B
        data[15] = 8'd6; // A
    end

    always_ff @(posedge clk) begin
        if (manual_mode) begin
            if (manual_read) begin
                data[address] <= program_switches;
            end
        end else begin
            if (read_from_bus) begin
                data[address] <= bus_in;
            end
        end
    end

    assign bus_out = data[address];

endmodule