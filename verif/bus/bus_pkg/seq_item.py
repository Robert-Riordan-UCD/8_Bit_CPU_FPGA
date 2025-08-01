from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", select=0, data=0, LANES=6, WIDTH=8):
        super().__init__(name)
        self.select = select
        self.data = data
        self.LANES = LANES
        self.WIDTH = WIDTH

    def __str__(self):
        return f"SELECT: {self.select:b}, DATA: 0x{self.data:x}"