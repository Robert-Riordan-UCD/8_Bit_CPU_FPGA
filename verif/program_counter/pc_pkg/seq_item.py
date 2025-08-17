from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, inc=0, jump=0, out=0, bus=0):
        super().__init__(name)
        self.rst = rst
        self.inc = inc
        self.jump = jump
        self.out = out
        self.bus = bus

    def __str__(self):
        return f"RST: {self.rst}, INC: {self.inc}, JUMP: {self.jump}, OUT: {self.out}, BUS IN: {self.bus}"