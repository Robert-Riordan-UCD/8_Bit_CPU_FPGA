from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, a=0, b=0, out=0, subtract=0, flags_in=0):
        super().__init__(name)
        #  Input
        self.rst = rst
        self.a = a
        self.b = b
        self.out = out
        self.subtract = subtract
        self.flags_in = flags_in

    def __str__(self):
        return f"A: 0x{self.a:02x}, B: {self.b:02x}, OUT: {self.out}, SUBTRACT: {self.subtract}, FLAGS: {self.flags_in}"