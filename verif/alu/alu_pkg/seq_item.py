from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item"):
        super().__init__(name)
        #  Input
        self.rst = 0
        self.a = 0
        self.b = 0
        self.out = 0
        self.subtract = 0
        self.flags_in = 0
        # Expected output
        self.expected_bus = 0
        self.expected_carry = 0
        self.expected_zero = 0

    def __str__(self):
        return f"A: 0x{self.a:02x}, B: {self.b:02x}, OUT: {self.out}, SUBTRACT: {self.subtract}, FLAGS: {self.flags_in}"