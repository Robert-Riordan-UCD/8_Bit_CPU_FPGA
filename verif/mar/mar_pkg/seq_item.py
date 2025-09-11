from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, read_from_bus=0, manual_mode=0, manual_switches=0, bus=0):
        super().__init__(name)
        self.rst = rst
        self.read_from_bus = read_from_bus
        self.manual_mode = manual_mode
        self.manual_switches = manual_switches
        self.bus = 0
        self.address = None

    def __str__(self):
        return f"RST: {self.rst}, READ BUS: {self.read_from_bus}, MODE: {"MANUAL" if self.manual_mode == 1 else "BUS"}, SWITCHES: {self.manual_switches}, BUS: {self.bus}, ADDR: {self.address}"