module program_counter (
    input clk,
    input rst,
    
    input inc,
    input jump,
    input out,

    inout [7:0] bus
);

    logic [3:0] count;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 0;
        end else if (jump && !inc) begin
            count <= bus;
        end else if (inc && !jump) begin
            count <= count + 1;
        end else begin
            count <= count;
        end
    end

    assign bus = out ? count : 8'bZ;

endmodule