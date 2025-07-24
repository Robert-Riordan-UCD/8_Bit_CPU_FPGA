from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", mode=0, toggle=0, halt=0):
        super().__init__(name)
        self.mode = mode
        self.toggle = toggle
        self.halt = halt

    def __str__(self):
        return f"MODE: {"manual" if self.mode.value == 1 else "continious"}, TOGGLE: {self.toggle}, HALT: {self.halt}"