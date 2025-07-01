module testbench ();

    logic clk, btn1_n, btn2_n;
    logic [5:0] led;

    initial begin
        clk = 0;
        forever
            #1 clk = ~clk;
    end

    top dut(
        clk,
        btn1_n,
        btn2_n,
        led
    );

    initial begin
        btn1_n = 0;
        btn2_n = 0;
        #50
        $finish;
    end

    initial begin
        $dumpvars;
        $dumpfile("dump.vcd");
    end

endmodule