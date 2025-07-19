from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, instruction=0, alu_carry=0, alu_zero=0):
        super().__init__(name)
        self.rst = rst
        self.instructions = instruction
        self.alu_carry = alu_carry
        self.alu_zero = alu_zero

    def __str__(self):
        return f"RST: {self.rst}, INS: {self.instruction}, CARRY: {self.alu_carry}, ZERO: {self.alu_zero}"