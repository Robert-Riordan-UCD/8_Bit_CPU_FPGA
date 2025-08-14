module register #(
    parameter BUS_OUTPUT_MASK = 8'hFF
)(
    input clk,
    input rst,

    input read_from_bus,

    input [7:0] bus_in,
    output [7:0] bus_out,
    output logic [7:0] value
);

    always_ff @( posedge clk or posedge rst ) begin
        if (rst) begin
            value <= 0;
        end else if (read_from_bus) begin
            value <= bus_in;
        end else begin
            value <= value;
        end
    end

    assign bus_out = BUS_OUTPUT_MASK & value;

endmodule