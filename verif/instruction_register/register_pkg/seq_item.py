from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    def __init__(self, name="seq_item", rst=0, read_from_bus=0, write_to_bus=0, bus_driver=0):
        super().__init__(name)
        self.rst = rst
        self.read_from_bus = read_from_bus
        self.write_to_bus = write_to_bus
        self.bus_driver = bus_driver

    def __str__(self):
        return f"RST: {self.rst}, READ: {self.read_from_bus}, WRITE: {self.write_to_bus}, BUS DRIVER: {self.bus_driver}"