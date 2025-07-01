module testbench ();

    logic clk, btn1_n, btn2_n, slide_switch;
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
        led,
        slide_switch
    );

    initial begin
        btn1_n = 0;
        btn2_n = 0;
        slide_switch = 0;
        #50
        $finish;
    end

    initial begin
        $dumpvars;
        $dumpfile("dump.vcd");
    end

endmodule