from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, enable=0, bus=0):
        super().__init__(name)
        self.rst = rst
        self.enable = enable
        self.bus = bus

    def __str__(self):
        return f"RST: {self.rst}, EN: {self.enable}, BUS: {self.bus}"