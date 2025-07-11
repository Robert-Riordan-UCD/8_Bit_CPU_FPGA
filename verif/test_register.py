# import cocotb
# from cocotb.triggers import RisingEdge, Timer
# from cocotb.clock import Clock
# from cocotb.binary import BinaryValue

# from pyuvm import *

# import random

# class RegisterSeqItem(uvm_sequence_item):
#     def __init__(self, read_from_bus=False, write_to_bus=False, bus_value=0):
#         super().__init__("RegisterSeqItem")
#         self.read_from_bus = read_from_bus
#         self.write_to_bus = write_to_bus
#         self.bus_value = bus_value

# class RegisterDriver(uvm_component):
#     def build_phase(self):
#         self.seq_item_port = uvm_seq_item_port("seq_item_port", self)

#     async def run_phase(self):
#         while True:
#             next_item = await self.seq_item_port.get_next_item()

#             self.dut.read_from_bus.value = next_item.read_from_bus
#             self.dut.write_to_bus.value = next_item.write_to_bus

#             if next_item.write_to_bus == 1 and next_item.read_from_bus == 0:
#                 self.logger.info(f"DRIVING {next_item.bus_value}")
#                 self.dut.bus_driver.setimmediatevalue(next_item.bus_value)
#                 self.dut.bus_driver._write = True
#             else:
#                 self.logger.info("HIGH Z")
#                 self.dut.bus_driver.setimmediatevalue(BinaryValue(value="zzzzzzzz", n_bits=8))
#                 self.dut.bus_driver._write = False
            
#             await RisingEdge(self.dut.clk)
#             self.seq_item_port.item_done()

# class RegisterSeqence(uvm_sequence):
#     async def body(self):
#         rst = RegisterSeqItem()
#         await self.start_item(rst)
#         self.driver.dut.rst.value = 1
#         await RisingEdge(self.driver.dut.clk)
#         await self.finish_item(rst)
#         self.driver.dut.rst.value = 0
        
#         # Read from bus
#         item = RegisterSeqItem(read_from_bus=True, bus_value=0x55)
#         await self.start_item(item)
#         await self.finish_item(item)

#         # Write to bus
#         item = RegisterSeqItem(write_to_bus=True)
#         await self.start_item(item)
#         await self.finish_item(item)

#         # 100 random reads and writes
#         for i in range(100):
#             read = random.randint(0, 1)
#             item = RegisterSeqItem(read_from_bus=read, write_to_bus=not read, bus_value=random.randint(0, 0xFF))
#             await self.start_item(item)
#             await self.finish_item(item)


# """
#     Compare current state with expectations and report errors
# """
# class RegisterScoreboard(uvm_component):
#     def __init__(self, name, parent):
#         super().__init__(name, parent)
#         self.expected_value = 0
    
#     def build_phase(self):
#         self.dut = RegisterDriver.dut

#     async def run_phase(self):
#         while True:
#             await RisingEdge(self.dut.clk)

#             if self.dut.rst == 1:
#                 self.expected_value = 0
            
#             self.logger.info(f"""Reset:\t\t{self.dut.rst}
#                            Read from bus:\t{self.dut.read_from_bus}
#                            Write to bus:\t{self.dut.write_to_bus}
#                            Value:\t\t{self.dut.value}""")

#             # Check value
#             if self.expected_value == self.dut.value.value:
#                 self.logger.info(f"Value match - Expected: {self.expected_value} Actual: {self.dut.value}")
#             else:
#                 self.logger.error(f"Value ERROR - Expected: {self.expected_value} Actual: {self.dut.value}")
            
#             # Check bus
#             if self.dut.write_to_bus.value == 1:
#                 if self.expected_value == self.dut.bus.value:
#                     self.logger.info(f"Bus match - Expected: {self.expected_value} Actual: {self.dut.bus}")
#                 else:
#                     self.logger.error(f"Bus ERROR - Expected: {self.expected_value} Actual: {self.dut.bus}")
            
#             if self.dut.read_from_bus == 1:
#                 self.expected_value = self.dut.bus.value

# """
#     Test setup
# """
# class RegisterTest(uvm_test):
#     def build_phase(self):
#         self.seqr = uvm_sequencer("seqr", self)
#         self.driver = RegisterDriver("driver", self)
#         self.seq = RegisterSeqence("seq")
#         self.scoreboard = RegisterScoreboard("scoreboard", self)

