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
        // data[0] = 8'b01011000; // LOAD IM 8
        // data[1] = 8'b11100000; // OUT
        // data[2] = 8'b01010001; // LOAD IM 1
        // data[3] = 8'b11100000; // OUT
        // data[4] = 8'b01100000; // JMP 0
    
        data[0] = 8'b01010001; // LOAD IM 1
        data[1] = 8'b00101111; // ADD 15
        data[2] = 8'b11100000; // OUT
        data[3] = 8'b01100001; // JMP 1
        data[15] = 8'b00000001; // 1
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