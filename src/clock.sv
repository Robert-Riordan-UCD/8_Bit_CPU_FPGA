`ifndef WAIT_TIME
`define WAIT_TIME 0
`endif

module clock (
    input logic sys_clk,
    input logic mode, // 0 = cont, 1 = manual
    input logic manual_toggle,
    input logic halt,

    output logic cpu_clk
);
    logic [$clog2(`WAIT_TIME)-1:0] count;
    logic cont_clk, man_clk;

    logic [$clog2(`WAIT_TIME)-1:0] man_count_down;

    initial begin
        count <= 0;
        cont_clk <= 0;
        man_clk <= 0;
        man_count_down <= 0;
    end

    always_ff @( posedge sys_clk ) begin
        count <= count + 1;
        if (count == `WAIT_TIME) begin
            count <= 0;
            cont_clk <= ~cont_clk;
        end

        if (manual_toggle) begin
            man_count_down <= -1; // Wrap to max
        end else if (man_count_down) begin
            man_count_down <= man_count_down - 1;
        end else begin
            man_count_down <= 0;
        end
    end

    assign cpu_clk = (mode ? |man_count_down : cont_clk) & ~halt;
endmodule