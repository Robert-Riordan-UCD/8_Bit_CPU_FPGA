module alu (
    input clk,
    input rst,

    input [7:0] a,
    input [7:0] b,

    input subtract,
    input flags_in,

    output [7:0] bus,
    output logic carry,
    output logic zero
);

    logic [8:0] sum; // Extra bit for carry detection
    assign sum = subtract ? a - b : a + b;
    assign bus = sum[7:0];

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            carry <= 0;
            zero <= 0;
        end else if (flags_in) begin
            carry <= sum[8];
            zero <= !(|sum[7:0]);
        end else begin
            carry <= carry;
            zero <= zero;
        end
    end

endmodule