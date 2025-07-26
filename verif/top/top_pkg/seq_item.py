from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", reset=0, clk_mode=0, clk_pulse=0, mar_address=0, ram_data=0, ram_mode=0, ram_pulse=0):
        super().__init__(name)
        self.reset = reset
        self.clk_mode = clk_mode
        self.clk_pulse = clk_pulse
        self.mar_address = mar_address
        self.ram_data = ram_data
        self.ram_mode = ram_mode
        self.ram_pulse = ram_pulse

    def __str__(self):
        return f"RESET: {self.reset}, CLK: mode={"man" if self.clk_mode == 1 else "cont"}, pulse={self.clk_pulse}, RAM: mode={"program" if self.ram_mode == 1 else  "run"}, pulse={self.ram_pulse}, addr={self.mar_address}, data={self.ram_data}"