module tb_alu;
    
    logic clk=0;
    always #1 clk = ~clk;

    logic rst;
    logic out;
    logic subtract;
    logic flags_in;

    logic [7:0] a;
    logic [7:0] b;

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