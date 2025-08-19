from pyuvm import uvm_subscriber
from cocotb.binary import BinaryValue

class Scoreboard(uvm_subscriber):
    def __init__(self, parent, name="scoreboard"):
        super().__init__(name, parent)
        self.logger.info("Init SCB")
        self.expect_boot_addr = 0
        self.expect_boot_ram = 0
        self.cycle_count = 0
        self.expected_data = [[None for i in range(17)] for j in range(4)]

        with open('bootloader_expected_data.csv', 'r') as fin:
            fin.readline()
            for line in fin:
                prog, addr, ins, data = line.split(',')
                try:
                    data = int(data)
                except ValueError:
                    data = None
                self.expected_data[int(prog)][int(addr)] = [ins.strip(), data]

    
    def write(self, op):
        self.logger.info("Write SCB")

        if op.rst == 1:
            self.cycle_count = 0
            self.expect_boot_addr = 0
            self.expect_boot_ram = 0
        
        if op.enable_bootload == 0:
            self.expect_boot_addr = 0
            self.expect_boot_ram = 0

        assert op.bootload_address == self.expect_boot_addr, f"ERROR Bootload address mismatch: Expected {self.expect_boot_addr}, Actual {op.bootload_address}"
        assert op.bootload_ram == self.expect_boot_ram, f"ERROR Bootload ram mismatch: Expected {self.expect_boot_addr}, Actual {op.bootload_address}"

        if op.bootload_address == 1:
            assert op.data == self.cycle_count//2, f"ERROR Expected address output on data: Expected {self.cycle_count//2}, Actual {op.data}"
        
        if op.bootload_ram == 1:
            op_code, data = self._get_expected_data(op.program_select, (self.cycle_count-1)/2)
            
            if not op_code == None and not data == None: # Instruction with data
                assert op_code*16 + data == op.data, f"ERROR Data mismatch: Expected {op_code*16 + data:08b}, Actual {int(op.data):08b}"
            elif not op_code == None and data == None: # Instruction without data
                assert op_code == op.data.value//16, f"ERROR Data mismatch: Expected {op_code:04b}????, Actual {int(op.data):08b}"
            elif op_code == None and not data == None: # Data
                assert data == op.data, f"ERROR Data mismatch: Expected {data:08b}, Actual {int(op.data):08b}"


        self.expect_boot_addr = (self.cycle_count+1) % 2
        self.expect_boot_ram = self.cycle_count % 2

        self.cycle_count += 1

        if self.cycle_count > 32:
            self.expect_boot_addr = 0
            self.expect_boot_ram = 0

    def _get_expected_data(self, prog, addr):
        ins = self.expected_data[int(prog)][int(addr)]
        if ins == None: return (None, None)

        op_code = None
        data = ins[1]

        match ins[0]:
            case "noop": op_code = 0
            case "load a": op_code = 1
            case "add": op_code = 2
            case "sub": op_code = 3
            case "store a": op_code = 4
            case "load im": op_code = 5
            case "jump": op_code = 6
            case "jump c": op_code = 7
            case "jump z": op_code = 8
            case "out": op_code = 14
            case "halt": op_code = 15

        return (op_code, data)

