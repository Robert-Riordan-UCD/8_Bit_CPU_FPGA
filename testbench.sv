module testbench ();

    logic clk, key_i, rst_i;
    logic [5:0] led;

    initial begin
        clk = 0;
        forever
            #5 clk = ~clk;
    end

    top dut(
        clk,
        key_i, //mode
        rst_i,  //btn
        led
    );

    initial begin
        key_i = 0;
        rst_i = 0;
        #40
        key_i = 1;
        #40
        rst_i = 1;
        #40
        key_i = 0;
        rst_i = 0;
        #500
        $finish;
    end

    initial begin
        $dumpvars;
        $dumpfile("dump.vcd");
    end

endmodule