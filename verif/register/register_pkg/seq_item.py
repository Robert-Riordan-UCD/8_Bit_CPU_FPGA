from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, read_from_bus=0, bus=0):
        super().__init__(name)
        self.rst = rst
        self.read_from_bus = read_from_bus
        self.bus = bus

    def __str__(self):
        return f"RST: {self.rst}, READ: {self.read_from_bus}, BUS IN: {self.bus}"