/*
    Populate ram with a program on reset
    Write an address followed by the data for each location in ram according to the selected program
*/

`define NUM_PROGRAMS 4

module bootloader (
    input clk,
    input rst,
    input [$clog2(`NUM_PROGRAMS)-1:0] program_select,
    input enable_bootload,

    output logic [7:0] data,
    output logic bootload_address,
    output logic bootload_ram
);
    logic addr_or_ram=0;
    logic [3:0] addr=0;
    logic complete=0;

    logic [5:0] counter;
    always_comb begin
        {complete, addr, addr_or_ram} = counter;        
    end

    logic [7:0] programs [`NUM_PROGRAMS][16];

    initial begin
        /* Initialize to 0 */
        integer prog;
        integer addr;
        for (prog = 0; prog < `NUM_PROGRAMS; prog = prog + 1) begin
            for (addr = 0; addr < 16; addr = addr + 1) begin
                programs[prog][addr] = {`NOOP, 4'b0000};
            end
		end

        /* Count in 1s */
        // Program
        programs[0][0] = {`LOAD_IM, 4'b0000};
        programs[0][1] = {`ADD,     4'b1111};
        programs[0][2] = {`OUT,     4'b0000};
        programs[0][3] = {`JUMP,    4'b0001};
        // Data
        programs[0][15] =    {8'b00000001};

        /* Fibonacci */
        // Program
        programs[1][0] = {`LOAD_IM, 4'b0000};
        programs[1][1] = {`ADD,     4'b1111};
        programs[1][2] = {`JUMPC,   4'b1010};
        programs[1][3] = {`OUT,     4'b0000};
        programs[1][4] = {`STORE_A, 4'b1101};
        programs[1][5] = {`LOAD_A,  4'b1110};
        programs[1][6] = {`STORE_A, 4'b1111};
        programs[1][7] = {`LOAD_A,  4'b1101};
        programs[1][8] = {`STORE_A, 4'b1110};
        programs[1][9] = {`JUMP,    4'b0001};
        programs[1][10]= {`HALT,    4'b0000};
        // Data
        programs[1][14] = {8'b00000001};
        programs[1][15] = {8'b00000000};
    end

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            counter <= 0;
        end else if (~complete) begin
            counter <= counter+1;
        end else begin
            counter <= counter;
        end
    end

    always_comb begin
        if (enable_bootload & ~complete & ~rst) begin
            bootload_address = ~addr_or_ram;
            bootload_ram = addr_or_ram; 
        end else begin
            bootload_address = 0;
            bootload_ram = 0;
        end
    end
    
    always_comb begin
        if (bootload_address & ~bootload_ram) begin
            data = addr;
        end else if (~bootload_address & bootload_ram) begin
            data = programs[program_select][addr];
        end else begin
            data = 'b0;
        end
    end
    
endmodule

 /* Alternate between 8 and 1 */
        // data[0] = 8'b01011000; // LOAD IM 8
        // data[1] = 8'b11100000; // OUT
        // data[2] = 8'b01010001; // LOAD IM 1
        // data[3] = 8'b11100000; // OUT
        
        // data[4] = 8'b01100000; // JMP 0
    
        // /* Multiply 6 by 11 */
        // data[0] = {`LOADA,  4'd15};
        // data[1] = {`STORE_A, 4'd13};
        
        // data[2] = {`LOADA,  4'd13};
        // data[3] = {`OUT,    4'b0};
        // data[4] = {`ADD,    4'd15};
        // data[5] = {`STORE_A, 4'd13};
        
        // data[6] = {`LOADA,  4'd14};
        // data[7] = {`SUB,    4'd12};
        // data[8] = {`JUMPZ,  4'd11};
        
        // data[9] = {`STORE_A, 4'd14};
        // data[10] = {`JUMP,  4'd2};
        
        // data[11] = {`HALT,  4'b0};
        
        // data[12] = 8'b1; // 1
        // data[13] = 8'b0; // SUM
        // data[14] = 8'd11; // B
        // data[15] = 8'd6; // A

