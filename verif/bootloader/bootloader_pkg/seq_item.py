from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, program_select=0, enable_bootload=0):
        super().__init__(name)
        self.rst = rst
        self.program_select = program_select
        self.enable_bootload = enable_bootload

    def __str__(self):
        return f"RST: {self.rst}, PROG: {self.program_select}, EN: {self.enable_bootload}"