#     def connect_phase(self):
#         self.seq.driver = self.driver
#         self.seq.driver.dut = self.driver.dut
#         self.seq.driver.seq_item_port.connect(self.seqr.seq_item_export)
    
#     async def run_phase(self):
#         self.raise_objection()
#         await self.seq.start(self.seqr)
#         self.drop_objection()

# """
#     Test entry point
# """
# @cocotb.test()
# async def run(dut):
#     clock = Clock(dut.clk, 10, units="ns")
#     cocotb.start_soon(clock.start())
#     RegisterDriver.dut = dut
#     await uvm_root().run_test("RegisterTest")


"""
    UVM Phases

    Build
        Build
        Connect
        Elaboration
    Simulation (run is parrallel to others which are in series)
        Run
        ----
        Reset
        Configure
        Main
        Shutdown
    Clean up
        Extract
        Check
        Report
        Final
"""

from cocotb.triggers import FallingEdge, Timer
from cocotb.queue import Queue

import pyuvm
from pyuvm import *

import random

@pyuvm.test()
class RegisterTest(uvm_test):
    def build_phase(self):
        self.logger.info("RegisterTest in build phase")

        self.env = RegisterEnv("env", self)
    
    def end_of_elaboration_phase(self):
        self.logger.info("RegisterTest in end of elaboration phase")

        self.test_all = TestAllSeq.create("test_all")
    
    async def run_phase(self):
        self.logger.info("RegisterTest in run phase")

        self.raise_objection()
        await self.test_all.start()
        self.drop_objection()


class RegisterEnv(uvm_env):
    def build_phase(self):
        self.logger.info("RegisterEnv in build phase")

        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = Driver("driver", self)
        self.cmd_mon = Monitor("cmd_mon", self, "get_cmd")
        self.coverage = Coverage("coverage", self)
        self.scoreboard = Scoreboard("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("RegisterEnv in connect phase")

        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.driver.ap.connect(self.scoreboard.result_export)
        self.cmd_mon.ap.connect(self.scoreboard.cmd_export) 
        self.cmd_mon.ap.connect(self.coverage.analysis_export)

class Monitor(uvm_component):
    def __init__(self, name, parent, cmd):
        super().__init__(name, parent)
        self.logger.info("Monitor __init__")
        self.cmd = cmd
        
    def build_phase(self):
        self.logger.info("Monitor in build phase")

        self.ap = uvm_analysis_port("ap", self)
        self.bfm = RegisterBFM()
        self.get_method = getattr(self.bfm, self.cmd)

    async def run_phase(self):
        self.logger.info("Monitor in run phase")

        while True:
            datum = await self.get_method()
            self.logger.debug(f"MONITORED {datum}")
            self.ap.write(datum)

class Scoreboard(uvm_component):
    def build_phase(self):
        self.logger.info("Scoreboard in build phase")

        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self)
        self.result_export = self.result_fifo.analysis_export
        self.result_get_port = uvm_get_port("result_get_port", self)

        self.cmd_fifo = uvm_tlm_analysis_fifo("cmd_fifo", self)
        self.cmd_export = self.cmd_fifo.analysis_export
        self.cmd_get_port = uvm_get_port("cmd_get_port", self)
    
    def connect_phase(self):
        self.logger.info("Scoreboard in connect phase")

        self.result_get_port.connect(self.result_fifo.get_export)
        self.cmd_get_port.connect(self.cmd_fifo.get_export)

    def check_phase(self):
        self.logger.info("Scoreboard in check phase")

        while self.result_get_port.can_get():
            _, actual_result = self.result_get_port.try_get()
            cmd_success, cmd = self.cmd_get_port.try_get()
            if not cmd_success:
                self.logger.critical(f"result {actual_result} has no command")            
            else:
                # FIXME: IDK what's going on here but it seems very ALU specific so here's my interpretation for now
                (read_from_bus, write_to_bus, bus) = cmd
                # predicted_result = predict_result(*cmd)
                # if predicted_result == actual_result:
                #     self.logger.info(f"Passed: Read={read_from_bus}, write={write_to_bus}, predicted={predicted_result}, actual={actual_result}")
                # else:
                #     self.logger.error(f"FAILED: Read={read_from_bus}, write={write_to_bus}, predicted={predicted_result}, actual={actual_result}")

