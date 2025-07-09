module register (
    input clk,
    input rst,

    input read_from_bus,
    input write_to_bus,

    inout [7:0] bus,
    output logic [7:0] value
);

    always_ff @( posedge clk or posedge rst ) begin
        if (rst) begin
            value <= 0;
        end else if (read_from_bus) begin
            value <= bus;
        end else begin
            value <= value;
        end
    end

    assign bus = (write_to_bus && !read_from_bus) ? value : 'bz;

endmodule