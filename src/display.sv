`ifndef DISPLAY_WAIT_TIME
`define DISPLAY_WAIT_TIME 0
`endif

// Segments
`define A 8'b00000001
`define B 8'b00000010
`define C 8'b00000100
`define D 8'b00001000
`define E 8'b00010000
`define F 8'b00100000
`define G 8'b01000000
`define DOT 8'b10000000

/*
    4x7 seven segment display
        inputs a-h for segements/dot
        inputs 1-4 for digit
        common anode
            active digit it high
            active segment is low
    output in hex
    only drives 2 of the digits because the max value possible with 8 bits is 0xFF
*/

module display (
    input cpu_clk,
    input sys_clk,
    input rst,
    input enable,
    input [7:0] bus,

    output [7:0] segments,
    output logic [3:0] digit
);
    logic [7:0] to_display;
    logic [3:0] bcd [4];
    logic [7:0] all_segments [4];
    logic [1:0] digit_counter;

    // Latch input
    always_ff @(posedge cpu_clk or posedge rst) begin
        if (rst) begin
            to_display <= 0;
        end else if (enable) begin
            to_display <= bus;
        end else begin
            to_display <= to_display;
        end
    end

    // Convert decimal to segments
    function [7:0] to_segments(input [3:0] bcd);
        case (bcd)
            0:  to_segments = `A | `B | `C | `D | `E | `F;
            1:  to_segments =      `B | `C;
            2:  to_segments = `A | `B      | `D | `E      | `G;
            3:  to_segments = `A | `B | `C | `D           | `G;
            4:  to_segments =      `B | `C           | `F | `G;
            5:  to_segments = `A      | `C | `D |      `F | `G;
            6:  to_segments = `A      | `C | `D | `E | `F | `G;
            7:  to_segments = `A | `B | `C;
            8:  to_segments = `A | `B | `C | `D | `E | `F | `G;
            9:  to_segments = `A | `B | `C | `D      | `F | `G;
            10: to_segments = `A | `B | `C      | `E | `F | `G; // A
            11: to_segments =           `C | `D | `E | `F | `G; // b
            12: to_segments = `A           | `D | `E | `F;      // C
            13: to_segments =      `B | `C | `D | `E      | `G; // d
            14: to_segments = `A           | `D | `E | `F | `G; // E
            15: to_segments = `A                | `E | `F | `G; // F
            default: to_segments = 8'b0;
        endcase
    endfunction

    assign all_segments[0] = to_segments(to_display & 4'hF);
    assign all_segments[1] = |(to_display>>4) ? to_segments((to_display>>4) & 4'hF) : 8'b0;
    assign all_segments[2] = 'b0;
    assign all_segments[3] = 'b0;
    
    // Mux to 7 segment diplay with sys clk
    logic [$clog2(`DISPLAY_WAIT_TIME)-1:0] count;
    logic display_clk;

    always_ff @( posedge sys_clk or posedge rst ) begin
        if (rst) begin
            count <= 0;
            display_clk <= 0;
        end else if (count == `DISPLAY_WAIT_TIME) begin
            count <= 0;
            display_clk <= ~display_clk;
        end else begin
            count <= count + 1;
            display_clk <= display_clk;
        end
    end

    always_ff @(posedge display_clk or posedge rst) begin
        if (rst) begin
            digit <= 4'b0001;
            digit_counter <= 0;
        end else begin
            digit <= {digit[2:0], digit[3]};
            digit_counter <= digit_counter + 1;
        end
    end

    assign segments = ~all_segments[digit_counter];

endmodule