# TODO: Not sure what coverage is needed for a register
# Read and write to all value
# Repeated reads
# Repeated writes
# Read following write
# Write following read
# No ops
# Simutanius read and write signal
# Reset
class Coverage(uvm_subscriber):
    def write(self, cmd):
        pass
        
class Driver(uvm_driver):
    def build_phase(self):
        self.logger.info("Driver in build phase")

        self.ap = uvm_analysis_port("ap", self)
    
    def start_of_simulation_phase(self):
        self.logger.info("Driver in start of simulation phase")

        self.bfm = RegisterBFM()
    
    async def launch_tb(self):
        self.logger.info("Launching TB")
        await self.bfm.reset() # FIXME: Currently hanging forever because time isn't passing in the simulation
        self.logger.info("BFM reset")
        self.bfm.start_bfm()
        self.logger.info("Tasks started")

    async def run_phase(self):
        self.logger.info("Driver in run phase")

        await self.launch_tb()
        while True:
            self.logger.info("driver looping")
            cmd = await self.seq_item_port.get_next_item()
            self.logger.info("driver cmd got")
            await self.bfm.send_op(cmd) # FIXME: Currently hanging forever because time isn't passing in the simulation
            self.logger.info("driver send op")
            result = await self.bfm.get_result()
            self.logger.info("driver results got")
            self.ap.write(result)
            self.logger.info("driver cmd got")
            cmd.result = result
            self.seq_item_port.item_done()

class RegisterBFM(metaclass=utility_classes.Singleton):
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=0)
        self.cmd_mon_queue = Queue(maxsize=0)
        self.result_mon_queue = Queue(maxsize=0)

    async def get_cmd(self):
        cmd = await self.cmd_mon_queue.get()
        return cmd

    async def get_result(self):
        print("get_results")
        res = await self.result_mon_queue.get()
        print("got results")
        return res
    
    async def reset(self):
        await FallingEdge(self.dut.clk)
        self.dut.rst.value = 1
        await FallingEdge(self.dut.clk)
        self.dut.rst.value = 0
        await FallingEdge(self.dut.clk)
    
    async def send_op(self, cmd):
        await self.driver_queue.put(cmd)

    async def cmd_mon_bfm(self):
        while True:
            await FallingEdge(self.dut.clk)
            self.cmd_mon_queue.put_nowait((self.dut.read_from_bus, self.dut.write_to_bus, self.dut.bus_driver))

    async def result_mon_bfm(self):
        while True:
            await FallingEdge(self.dut.clk)
            self.result_mon_queue.put_nowait(self.dut.value)

    async def driver_bfm(self):
        self.dut.read_from_bus.value = 0
        self.dut.write_to_bus.value = 0
        self.dut.bus_driver.value = 0

        while True:
            await FallingEdge(self.dut.clk)
            try:
                item = self.driver_queue.get_nowait()
                self.dut.read_from_bus.value = item.read_from_bus
                self.dut.write_to_bus.value = item.write_to_bus
                self.dut.bus_driver.value = item.bus_value
            except QueueEmpty:
                pass

    def start_bfm(self):
        cocotb.start_soon(self.driver_bfm())
        cocotb.start_soon(self.cmd_mon_bfm())
        cocotb.start_soon(self.result_mon_bfm())


# Read and write to all value
# Repeated reads
# Repeated writes
# Read following write
# Write following read
# No ops
# Simultanius read and write signal
# Reset        
class TestAllSeq(uvm_sequence):
    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random_seq = RandomSeq("random")
        await random_seq.start(seqr)
    
class RandomSeq(uvm_sequence):
    async def body(self):
        cmd_tr = RegisterSeqItem("random")
        print("STARTING")
        await self.start_item(cmd_tr)
        print("STARTIED")
        cmd_tr.randomize()
        await self.finish_item(cmd_tr)
        await Timer(200, units="ns")

class RegisterSeqItem(uvm_sequence_item):
    def __init__(self, name, read_from_bus=False, write_to_bus=False, bus_value=0x00):
        super().__init__(name)
        self.read_from_bus = read_from_bus
        self.write_to_bus = write_to_bus
        self.bus_value = bus_value
    
    def randomize(self):
        self.read_from_bus = bool(random.randint(0, 1))
        self.write_to_bus = bool(random.randint(0, 1))
        self.bus_value = random.randint(0, 0xFF)

    def __eq__(self, other):
        return (self.read_from_bus == other.read_from_bus and self.write_to_bus == other.write_to_bus and self.bus_value == other.bus_value)
