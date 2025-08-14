module program_counter (
    input clk,
    input rst,
    
    input inc,
    input jump,

    input logic [7:0] bus_in,
    output logic [7:0] bus_out
);

    logic [3:0] count=0;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 0;
        end else if (jump && !inc) begin
            count <= bus_in;
        end else if (inc && !jump) begin
            count <= count + 1;
        end else begin
            count <= count;
        end
    end

assign bus_out = {4'b0, count};

endmodule