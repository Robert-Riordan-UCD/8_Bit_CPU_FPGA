module random_access_memory (
    input clk,

    input read_from_bus,
    input write_to_bus,

    input manual_mode,
    input manual_read,

    input [3:0] address,

    input [7:0] program_switches,

    inout [7:0] bus
);

    logic [3:0] data [7:0];

    always_ff @(posedge clk) begin
        if (manual_mode) begin
            if (manual_read) begin
                data[address] <= program_switches;
            end
        end else begin
            if (read_from_bus && ~write_to_bus) begin
                data[address] <= bus;
            end
        end
    end

    assign bus = (write_to_bus && ~read_from_bus && ~manual_mode) ? data[address] : 8'bZ;

endmodule