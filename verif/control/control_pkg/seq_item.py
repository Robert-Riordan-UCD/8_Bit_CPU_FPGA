from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, instruction=0, alu_carry=0, alu_zero=0, bootload_address=0, bootload_ram=0, expected_output=None):
        super().__init__(name)
        self.rst = rst
        self.instruction = instruction
        self.alu_carry = alu_carry
        self.alu_zero = alu_zero
        self.bootload_address = bootload_address
        self.bootload_ram = bootload_ram
        self.expected_output = expected_output if expected_output else list()

    def __str__(self):
        return f"RST: {self.rst}, INS: {self.instruction}, CARRY: {self.alu_carry}, ZERO: {self.alu_zero}, BOOT ADDR: {self.bootload_address}, BOOT RAM: {self.bootload_ram}"