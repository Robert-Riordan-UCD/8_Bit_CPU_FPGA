module tb_alu;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst=0;
    logic out=0;
    logic subtract=0;
    logic flags_in=0;

    logic [7:0] a=0;
    logic [7:0] b=0;

    logic [7:0] bus;
    logic carry;
    logic zero;

    alu dut (
        .clk(clk),
        .rst(rst),
        .out(out),
        .subtract(subtract),
        .flags_in(flags_in),
        .carry(carry),
        .zero(zero),
        .a(a),
        .b(b),
        .bus(bus)
    );

endmodule