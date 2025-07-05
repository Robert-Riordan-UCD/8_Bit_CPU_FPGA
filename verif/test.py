#! /usr/bin/python3

import pyuvm
from pyuvm import *

@pyuvm.test()
class AluTest(uvm_test):
    def build_phase(self):
        self.env = AluEnv("env", self)
    
    def end_of_elaboration_phase(self):
        self.test_all = TestAllSeq.create("test_all")
    
    async def run_phase(self):
        self.raise_objection()
        await self.test_all.start()
        self.drop_objection()

@pyuvm.test()
class ParallelTest(AluTest):
    def build_phase(self):
        uvm_factory().set_type_override_by_type(TestAllSeq, TestAllForkSeq)
        super().build_phase()

@pyuvm.test()
class FibonnacciTest(AluTest):
    def build_phase(self):
        ConfigDB().set(None, "*", "DISABLE_COVERAGE_ERRORS", True)
        uvm_factory().set_type_override_by_type(TestAllSeq, FibonnacciSeq)
        return super().build_phase()

class AluEnv(uvm_env):
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = Driver.create("driver", self)
        self.cmd_mon = Monitor("cmd_mon", self, "get_cmd")
        self.coverage = Coverage("coverage", self)
        self.scoreboard = Scoreboard("scoreboard", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.cmd_mon.ap.connect(self.scoreboard.cmd_export)
        self.cmd_mon.ap.connect(self.coverage.analysis_export)
        self.driver.ap.connect(self.scoreboard.result_export)

class Monitor(uvm_component):
    def __init__(self, name, parent, method_name):
        super().__init__(self, parent)
        self.method_name = method_name
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.bfm = TinyAluBfm()
        self.get_method = get_attr(self.bfm, self.method_name)
    
    async def run_phase(self):
        while True:
            datum = await self.get_method()
            self.logger.debug(f"MONITORED {datum}")
            self.ap.write(datum)

class Scoreboard(uvm_component):
    def build_phase(self):
        self.cmd_fifo = uvm_tlm_analysis_fifo("cmd_fifo", self)
        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self)
        self.cmd_get_port = uvm_get_port("cmd_get_port", self)
        self.result_get_port = uvm_get_port("result_get_port", self)
        self.cmd_export = self.cmd_fifo.analysis_export
        self.result_export = self.result_fifo.analysis_export
    
    def connect_phase(self):
        self.cmd_get_port.connect(self.cmd_fifo.get_export)
        self.result_get_port.connect(self.result_fifo.get_export)
    
    def check_phase(self):
        while self.result_get_port.can_get():
            _, actual_result = self.result_get_port.try_get()
            cmd_success, cmd = self.cmd_get_port.try_get()
            if not cmd_success:
                self.logger.critical(f"result {actual_result} had no command")
            else:
                (A, B, op_numb) = cmd
                op = Ops(op_numb)
                predicted_result = alu_prediction(A, B, op)
                if predicted_result == actual_result:
                    self.logger.info("PASSED: 0x{A:02x} {op.name} 0x{B:02x} = 0x{actual_result:04x}")
                else:
                    self.logger.error(f"FAILED: 0x{A:02x} {op.name} 0x{B:02x} = 0x{actual_result:04x} expected 0x{predicted_result:04x}")

class Coverage(uvm_subscriber):
    def end_of_elaboration_phase(self):
        self.cvg = set()
    
    def write(self, cmd):
        (_, _, op) = cmd
        self.cvg.add(op)
    
    def report_phase(self):
        try:
            disable_errors = ConfigDB.get(self, "", "DISABLE_COVERAGE_ERRORS")
        except UVMConfigItemNotFound:
                disable_errors = False
        
        if not disable_errors:
            if len(set(Ops) - self.cvg) > 0:
                self.logger.error(f"Functional coverage error. Missed {set(Ops) - self.cvg}")
                assert False
            else:
                self.logger.info("Covered all operations")
                assert True

class Driver(uvm_driver):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    def start_of_simulation_phase(self):
        self.bfm = TinyAluBfm()
    
    async def launch_tb(self):
        await self.bfm.reset()
        self.bfm.start_tasks()
    
    async def run_phase(self):
        await self.launch_tb()
        while True:
            cmd = await self.seq_item_port.get_next_item()
            await self.bfm.send_op(cmd.A, cmd.B, cmd.op)
            result = await self.bfm.get_result()
            self.ap.write(result)
            cmd.result = result
            self.seq_item_port.item_done()

class TestAllSeq(uvm_sequence):
    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random = RandomSeq("random")
        max_op = MaxSeq("max")
        await random.start(seqr)
        await max_op.start(seqr)

class RandomSeq(uvm_sequence):
    async def body(self):
        for op in list(Ops):
            cmd_tr = AluSeqItem("cmd_tr", None, None, op)
            await self.start_item(cmd_tr)
            cmd_tr.randomize_operands()
            await self.finish_item(cmd_tr)

class MaxSeq(uvm_sequence):
    async def body(self):
        for op in list(Ops):
            cmd_tr = AluSeqItem("cmd_tr", 0xff, 0xff, op)
            await self.start_item(cmd_tr)
            await self.finish_item(cmd_tr)

class AluSeqItem(uvm_sequence_item):
    def __init__(self, name, aa, bb, op):
        super.__init__(name)
        self.A = aa
        self.B = bb
        self.op = Ops(op)
    
    def randomize_operands(self):
        self.A = random.randint(0, 255)
        self.B = random.randint(0, 255)
    
    def randomize(self):
        self.randomize_operands()
        self.op = random.choice(list(Ops))
    
    def __eq__(self, other):
        return self.A == other.A and self.B == other.B and self.op == other.op
    
    def __str__(self):
        return f"{self.get_name()} : A: 0x{self.A:02x} OP: 0x{self.op.name} ({self.op.value}) B: 0x{self.B:02x}"

print("Hello")

