module memory_address_register (
    input clk,
    input rst,

    input read_from_bus,

    input manual_mode,
    input [3:0] manual_switches,

    input [3:0] bus,

    output logic [3:0] address
);
    logic [3:0] cont_addr;

    always_ff @( posedge clk or posedge rst) begin
        if (rst) begin
            cont_addr <= 0;
        end else if (!manual_mode && read_from_bus) begin
            cont_addr <= bus;
        end else begin
            cont_addr <= cont_addr;
        end
    end

    assign address = manual_mode ? manual_switches : cont_addr;
    
endmodule