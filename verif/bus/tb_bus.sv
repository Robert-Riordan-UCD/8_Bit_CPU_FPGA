module tb_bus;
    
    parameter LANES = 6;
    parameter WIDTH = 8;

    logic clk=0;
    always #1 clk = ~clk;

    logic [LANES-1:0] lane_select;
    logic [LANES*WIDTH-1:0] lane_data;

    logic [WIDTH-1:0] bus_data;

    bus #(
        .LANES(LANES),
        .WIDTH(WIDTH)    
    ) dut (
        .lane_select(lane_select),
        .lane_data(lane_data),
        .bus_data(bus_data)
    );

endmodule