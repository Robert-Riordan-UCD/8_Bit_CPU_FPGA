from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", read_from_bus=0, manual_mode=0, manual_read=0, address=0, program_switches=0, bus=0):
        super().__init__(name)
        self.read_from_bus = read_from_bus
        self.manual_mode = manual_mode
        self.manual_read = manual_read
        self.address = address
        self.program_switches = program_switches
        self.bus = bus

    def __str__(self):
        return f"MODE: {"manual" if self.manual_mode else "bus"}, BUS READ: {self.read_from_bus}, MANUAL READ: {self.manual_read}, ADDRESS: {self.address}, SWITCHES: {self.program_switches}, BUS IN: {self.bus}"