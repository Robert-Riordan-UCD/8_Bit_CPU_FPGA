`ifndef WAIT_TIME
`define WAIT_TIME 1
`endif

module clock (
    input logic sys_clk,
    input logic mode, // 0 = cont, 1 = manual
    input logic button,

    output logic cpu_clk
);
    logic [23:0] count;
    logic cont_clk, man_clk;

    initial begin
        count <= 0;
        cont_clk <= 0;
        man_clk <= 0;
    end

    always_ff @( posedge sys_clk ) begin
        count <= count + 1;
        if (count == `WAIT_TIME) begin
            count <= 0;
            cont_clk <= ~cont_clk;
        end
    end

    always_ff @( posedge button ) begin
        man_clk <= ~man_clk;
    end

    assign cpu_clk = mode ? man_clk : cont_clk;
endmodule