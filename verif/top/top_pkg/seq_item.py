from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst_n=1, clk_mode=0, clk_pulse=0, mar_switches=0, ram_switches=0, ram_mode=0, ram_pulse=0, bootloader_program_select=0, enable_bootloader=0):
        super().__init__(name)
        self.rst_n = rst_n
        self.clk_mode = clk_mode
        self.clk_pulse = clk_pulse
        self.mar_switches = mar_switches
        self.ram_switches = ram_switches
        self.ram_mode = ram_mode
        self.ram_pulse = ram_pulse
        self.bootloader_program_select = bootloader_program_select
        self.enable_bootloader = enable_bootloader

    def __str__(self):
        return f"RESET: {not self.rst_n}, CLK: mode={"man" if self.clk_mode == 1 else "cont"}, pulse={self.clk_pulse}, RAM: mode={"program" if self.ram_mode == 1 else  "run"}, pulse={self.ram_pulse}, addr={self.mar_switches}, data={self.ram_switches}, BOOT: en={self.enable_bootloader}, addr={self.bootloader_program_select}"