module bus #(
    parameter WIDTH = 8,
    parameter LANES = 1
)(
    input [LANES-1:0] lane_select,
    input [LANES*WIDTH-1:0] lane_data,

    output [WIDTH-1:0] bus_data
);

    // Convert lane_seect from one-hot to binary
    logic [$clog2(LANES)-1:0] lane_select_binary;

    always_comb begin
        lane_select_binary = 'b0;
        for (integer i=0; i < LANES; i++) begin
            if (lane_select[i]) begin
                lane_select_binary = i[$clog2(LANES)-1:0];
            end
        end
    end

    // Drive output
    // data if any lane select is active otherwise 0
    assign bus_data = (|lane_select) ? lane_data[(lane_select_binary+1)*WIDTH-1 -: WIDTH] : 'b0;

endmodule
