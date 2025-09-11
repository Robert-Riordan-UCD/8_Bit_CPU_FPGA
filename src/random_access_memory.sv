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

    always_ff @(posedge clk) begin
        if (manual_mode) begin
            if (manual_read) begin
                data[address] <= manual_data;
            end
        end else begin
            if (read_from_bus) begin
                data[address] <= bus_in;
            end
        end
    end

    logic [7:0] manual_data;
    always_ff @(posedge manual_read) begin
        manual_data <= program_switches;
    end

    assign bus_out = data[address];

endmodule