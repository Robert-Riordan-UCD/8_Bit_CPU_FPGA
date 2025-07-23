`ifndef WAIT_TIME
`define WAIT_TIME 0
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
    Design assumptions
        4x7 seven segment display
            inputs a-h for segements/dot
            inputs 1-4 for digit
                common cathode
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

    // Convert to binary to 4 decimal digits
    // NOTE: This is inefficent but I'm going to get it working and see if I need to optimize later
    assign bcd[0] = to_display % 10;
    assign bcd[1] = (to_display / 10) % 10;
    assign bcd[2] = (to_display / 100) % 100;
    assign bcd[3] = (to_display / 1000) % 1000;

    // Convert decimal to segments
    function [7:0] bcd_to_segments(input [3:0] bcd);
        case (bcd)
            0: bcd_to_segments = `A | `B | `C | `D | `E | `F;
            1: bcd_to_segments =      `B | `C;
            2: bcd_to_segments = `A | `B      | `D | `E      | `G;
            3: bcd_to_segments = `A | `B | `C | `D           | `G;
            4: bcd_to_segments =      `B | `C           | `F | `G;
            5: bcd_to_segments = `A      | `C | `D | `E      | `G;
            6: bcd_to_segments = `A      | `C | `D | `E | `F | `G;
            7: bcd_to_segments = `A | `B | `C;
            8: bcd_to_segments = `A | `B | `C | `D | `E | `F | `G;
            9: bcd_to_segments = `A | `B | `C      | `E | `F | `G;
            default: bcd_to_segments = 8'b0;
        endcase
    endfunction

    assign all_segments[0] = bcd_to_segments(bcd[0]);
    assign all_segments[1] = bcd_to_segments(bcd[1]);
    assign all_segments[2] = bcd_to_segments(bcd[2]);
    assign all_segments[3] = bcd_to_segments(bcd[3]);

    // Mux to 7 segment diplay with sys clk
    always_ff @(posedge sys_clk or posedge rst) begin
        if (rst) begin
            digit <= 4'b0001;
            digit_counter <= 0;
        end else begin
            digit <= {digit[2:0], digit[3]};
            digit_counter <= digit_counter + 1;
        end
    end

    assign segments = all_segments[digit_counter];

endmodule