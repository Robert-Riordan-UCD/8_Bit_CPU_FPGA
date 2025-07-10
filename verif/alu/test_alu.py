import cocotb, pyuvm

from alu_pkg.test import Test

@cocotb.test
async def run_test(dut):
    await pyuvm.uvm_root().run_test("Test")