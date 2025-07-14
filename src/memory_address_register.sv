module memory_address_register (
    input clk,
    input rst,

    input read_from_bus,

    input manual_mode,
    input manual_read,
    input [3:0] manual_switches,

    input [3:0] bus,

    output logic [3:0] address
);

    always_ff @( posedge clk or posedge rst or posedge manual_read) begin
        if (rst) begin
            address <= 0;
        end else if manual_read begin
            if manual_mode begin
                address <= manual_switches;
            end else begin
                address <= address;
            end
        end else if (read_from_bus && !manual_mode) begin
            address <= bus;
        end else begin
            address <= address;
        end
    end
    
endmodule